import numpy as np
import xarray as xr

from typing import TYPE_CHECKING, Any, Callable, Hashable
from quantify_scheduler.gettables import _evaluate_parameter_dict
from quantify_scheduler.device_under_test.quantum_device import QuantumDevice
from quantify_scheduler.instrument_coordinator.components.base import (
    instrument_to_component_name,
)
from numpy.typing import NDArray


# creating a new gettable that pings the instrument coordinator and satsifies meas-control


class ZISpectroscopyGettable:
    """Allows skipping compilation and directly pinging the instrument coordinator component.

    Used only for fast frequency sweeping.

    Parameters
    ----------
    quantum_device
        The qcodes instrument representing the quantum device under test (DUT)
        containing quantum device properties and setup configuration information.
        This is used to extract the Instrument coordinator and the device setup.
    implemented_experiment
        A function which returns a dataset from a LabOneQ experiment.
    schedule_kwargs
        The schedule function keyword arguments, when a value in this dictionary is
        a :class:`~qcodes.instrument.parameter.Parameter`, this parameter will be
        evaluated every time :code:`.get()` is called before being passed to the
        :code:`schedule_function`.
    num_channels
        The number of channels to expect in the acquisition data.
    data_labels
        Allows to specify custom labels. Needs to be precisely 2*num_channels if
        specified. The order is [Voltage I 0, Voltage Q 0, Voltage I 1, Voltage Q 1,
        ...], in case real_imag==True, otherwise [Magnitude 0, Phase 0, Magnitude 1,
        Phase 1, ...].
    real_imag
        If true, the gettable returns I, Q values. Otherwise, magnitude and phase
        (degrees) are returned.
    batched
        Used to indicate if the experiment is performed in batches or in an
        iterative fashion.
    max_batch_size:
        Determines the maximum number of points to acquire when acquiring in batched
        mode. Can be used to split up a program in parts if required due to hardware
        constraints.
    always_initialize:
        If True, then reinitialize the schedule on each invocation of ``get``. If
        False, then only initialize the first invocation of ``get``.

    Returns
    -------
    :
        A MeasurementControl compatible gettable for spectroscopy with ZI
    """

    def __init__(
        self,
        quantum_device: QuantumDevice,
        implemented_experiment: Callable,
        experiment_args: dict[str, Any],
        num_channels: int = 1,
        real_imag: bool = True,
        batched: bool = True,
        batch_size: int = 1024,
    ):
        self.implemented_experiment = implemented_experiment
        self.experiment_args = experiment_args
        self.quantum_device = quantum_device
        self.batched = batched
        self.batch_size = batch_size

        # creating an empty attribut to later hold
        # the instrument coordinator component for ZI
        self.icc = None

        self.real_imag = real_imag
        if self.real_imag:
            self.name = ["I", "Q"] * num_channels
            self.label = [
                f"Voltage {iq}{ch}" for ch in range(num_channels) for iq in ["I", "Q"]
            ]
            self.unit = ["V", "V"] * num_channels
        else:
            self.name = ["magn", "phase"] * num_channels
            self.label = [
                f"{val_label}{ch}"
                for ch in range(num_channels)
                for val_label in ["Magnitude", "Phase"]
            ]

            self.unit = ["V", "deg"] * num_channels

    def initialize(self):

        experiment_args = _evaluate_parameter_dict(parameters=self.experiment_args)
        compiled_instructions = self.implemented_experiment(**experiment_args)

        # extracting the InstrumentCoordinatorComponent from quantum device
        instr_coordinator = self.quantum_device.instr_instrument_coordinator.get_instr()

        # extracting icc based on name given within quantum_device.hardware_config()["hardware_description"]
        icc_name = [
            key
            for key, value in self.quantum_device.hardware_config()[
                "hardware_description"
            ].items()
            if value["instrument_type"] == "ZIDeviceSetup"
        ]
        assert len(icc_name) == 1
        zi_icc = instr_coordinator.get_component(
            instrument_to_component_name(icc_name[0])
        )
        zi_icc.prepare(compiled_instructions)

        self.icc = zi_icc

    def get(self) -> tuple[np.ndarray, ...]:

        self.initialize()

        # getting the instrument coordinator component
        zi_icc = self.icc
        zi_icc.start()
        acquired_data = xr.Dataset()
        acquired_data = acquired_data.merge(zi_icc.retrieve_acquisition())

        if len(acquired_data) == 0:
            raise RuntimeError(
                f"ZIInstrumentCoordinatorComponent.retrieve_acquisition() "
                + f"did not return any data, but was expected to return data."
            )
        result = self.process_acquired_data(acquired_data)
        return result

    def _reshape_data(self, acq_protocol: str, vals: NDArray) -> list[NDArray]:

        if acq_protocol == "ThresholdedAcquisition":
            return [vals.real.astype(np.uint32)]
        if acq_protocol in (
            "Trace",
            "SSBIntegrationComplex",
            "ThresholdedAcquisition",
            "WeightedIntegratedSeparated",
            "NumericalSeparatedWeightedIntegration",
            "NumericalWeightedIntegration",
        ):
            ret_val = []
            if self.real_imag:
                ret_val.append(vals.real)
                ret_val.append(vals.imag)
                return ret_val
            else:
                ret_val.append(np.abs(vals))
                ret_val.append(np.angle(vals, deg=True))
                return ret_val

        raise NotImplementedError(
            f"Acquisition protocol {acq_protocol} is not supported."
        )

    def process_acquired_data(  # noqa: PLR0912
        self,
        acquired_data: xr.Dataset,
    ) -> tuple[NDArray[np.float64], ...]:
        """
        Reshapes the data as returned from the instrument coordinator into the form
        accepted by the measurement control.

        Parameters
        ----------
        acquired_data
            Data that is returned by instrument coordinator.

        Returns
        -------
        :
            A tuple of data, casted to a historical conventions on data format.
        """
        # retrieve the acquisition results

        return_data = []
        # We sort acquisition channels so that the user
        # has control over the order of the return data.
        # https://gitlab.com/quantify-os/quantify-scheduler/-/issues/466
        sorted_acq_channels: list[Hashable] = sorted(acquired_data.data_vars)
        for idx, acq_channel in enumerate(sorted_acq_channels):
            acq_channel_data = acquired_data[acq_channel]
            acq_protocol = acq_channel_data.attrs["acq_protocol"]

            num_dims = len(acq_channel_data.dims)

            if acq_protocol in (
                "SSBIntegrationComplex",
                "WeightedIntegratedSeparated",
                "NumericalSeparatedWeightedIntegration",
                "NumericalWeightedIntegration",
                "ThresholdedAcquisition",
            ) and num_dims not in (1, 2):
                raise TypeError(
                    f"Data returned by an instrument coordinator component for "
                    f"{acq_protocol} acquisition protocol is expected to be an "
                    f"array of complex numbers with with one or two dimensions: "
                    f"acquisition index and optionally repetition index. This is not the case for "
                    f"acquisition channel {acq_channel}, that has data "
                    f"type {acq_channel_data.dtype} and {num_dims} dimensions: "
                    f"{', '.join(str(dim) for dim in acq_channel_data.dims)}."
                )

            vals = acq_channel_data.to_numpy().reshape((-1,))

            if not self.batched and len(vals) != 1:
                raise ValueError(
                    f"For iterative mode, only one value is expected for each "
                    f"acquisition channel. Got {len(vals)} values for acquisition "
                    f"channel '{acq_channel}' instead."
                )
            return_data.extend(self._reshape_data(acq_protocol, vals))

        return tuple(return_data)
