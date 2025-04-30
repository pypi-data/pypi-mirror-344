import numpy as np
import xarray as xr

from typing import TYPE_CHECKING
from copy import deepcopy
from laboneq.simple import *
from quantify_scheduler.backends.types.common import Connectivity

from qcodes.instrument.base import Instrument
from quantify_zurich_instruments.datastructures import AcquisitionConfig
from quantify_scheduler.enums import BinMode

from quantify_zurich_instruments.compilation import _resolve_modulation_frequencies


def _exp_signal(port, clock, input=False, output=False):
    """Return the experiment signal name for a (port, clock) pair."""
    assert input ^ output, "experiment signal must be either input or output"
    assert (
        "output" not in clock
    ), "enter the clock name without specifying input or output"
    assert (
        "input" not in clock
    ), "enter the clock name without specifying input or output"
    if input:
        return f"{port}-{clock}-input"
    else:
        return f"{port}-{clock}-output"


def res_spectroscopy_pulsed(freq_sweep, num_averages, readout_pulse, qubit_name):

    ## define experimental sequence
    # outer loop - vary drive frequency
    measure = f"{qubit_name}:res-{qubit_name}.ro-output"
    acquire = f"{qubit_name}:res-{qubit_name}.ro-input"

    # Create resonator spectroscopy experiment - uses only readout drive and signal acquisition
    exp_spec_pulsed = Experiment(
        uid="Resonator Spectroscopy",
        signals=[
            ExperimentSignal(measure),
            ExperimentSignal(acquire),
        ],
    )

    qubit = Instrument.find_instrument(qubit_name)
    envelope_duration = qubit.measure.pulse_duration()

    # inner loop - average multiple measurements for each frequency - measurement in spectroscopy mode
    with exp_spec_pulsed.acquire_loop_rt(
        uid="shots",
        count=2**num_averages,
        acquisition_type=AcquisitionType.SPECTROSCOPY,
        averaging_mode=AveragingMode.SEQUENTIAL,
    ):
        with exp_spec_pulsed.sweep(uid="res_freq", parameter=freq_sweep):
            # readout pulse and data acquisition
            with exp_spec_pulsed.section(uid="spectroscopy"):
                # play resonator excitation pulse
                exp_spec_pulsed.play(signal=measure, pulse=readout_pulse)
                # resonator signal readout
                exp_spec_pulsed.acquire(
                    signal=acquire,
                    handle="ACQ_CHANNEL_0",  # hardcoding this since we assume that there is only one qubit
                    length=envelope_duration,
                )
            # relax time after readout - for signal processing and qubit relaxation to ground state
            with exp_spec_pulsed.section(uid="relax", length=1e-6):
                exp_spec_pulsed.reserve(signal=measure)

    return exp_spec_pulsed


# this needs as input the list of qubit_frequencies and the qubit/element name
# always ensure frequencies are in linspace to ensure the values being set from user are exactly the same
# of what we see from the analysis


