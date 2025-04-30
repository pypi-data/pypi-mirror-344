"""Init script for quantum machines setup."""

from __future__ import annotations

from pathlib import Path

import quantify_core.visualization.pyqt_plotmon as pqm
from laboneq.simple import (
    HDAWG,
    PQSC,
    SHFQC,
    DeviceSetup,
    create_connection,
)
from quantify_core.data.handling import get_datadir, set_datadir
from quantify_core.measurement.control import MeasurementControl
from quantify_scheduler.device_under_test.quantum_device import QuantumDevice
from quantify_scheduler.device_under_test.transmon_element import (
    BasicTransmonElement,
)
from quantify_scheduler.instrument_coordinator import InstrumentCoordinator
from zmq import device

from quantify_zurich_instruments.instrument_coordinator import (
    ZIInstrumentCoordinatorComponent,
)
from laboneq.simple import (
    SHFQC,
    HDAWG,
    PQSC,
    DeviceSetup,
    Session,
    create_connection,
)

if TYPE_CHECKING:
    from quantify_core.data.types import TUID

# set datadir path
set_datadir(Path.home() / "quantify-data")
get_datadir()

# set quantum device and element
quantum_device = QuantumDevice("quantum_device")

q0 = BasicTransmonElement("q0")

# set meas_ctrl
meas_ctrl = MeasurementControl("meas_ctrl")
quantum_device.instr_measurement_control(meas_ctrl.name)

# get hardware config
hardware_compilation_config = {
    "config_type": "quantify_zurich_instruments.datastructures.ZIHardwareCompilationConfig",
    "hardware_description": {
        "zi_device_setup": {
            "instrument_type": "ZIDeviceSetup",
            "dataserver": ("localhost", "8004"),
        }
    },
    "hardware_options": {
        "modulation_frequencies": {
            "q0:res-q0.ro-output": {"interm_freq": None, "lo_freq": 7e9},
            "q0:res-q0.ro-input": {"interm_freq": None, "lo_freq": 7e9},
            "q0:mw-q0.01-output": {"interm_freq": 100e6, "lo_freq": None},
        }
    },
    "connectivity": {
        "graph": [
            # Connect Quantify ports to LabOne Q logical signal groups
            # from the device setup:
            ("q0:res", "shfqc_01:qachannels_0_output"),
            ("shfqc_01:qachannels_0_input", "q0:res"),
            ("q0:mw", "shfqc_01:sgchannels_0_output"),
            ("q0:fl", "hdawg_01:sigouts_0"),
        ]
    },
}
quantum_device.hardware_config(hardware_compilation_config)

device_setup = DeviceSetup("zi_device_setup")
device_setup.add_dataserver("localhost", "8004")

device_setup.add_instruments(
    SHFQC(
        uid="shfqc_01",
        address="DEV12382",  # your device address here
        device_options="SHFQC/QC2CH",
    ),
)
device_setup.add_instruments(
    HDAWG(
        uid="hdawg_01",
        address="DEV8938",  # your device address here
    )
)
device_setup.add_instruments(
    PQSC(
        uid="pqsc_01",
        address="DEV10166",  # your device address here
        reference_clock_source="internal",
    )
)

device_setup.add_connections(
    "shfqc_01",
    create_connection(
        to_signal="shfqc_01/sgchannels_0_output",
        ports="SGCHANNELS/0/OUTPUT",
    ),
    create_connection(
        to_signal="shfqc_01/qachannels_0_output",
        ports="QACHANNELS/0/OUTPUT",
    ),
    create_connection(
        to_signal="shfqc_01/qachannels_0_input",
        ports="QACHANNELS/0/INPUT",
    ),
)
device_setup.add_connections(
    "hdawg_01",
    create_connection(
        to_signal="hdawg_01/sigouts_0",
        ports="SIGOUTS/0",
    ),
    create_connection(
        to_signal="hdawg_01/sigouts_1",
        ports="SIGOUTS/1",
    ),
    create_connection(
        to_signal="hdawg_01/sigouts_2",
        ports="SIGOUTS/2",
    ),
    create_connection(
        to_signal="hdawg_01/sigouts_3",
        ports="SIGOUTS/3",
    ),
)
device_setup.add_connections(
    "pqsc_01",
    create_connection(
        to_instrument="sfqc_01",
        ports="ZSYNCS/0",
    ),
    create_connection(
        to_instrument="hdawg_01",
        ports="ZSYNCS/1",
    ),
)

# set instrument coordinator
ic = InstrumentCoordinator("ic")
comp_config = quantum_device.generate_compilation_config()
zi_icc = ZIInstrumentCoordinatorComponent(
    device_setup=device_setup,
    do_emulation=False,  # set to False to run on actual hardware
)
quantum_device.instr_instrument_coordinator(ic.name)
ic.add_component(zi_icc)


# set plotmon
plotmon = pqm.PlotMonitor_pyqt("plotmon")
# Connect the live plotting monitor to the measurement control
meas_ctrl.instr_plotmon(plotmon.name)

# LAST_TUID: TUID = None  # type: ignore # "20220831-163314-515-477c3d"
list_of_qubits = [
    q0,
]
for qubit in list_of_qubits:
    quantum_device.add_element(qubit)

    # # loads settings from the last datafile onto these instruments
    # try:
    #     load_settings_onto_instrument(instrument=qubit, tuid=LAST_TUID)
    # except ValueError:
    #     print(f"Failed loading {qubit}")
    #     continue

list_of_edges = []
for edge in list_of_edges:
    quantum_device.add_edge(edge)

    # loads settings from the last datafile onto these instruments
    # try:
    #     load_settings_onto_instrument(instrument=edge, tuid=LAST_TUID)
    # except ValueError:
    #     print(f"Failed loading {edge}")
    #     continue
