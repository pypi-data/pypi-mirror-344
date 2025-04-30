from collections.abc import Hashable

import logging
import numpy as np
import xarray as xr
from laboneq.simple import DeviceSetup, Session
from qcodes.instrument import InstrumentBase
from quantify_scheduler.enums import BinMode
from quantify_scheduler.instrument_coordinator.components.base import (
    InstrumentCoordinatorComponentBase,
)


class ZIInstrumentCoordinatorComponent(InstrumentCoordinatorComponentBase):
    """Instrument coordinator component for the Zurich Instruments backend."""

    def __new__(
        cls, device_setup: DeviceSetup, do_emulation: bool = False
    ) -> InstrumentCoordinatorComponentBase:
        """Create a dummy instrument to be compatible with ICCBase.__new__."""
        instrument = InstrumentBase(name=device_setup.uid)
        instance = super().__new__(cls, instrument)
        return instance

    def __init__(self, device_setup: DeviceSetup, do_emulation: bool = False):
        """Initialize LabOneQ session, and create dummy instrument for ZI cluster."""
        # Create a dummy instrument to be compatible with ICCBase.__init__
        instrument = InstrumentBase(name=device_setup.uid)
        super().__init__(instrument)

        self.device_setup = device_setup
        self.session = None
        self.experiment = None
        self.result = None
        self.do_emulation = do_emulation
        self.acquisition_config = None

    def get_hardware_log(self):
        pass

    def is_running(self) -> bool:
        return True

    def prepare(self, compiled_instructions: dict) -> None:
        experiment = compiled_instructions["experiment"]

        self.acquisition_config = compiled_instructions["acquisition_config"]

        self.session = Session(device_setup=self.device_setup, log_level=logging.ERROR)
        self.session.connect(do_emulation=self.do_emulation)
        self.experiment = experiment

    def start(self) -> None:
        self.result = self.session.run(self.experiment)

        if self.result.execution_errors:
            raise Exception(self.result.execution_errors)

    def retrieve_acquisition(self) -> xr.Dataset:
        assert self.result is not None
        assert self.acquisition_config is not None

        acq_channel_results: list[dict[Hashable, xr.DataArray]] = []
        for acq_channel, acq_protocol in self.acquisition_config.acq_protocols.items():
            # Get data arrays
            data = np.array(
                self.result.acquired_results[f"ACQ_CHANNEL_{acq_channel}"].data
            )

            if acq_protocol == "Trace":
                if self.acquisition_config.bin_mode == BinMode.AVERAGE:
                    acq_channel_results.append(
                        {
                            acq_channel: xr.DataArray(
                                # Should be one averaged array
                                data.reshape((1, -1)),
                                dims=(
                                    f"acq_index_{acq_channel}",
                                    f"trace_index_{acq_channel}",
                                ),
                                attrs={"acq_protocol": acq_protocol},
                            )
                        }
                    )
                elif self.acquisition_config.bin_mode == BinMode.APPEND:
                    raise NotImplementedError(
                        "Append mode not yet implemented for the ZI backend"
                    )
                    acq_channel_results.append(
                        {
                            acq_channel: xr.DataArray(
                                data.reshape(
                                    (-1, self.acquisition_config.n_acquisitions)
                                ),
                                dims=(
                                    f"acq_index_{acq_channel}",
                                    f"trace_index_{acq_channel}",
                                ),
                                attrs={"acq_protocol": acq_protocol},
                            )
                        }
                    )

            elif acq_protocol in ("SSBIntegrationComplex", "WeightedIntegratedComplex"):
                if self.acquisition_config.bin_mode == BinMode.AVERAGE:
                    acq_channel_results.append(
                        {
                            acq_channel: xr.DataArray(
                                # Sanity check: data size must be equal to n_acquisitions
                                data.reshape((self.acquisition_config.n_acquisitions,)),
                                dims=(f"acq_index_{acq_channel}",),
                                attrs={"acq_protocol": acq_protocol},
                            )
                        }
                    )
                elif self.acquisition_config.bin_mode == BinMode.APPEND:

                    acq_channel_results.append(
                        {
                            acq_channel: xr.DataArray(
                                data.reshape(
                                    (-1, self.acquisition_config.n_acquisitions)
                                ),
                                dims=("repetition", f"acq_index_{acq_channel}"),
                                attrs={"acq_protocol": acq_protocol},
                            )
                        }
                    )
            else:
                raise NotImplementedError(f"{acq_protocol=} not implemented.")

            return xr.merge(acq_channel_results, compat="no_conflicts")

        # TODO: figure out how this should work for different acquisition protocols.
        # In other backends, a separate acq_config is compiled which is then
        # used here to map the results onto the correct xarray Dataset.

        # acq_channel_results: list[xr.DataArray] = []
        # for res_handle, res_handle_result in self.result.acquired_results.items():
        #     acq_channel = int(res_handle[-1])
        #     acq_channel_results.append(
        #         xr.DataArray(
        #             np.array(res_handle_result.data).reshape((-1,)),
        #             dims=(f"acq_index_{acq_channel}",),
        #             name=acq_channel,
        #         )
        #     )
        # return xr.merge(acq_channel_results, compat="no_conflicts")

    def stop(self) -> None:
        pass

    def wait_done(self, timeout_sec: int = 10) -> None:
        pass