def heterodyne_spec_zi(
    qubit_name,
    frequencies,
    quantum_device,
    amplitude: float = None,
):
    """
    a custom heterodyne spectroscopy schedule that takes in the qubit name and frequencies to sweep over.
    uses laboneq heterodyne spectroscopy implementation.
    ignores going via the compilation -> should give `compiled_instructions` dict directly
    for the instrument coordinator to call it.
    """
    compiled_instructions = {}
    qubit = Instrument.find_instrument(qubit_name)
    num_points = frequencies.size

    # obtaining the center frequency using the modulation frequencies
    # and qubit resonator frequency

    modulation_frequencies = quantum_device.hardware_config()["hardware_options"][
        "modulation_frequencies"
    ]

    if not qubit.clock_freqs.readout():
        raise ValueError(
            f"Qubit readout frequency missing, enter value by calling {qubit_name}.clock_freqs.readout()"
        )

    resonator_lo_freq = _resolve_modulation_frequencies(
        rf_freq=qubit.clock_freqs.readout(),
        interm_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "interm_freq"
        ],
        lo_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "lo_freq"
        ],
    ).lo_freq

    start_freq = frequencies[0] - resonator_lo_freq
    stop_freq = frequencies[-1] - resonator_lo_freq

    # frequency range of spectroscopy scan -
    # around expected centre frequency as defined in qubit parameters
    # define sweep parameter
    readout_freq_sweep_param = LinearSweepParameter(
        uid=f"{qubit_name}_res_freq",
        start=start_freq,
        stop=stop_freq,
        count=num_points,
        axis_name="Frequency [Hz]",
    )
    # define number of averages
    # used for 2^num_averages, maximum: num_averages = 17
    # within quantify we enter the averages directly,
    # so reverse-engineering repetitions to get laboneq num_averages
    num_averages = int(np.log2(quantum_device.cfg_sched_repetitions()))

    # readout pulse parameters and definition - to be filled in from device config

    envelope_duration = qubit.measure.pulse_duration()
    amplitude = amplitude if amplitude else qubit.measure.pulse_amp()
    readout_pulse = pulse_library.gaussian_square(
        uid="readout_pulse", length=envelope_duration, amplitude=amplitude
    )

    # define the experiment with the frequency sweep relevant for qubit 0
    exp_spec_pulsed = res_spectroscopy_pulsed(
        readout_freq_sweep_param, num_averages, readout_pulse, qubit_name
    )

    # adding base calibration to configure center frequency and pulse power

    resonator_interm_freq = _resolve_modulation_frequencies(
        rf_freq=qubit.clock_freqs.readout(),
        interm_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "interm_freq"
        ],
        lo_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "lo_freq"
        ],
    ).interm_freq

    # setting modulation frequencies

    # calibration of the readout line oscillator for the experimental signals
    exp_calibration = Calibration()
    # sets the oscillator of the experimental measure signal
    exp_calibration[f"{qubit_name}:res-{qubit_name}.ro-output"] = SignalCalibration(
        # for spectroscopy, use the hardware oscillator of the QA, and set the sweep parameter as frequency
        oscillator=Oscillator(
            "readout_osc",
            frequency=readout_freq_sweep_param,
            modulation_type=ModulationType.HARDWARE,
        ),
        local_oscillator=Oscillator(
            frequency=resonator_lo_freq
        ),  # both input and output should be same float value
        range=qubit.measure.reference_magnitude.dBm(),
    )

    # input calibration
    exp_calibration[f"{qubit_name}:res-{qubit_name}.ro-input"] = SignalCalibration(
        oscillator=Oscillator(
            frequency=resonator_interm_freq,
            modulation_type=ModulationType.SOFTWARE,  # for readout signals being sent from instrument
        ),  # is constant, with the baseband IF being re-calibrated after experiment
        local_oscillator=Oscillator(
            frequency=resonator_lo_freq
        ),  # both input and output should be same float value
        range=10,
    )

    # set signal calibration and signal map for experiment to qubit mentioned
    exp_spec_pulsed.set_calibration(exp_calibration)

    # setting signal map using connectivity from the hardware config
    connectivity = Connectivity.model_validate(
        quantum_device.hardware_config()["connectivity"]
    )

    graph = connectivity.graph

    edges = graph.edges
    signal_map = {}
    port = qubit.ports.readout()
    clock = f"{qubit_name}.ro"

    for logical_signal in graph.neighbors(port):
        if (port, logical_signal) in edges and logical_signal.endswith("_output"):
            output_signal = _exp_signal(port, clock, output=True)
            signal_map[output_signal] = logical_signal.replace(":", "/")
        if (logical_signal, port) in edges and logical_signal.endswith("_input"):
            input_signal = _exp_signal(port, clock, input=True)
            signal_map[input_signal] = logical_signal.replace(":", "/")

    exp_spec_pulsed.set_signal_map(signal_map)

    compiled_instructions["experiment"] = exp_spec_pulsed
    compiled_instructions["acquisition_config"] = AcquisitionConfig(
        bin_mode=BinMode.AVERAGE,
        acq_protocols={0: "SSBIntegrationComplex"},
        n_acquisitions=num_points,
        acquisition_type=AcquisitionType.SPECTROSCOPY,
    )

    return compiled_instructions


