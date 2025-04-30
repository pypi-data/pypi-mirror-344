"""Datastructures for the ZI backend."""

from __future__ import annotations

from typing import Literal, Optional, Union

from laboneq.core.types.enums import AcquisitionType, ReferenceClockSource
from laboneq.dsl.device.instruments.zi_standard_instrument import ZIStandardInstrument
from pydantic import Field, ConfigDict
from quantify_scheduler.backends.graph_compilation import SimpleNodeConfig
from quantify_scheduler.backends.types.common import (
    HardwareCompilationConfig,
    HardwareDescription,
    HardwareOptions,
)
from quantify_scheduler.enums import BinMode
from quantify_scheduler.structure.model import DataStructure


class ZIDeviceSetupDescription(HardwareDescription):
    """Specification of the ZI DeviceSetup in the :class:`~.ZIHardwareCompilationConfig`."""

    # Arbitrary types are required for the ZIStandardInstrument
    model_config = ConfigDict(arbitrary_types_allowed=True)

    instrument_type: Literal["ZIDeviceSetup"]

    dataserver: tuple[str, str]
    """The IP address and port of the dataserver to connect to."""
    instruments: dict[str, ZIStandardInstrument] = {}
    """The instruments to add to the device setup."""


class ZIHardwareOptions(HardwareOptions):
    """Hardware options for the ZI backend."""

    output_att: dict[str, int] | None = None
    """
    Dictionary containing the attenuation settings (values) that should be applied
    to the outputs that are connected to a certain port-clock combination (keys).
    """


class ZIHardwareCompilationConfig(HardwareCompilationConfig):
    """Datastructure containing all the information needed to compile to a LabOne Q Experiment."""

    hardware_description: dict[str, ZIDeviceSetupDescription]
    hardware_options: ZIHardwareOptions
    compilation_passes: list[SimpleNodeConfig] = Field(
        default=[
            {
                "name": "flatten_schedule",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".flatten_schedule",
            },
            {
                "name": "initialize_compiled_instructions",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".initialize_compiled_instructions",
            },
            {
                "name": "compile_experiment_signals",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".compile_experiment_signals",
            },
            {
                "name": "compile_operations",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".compile_operations",
            },
            {
                "name": "compile_calibration",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".compile_calibration",
            },
            {
                "name": "compile_acquisition_config",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".compile_acquisition_config",
            },
            {
                "name": "snap_timing_to_system_grid",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".snap_timing_to_system_grid",
            },
            {
                "name": "compile_experiment",
                "compilation_func": "quantify_zurich_instruments.compilation"
                + ".compile_experiment",
            },
        ],
        validate_default=True,
    )


class AcquisitionConfig(DataStructure):
    """Acquisition Config used to format acquired data in the InstrumentCoordinator."""

    bin_mode: Union[BinMode, None]  # noqa: UP007
    # The following acquisition types are supported
    acq_protocols: dict[
        int, Literal["Trace", "SSBIntegrationComplex", "WeightedIntegratedComplex"]
    ]
    n_acquisitions: int
    acquisition_type: AcquisitionType