def qubit_spectroscopy_pulsed(
    freq_sweep,
    num_averages,
    readout_pulse,
    drive_pulse,
    qubit_name,
    readout_pulse_duration,
):
    """
    Define the signal lines and the acquisition loop.

    Acquisition loop contains of the pulses/operations being played on the pre-defined
    signal lines, new experiment line for drive.
    """

    # defining the experiment lines aka ports
    measure = f"{qubit_name}:res-{qubit_name}.ro-output"
    acquire = f"{qubit_name}:res-{qubit_name}.ro-input"
    drive = f"{qubit_name}:mw-{qubit_name}.01-output"

    # Create resonator spectroscopy experiment - uses only readout drive and signal acquisition
    exp_qspec = Experiment(
        uid="Drive Spectroscopy",
        signals=[
            ExperimentSignal(drive),
            ExperimentSignal(measure),
            ExperimentSignal(acquire),
        ],
    )

    # inner loop - real-time averaging - QA in integration mode
    with exp_qspec.acquire_loop_rt(
        uid="freq_shots",
        count=2**num_averages,
        acquisition_type=AcquisitionType.SPECTROSCOPY,
        averaging_mode=AveragingMode.CYCLIC,
    ):
        with exp_qspec.sweep(uid="qfreq_sweep", parameter=freq_sweep):
            envelope_duration = readout_pulse_duration
            with exp_qspec.section(uid="qubit_excitation"):
                exp_qspec.play(signal=drive, pulse=drive_pulse)
            with exp_qspec.section(
                uid="readout_section", play_after="qubit_excitation"
            ):
                # play readout pulse on measure line
                exp_qspec.play(signal=measure, pulse=readout_pulse)
                # trigger signal data acquisition
                exp_qspec.acquire(
                    signal=acquire,
                    handle="ACQ_CHANNEL_0",
                    length=envelope_duration,
                )
            # relax time after readout - for qubit relaxation to groundstate and signal processing
            with exp_qspec.section(
                uid="relax",
                length=1e-6,
            ):
                exp_qspec.reserve(signal=measure)

    return exp_qspec


def qubit_spectroscopy_zi(
    qubit_name,
    qubit_frequencies,
    quantum_device,
    amplitude,
    drive_envelope_duration,
    ref_magnitude,
):
    """
    a custom qubit spectroscopy schedule that takes in the qubit name, qubit_frequencies and amplitudes to sweep over.
    uses laboneq qubitspectroscopy implementation.
    ignores going via the compilation -> should give `compiled_instructions` dict directly
    for the instrument coordinator to call it.
    """
    compiled_instructions = {}
    qubit = Instrument.find_instrument(qubit_name)

    num_points = qubit_frequencies.size

    # obtaining the center frequency using the modulation qubit_frequencies
    # and qubit drive frequency
    modulation_frequencies = quantum_device.hardware_config()["hardware_options"][
        "modulation_frequencies"
    ]

    drive_lo_freq = _resolve_modulation_frequencies(
        rf_freq=qubit.clock_freqs.f01(),
        interm_freq=modulation_frequencies[f"{qubit_name}:mw-{qubit_name}.01-output"][
            "interm_freq"
        ],
        lo_freq=modulation_frequencies[f"{qubit_name}:mw-{qubit_name}.01-output"][
            "lo_freq"
        ],
    ).lo_freq
    start_freq = qubit_frequencies[0] - drive_lo_freq
    stop_freq = qubit_frequencies[-1] - drive_lo_freq

    # frequency range of spectroscopy scan -
    # around expected centre frequency as defined in qubit parameters
    # define sweep parameter
    drive_freq_sweep_param = LinearSweepParameter(
        uid=f"drive_freq_{qubit_name}",
        start=start_freq,
        stop=stop_freq,
        count=num_points,
        axis_name="Frequency [Hz]",
    )

    # define number of averages
    # used for 2^num_averages, maximum: num_averages = 17
    # within quantify we enter the averages directly,
    # so reverse-engineering repetitions to get laboneq num_averages
    num_averages = int(np.log2(quantum_device.cfg_sched_repetitions()))

    # readout pulse parameters and definition - obtain the calibrated values
    # from the qubit device config
    readout_pulse = pulse_library.gaussian_square(
        uid=f"readout_pulse_{qubit_name}",
        length=qubit.measure.pulse_duration(),
        amplitude=qubit.measure.pulse_amp(),
    )
    readout_pulse_duration = qubit.measure.pulse_duration()

    # drive pulse definition
    drive_pulse = pulse_library.const(
        uid="drive_pulse", length=drive_envelope_duration, amplitude=amplitude
    )

    # define the experiment with the frequency sweep relevant for qubit 0
    exp_qubit_spec_pulsed = qubit_spectroscopy_pulsed(
        drive_freq_sweep_param,
        num_averages,
        readout_pulse,
        drive_pulse,
        qubit_name,
        readout_pulse_duration,
    )

    # adding base calibration to configure center frequency and pulse power
    # calibration of the drive line oscillator for the experimental signals
    exp_calibration = Calibration()
    # sets the oscillator of the experimental measure signal
    exp_calibration[f"{qubit_name}:mw-{qubit_name}.01-output"] = SignalCalibration(
        # for spectroscopy, use the hardware oscillator of the SG, and set the sweep parameter as frequency
        oscillator=Oscillator(
            "drive_osc",
            frequency=drive_freq_sweep_param,
            modulation_type=ModulationType.HARDWARE,
        ),
        local_oscillator=Oscillator(frequency=drive_lo_freq),
        range=ref_magnitude,
    )

    # also set latest resonator calibration
    resonator_lo_freq = _resolve_modulation_frequencies(
        rf_freq=qubit.clock_freqs.readout(),
        interm_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "interm_freq"
        ],
        lo_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "lo_freq"
        ],
    ).lo_freq
    resonator_interm_freq = _resolve_modulation_frequencies(
        rf_freq=qubit.clock_freqs.readout(),
        interm_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "interm_freq"
        ],
        lo_freq=modulation_frequencies[f"{qubit_name}:res-{qubit_name}.ro-output"][
            "lo_freq"
        ],
    ).interm_freq

    exp_calibration[f"{qubit_name}:res-{qubit_name}.ro-output"] = SignalCalibration(
        oscillator=Oscillator(
            frequency=resonator_interm_freq,
            modulation_type=ModulationType.HARDWARE,  # for readout signals being sent from instrument
        ),  # is constant, with the baseband IF being re-calibrated after experiment
        local_oscillator=Oscillator(
            frequency=resonator_lo_freq
        ),  # both input and output should be same float value
        range=qubit.measure.reference_magnitude.dBm(),
    )

    # set signal calibration and signal map for experiment to qubit mentioned
    exp_qubit_spec_pulsed.set_calibration(exp_calibration)

    # setting signal map using connectivity from the hardware config
    # this is to map the qubit ports to actual instrument ports from which signals
    # are being sent
    connectivity = Connectivity.model_validate(
        quantum_device.hardware_config()["connectivity"]
    )

    graph = connectivity.graph

    edges = graph.edges
    signal_map = {}
    for port, clock in [
        (f"{qubit_name}:res", f"{qubit_name}.ro"),
        (f"{qubit_name}:mw", f"{qubit_name}.01"),
    ]:
        for logical_signal in graph.neighbors(port):
            if (port, logical_signal) in edges and logical_signal.endswith("_output"):
                output_signal = _exp_signal(port, clock, output=True)
                signal_map[output_signal] = logical_signal.replace(":", "/")
            if (logical_signal, port) in edges and logical_signal.endswith("_input"):
                input_signal = _exp_signal(port, clock, input=True)
                signal_map[input_signal] = logical_signal.replace(":", "/")

    exp_qubit_spec_pulsed.set_signal_map(signal_map)

    compiled_instructions["experiment"] = exp_qubit_spec_pulsed
    compiled_instructions["acquisition_config"] = AcquisitionConfig(
        bin_mode=BinMode.AVERAGE,
        acq_protocols={0: "SSBIntegrationComplex"},
        n_acquisitions=num_points,
        acquisition_type=AcquisitionType.SPECTROSCOPY,
    )

    return compiled_instructions


class ParRestorer:
    """
    A context manager to ensure a parameter gets restored to its initial value
    upon exiting the context manager.
    """

    def __init__(self, *param):
        self.params = param
        self.old_value = None

    def __enter__(self):
        # Use deepcopy to properly restore objects that may be modified in-place, like
        # dicts
        self.old_values = [deepcopy(param.get()) for param in self.params]

    def __exit__(self, exc_type, exc_val, exc_tb):
        for param, old_value in zip(self.params, self.old_values):
            param.set(old_value)
