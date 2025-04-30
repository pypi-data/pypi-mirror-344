"""Compilation passes for Zurich Instruments backend."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from uuid import uuid4
import numpy as np
import pandas as pd
from quantify_scheduler.enums import BinMode
from laboneq.dsl.calibration import (
    Calibration,
    Oscillator,
    SignalCalibration,
)
from laboneq.dsl.enums import AcquisitionType, AveragingMode, ModulationType
from laboneq.dsl.experiment import (
    Acquire,
    Experiment,
    ExperimentSignal,
    Operation,
    PlayPulse,
    Section,
    pulse_library,
)
from quantify_scheduler.backends.types.common import ModulationFrequencies
from quantify_scheduler.helpers.schedule import _extract_port_clocks_used
from quantify_scheduler.helpers.waveforms import exec_waveform_function
from quantify_scheduler.operations.gate_library import Measure
from quantify_scheduler.schedules.schedule import Schedule, Schedulable
from quantify_scheduler.operations.control_flow_library import ControlFlowOperation
from quantify_zurich_instruments.datastructures import AcquisitionConfig

if TYPE_CHECKING:
    from quantify_scheduler.backends.graph_compilation import CompilationConfig
import warnings


@dataclass
class LabOneQOp:
    """A list of LabOne Q operations and sections for a Quantify operation."""

    name: str
    play_ops: list[Operation | Section] = field(default_factory=list)
    acquire_ops: list[Operation | Section] = field(default_factory=list)


class LabOneQNullOp:
    """A null operation placeholder."""


class IntegrationKernelCache:
    """A cache for LabOne Q integration kernels."""

    # Integration kernels need to be the same for a particular
    # acquisition line. The LabOne Q compiler can't easily check
    # if two kernels are the same, so we need to ensure that we
    # use the same pulse objects each time. This requires caching
    # the pulse objects, hence the need for this class

    def __init__(self):
        self.kernels = {}

    def __contains__(self, exp_signal):
        """Return True if cached kernels for the signal exist."""
        return exp_signal in self.kernels

    def __getitem__(self, exp_signal):
        """Return the cached kernels for the signal."""
        return self.kernels[exp_signal]

    def __setitem__(self, exp_signal, kernels):
        """Store kernels in the cache."""
        # make a copy of the stored list so that its not mutated
        # if the supplied list is modified:
        self.kernels[exp_signal] = list(kernels)

    def assert_equal(self, exp_signal, new_kernels):
        """Assert that the given kernels match those in the cache."""
        old_kernels = self.kernels[exp_signal]
        assert len(old_kernels) == len(new_kernels)
        for k1, k2 in zip(old_kernels, new_kernels):
            assert (
                k1.function == k2.function
                and k1.amplitude == k2.amplitude
                and k1.length == k2.length
                and k1.can_compress == k2.can_compress
                and k1.pulse_parameters == k2.pulse_parameters
            )


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


class CompiledInstructions:
    """Access to the schedule instruction section for a given config."""

    def __init__(self, schedule, config, initialize=False):
        self._section_name = self._device_setup_name(config)
        if initialize:
            schedule["compiled_instructions"][self._section_name] = {}
        self._section = schedule["compiled_instructions"][self._section_name]

    def __getitem__(self, name):
        """Retrieve an item from the section."""
        return self._section[name]

    def __setitem__(self, name, value):
        """Set an item in the section."""
        self._section[name] = value

    def _device_setup_name(self, config: CompilationConfig) -> str:
        """Return the name of the device setup."""
        assert config.hardware_compilation_config is not None

        device_setup_names = [
            key
            for key, value in config.hardware_compilation_config.hardware_description.items()
            if value.instrument_type == "ZIDeviceSetup"
        ]
        assert len(device_setup_names) == 1
        return device_setup_names[0]


def _resolve_modulation_frequencies(
    rf_freq: float | None, interm_freq: float | None, lo_freq: float | None
) -> ModulationFrequencies:
    """Resolve the modulation frequencies using IF + LO = RF."""
    if rf_freq is not None and np.isnan(rf_freq):
        rf_freq = None
    # Calculate the modulation frequencies:
    if rf_freq is not None:
        if interm_freq is None and lo_freq is None:
            raise ValueError(
                f"Modulation frequencies underconstrained."
                f" At least two of the modulation frequencies {interm_freq=},"
                f" {lo_freq=}, and {rf_freq=} should be specified."
            )
        elif interm_freq is None and lo_freq is not None:
            interm_freq = rf_freq - lo_freq
        elif interm_freq is not None and lo_freq is None:
            lo_freq = rf_freq - interm_freq
        elif (
            interm_freq is not None
            and lo_freq is not None
            and interm_freq + lo_freq != rf_freq
        ):
            raise ValueError(
                f"Modulation frequencies overconstrained for clock"
                f" with frequency {rf_freq}. Modulation frequencies"
                f" {interm_freq=} and {lo_freq=} should follow the"
                f" relation IF + LO = RF."
            )
    else:
        if interm_freq is None or lo_freq is None:
            raise ValueError(
                f"Modulation frequencies underconstrained."
                f" At least two of the modulation frequencies {interm_freq=},"
                f" {lo_freq=}, and {rf_freq=} should be specified."
            )
        rf_freq = interm_freq + lo_freq

    return ModulationFrequencies(
        interm_freq=interm_freq,
        lo_freq=lo_freq,
    )


@pulse_library.register_pulse_functional
def quantify_pulse(x, pulse_info, length=None, **_):
    """Create a Quantify waveform pulse.

    Arguments
    ---------
        pulse_info (dict):
            The pulse information describing the pulse. This
            will be passed to ``exec_waveform_function``.
        **_ (Any):
            All pulses accept the following keyword arguments:
            - uid ([str][]): Unique identifier of the pulse
            - length ([float][]): Length of the pulse in seconds
            - amplitude ([float][]): Amplitude of the pulse

    Returns
    -------
        pulse (Pulse): Gaussian pulse.
    """
    # The x values received from the LabOne Q compiler run from
    # -1.0 to (1.0 - one sample), so we need to translate and
    # rescale them here to create a list of times for Quantify's
    # waveform functions:
    t = (x + 1.0) * (length / 2)
    wave = exec_waveform_function(pulse_info["wf_func"], t, pulse_info)
    return wave


def _translate_pulse_info(pulse_info, output=False, input=False):
    """Translate a play pulse_info to a LabOne Q operation."""
    assert pulse_info["wf_func"] is not None
    assert pulse_info["port"] is not None
    assert pulse_info["clock"] is not None
    # assert pulse_info["t0"] == 0
    exp_signal = _exp_signal(
        pulse_info["port"],
        pulse_info["clock"],
        output=output,
        input=input,
    )
    # Note: amplitude and phase are, in Quantify, taken care of by
    #       the waveform itself. The LabOne Q amplitude and phase
    #       could in future be used to support sweeping these
    #       parameters.
    return PlayPulse(
        signal=exp_signal,
        amplitude=None,
        phase=None,
        length=pulse_info["duration"],
        pulse=quantify_pulse(
            length=pulse_info["duration"],
            pulse_info=pulse_info,
        ),
    )


def _translate_acquisition_kernel(acquire_info, input=False, output=False):
    """Translate a play pulse_info to a LabOne Q operation."""
    duration_list = []
    amp_list = 0
    if not len(acquire_info["waveforms"]) <= 2:
        raise ValueError(
            "The acquisition is expected to have a real and imaginary waveform."
        )
    for pulse_info in acquire_info["waveforms"]:
        duration_list.append(pulse_info["duration"])
        amp_list += pulse_info["amp"]
    if not all(duration == duration_list[0] for duration in duration_list):
        raise ValueError("All pulses in the acquisition must have the same duration.")

    pulse_info = acquire_info["waveforms"][0]
    pulse_info["amp"] = amp_list
    if pulse_info["amp"] != 0:
        pulse_info["amp"] = pulse_info["amp"] / abs(pulse_info["amp"])
    else:
        pulse_info["amp"] = 0
    assert pulse_info["wf_func"] is not None
    assert pulse_info["port"] is not None
    assert pulse_info["clock"] is not None

    exp_signal = _exp_signal(
        pulse_info["port"],
        pulse_info["clock"],
        output=output,
        input=input,
    )

    # Note: amplitude and phase are, in Quantify, taken care of by
    #       the waveform itself. The LabOne Q amplitude and phase
    #       could in future be used to support sweeping these
    #       parameters.
    return PlayPulse(
        signal=exp_signal,
        amplitude=None,
        phase=None,
        length=pulse_info["duration"],
        pulse=quantify_pulse(
            length=pulse_info["duration"],
            pulse_info=pulse_info,
        ),
    )


def _translate_acquistion_info(acquire_info, kernel_cache):
    """Translate a measure operation into a LabOne Q section."""
    assert acquire_info["port"] is not None
    assert acquire_info["clock"] is not None
    assert acquire_info["protocol"] in ["SSBIntegrationComplex", "Trace"]

    exp_signal = _exp_signal(
        acquire_info["port"],
        acquire_info["clock"],
        input=True,
    )
    if len(acquire_info["waveforms"]) >= 1:
        kernels = [_translate_acquisition_kernel(acquire_info, input=True).pulse]
    else:
        kernels = []

    if exp_signal in kernel_cache:
        kernel_cache.assert_equal(exp_signal, kernels)
        kernels = kernel_cache[exp_signal]
    else:
        kernel_cache[exp_signal] = kernels

    return Acquire(
        signal=exp_signal,
        handle=f"ACQ_CHANNEL_{acquire_info['acq_channel']}",
        kernel=kernels,
        length=acquire_info["duration"],
    )


def flatten_schedule(
    schedule: Schedule,
    config: CompilationConfig,
) -> Schedule:
    """
    Recursively flatten subschedules based on the absolute timing.

    Parameters
    ----------
    schedule : Schedule
        schedule to be flattened
    config : CompilationConfig
        Compilation config for
        :class:`~quantify_scheduler.backends.graph_compilation.QuantifyCompiler`,
        which is currently not only used to detect if the function is called directly.
        by default None

    Returns
    -------
    Schedule
        Equivalent schedule without subschedules
    """

    def _insert_op_at_time(
        schedule: Schedule, operation: Operation, abs_time: float
    ) -> None:
        new_key = str(uuid4())
        new_schedulable = Schedulable(
            name=new_key,
            operation_id=operation.hash,
        )
        # Timing constraints in the new schedulable are meaningless, so remove the list
        new_schedulable["timing_constraints"] = None
        new_schedulable["abs_time"] = abs_time
        schedule["operation_dict"][operation.hash] = operation
        schedule["schedulables"][new_key] = new_schedulable

    def _move_to_end(ordered_dict: dict, key: Any) -> None:  # noqa: ANN401
        """
        Moves the element with ``key`` to the end of the dict.

        Note: dictionaries from Python 3.7 are ordered.
        """
        value = ordered_dict.pop(key)
        ordered_dict[key] = value

    all_resources = dict(schedule.resources)
    for op in schedule.operations.values():
        if isinstance(op, Schedule):
            flatten_schedule(op, config)
            all_resources.update(op.resources)

    op_keys_to_pop = set()
    schedulable_keys_to_pop = set()
    # we cannot use .items() directly since we modify schedule.schedulables in the loop
    schedulable_iter = tuple(schedule.schedulables.items())
    for schedulable_key, schedulable in schedulable_iter:
        op_key = schedulable["operation_id"]
        op = schedule.operations[op_key]
        if isinstance(op, Schedule):
            offset = schedulable["abs_time"]

            # insert new schedulables shifted by the correct offset
            for inner_schedulable in op.schedulables.values():
                inner_op = op.operations[inner_schedulable["operation_id"]]
                _insert_op_at_time(
                    schedule, inner_op, inner_schedulable["abs_time"] + offset
                )

            # mark the inner schedule for removal from the parent
            op_keys_to_pop.add(op_key)
            schedulable_keys_to_pop.add(schedulable_key)
        else:
            _move_to_end(schedule.schedulables, schedulable_key)

    for key in op_keys_to_pop:
        schedule["operation_dict"].pop(key)
    for key in schedulable_keys_to_pop:
        schedule["schedulables"].pop(key)

    for resource in all_resources.values():
        if resource.name not in schedule.resources:
            schedule.add_resource(resource)

    return schedule


def initialize_compiled_instructions(
    schedule: Schedule, config: CompilationConfig
) -> Schedule:
    """Initialize the compiled instructions dictionary."""
    CompiledInstructions(schedule, config, initialize=True)
    return schedule


def compile_experiment_signals(
    schedule: Schedule, config: CompilationConfig
) -> Schedule:
    """Generate the experiment signals required by the schedule."""
    compiled_instructions = CompiledInstructions(schedule, config)
    compiled_instructions["experiment_signals"] = experiment_signals = []
    compiled_instructions["signal_map"] = signal_map = {}

    graph = config.hardware_compilation_config.connectivity.graph
    # TODO: replace with directed edges and remove hacky .endswith() checks
    #       on the logical signal names below.
    edges = graph.edges

    for port, clock in _extract_port_clocks_used(schedule):
        for logical_signal in graph.neighbors(port):
            if (port, logical_signal) in edges and logical_signal.endswith("_output"):
                output_signal = _exp_signal(port, clock, output=True)
                experiment_signals.append(ExperimentSignal(output_signal))
                signal_map[output_signal] = logical_signal.replace(":", "/")
            if (logical_signal, port) in edges and logical_signal.endswith("_input"):
                input_signal = _exp_signal(port, clock, input=True)
                experiment_signals.append(ExperimentSignal(input_signal))
                signal_map[input_signal] = logical_signal.replace(":", "/")

    return schedule


def _validate_signal(exp_signal):
    """Validate that the experiment signal is a permissible input."""
    return not (exp_signal.endswith("-input") and "ro" not in exp_signal)


def compile_calibration(schedule: Schedule, config: CompilationConfig) -> Schedule:
    """Generate LabOneQ experiment calibration that sets the port delays, oscillator frequencies and the reference magnitudes."""
    compiled_instructions = CompiledInstructions(schedule, config)
    compiled_instructions["calibration"] = calibration = Calibration()

    # Get mod frequencies from config
    if config.hardware_compilation_config is not None:
        modulation_frequencies = (
            config.hardware_compilation_config.hardware_options.modulation_frequencies
        )
        latency_corrections = (
            config.hardware_compilation_config.hardware_options.latency_corrections
        )

        if modulation_frequencies is not None:
            # Extract unique qubits from keys
            qubits = set(key.split(":")[0] for key in modulation_frequencies)

            for qubit in qubits:
                if (
                    any(
                        key.startswith(f"{qubit}:") and key.endswith("ro-output")
                        for key in modulation_frequencies
                    )
                ) or (
                    any(
                        key.startswith(f"{qubit}:") and key.endswith("ro-input")
                        for key in modulation_frequencies
                    )
                ):
                    assert any(
                        key.startswith(f"{qubit}:") and key.endswith("ro-output")
                        for key in modulation_frequencies
                    ) and any(
                        key.startswith(f"{qubit}:") and key.endswith("ro-input")
                        for key in modulation_frequencies
                    ), f"Both ro-output and ro-input modulation frequencies must be set for {qubit} in the config."
        else:
            modulation_frequencies = None
            raise ValueError("No modulation frequencies found in the config.")

    else:
        latency_corrections = None
        raise ValueError("No hardware compilation config found.")

    # Here we want to implement the port_delay parameter which sets a delay on all
    # signals that play on a specific port. This delay will not be shown in the
    # pulse sheet viewer nor in the schedule since it serves to calibrate timings
    # of signals with respect to the schedule. In the current implementation
    # negative port delays are allowed and will be compiled to positive delays
    # on the hardware where all relative delays are corrected. The caveat is that
    # the hardware adds up the delay of QA out onto the delay of QA in. This is
    # also handeled in our compilation but the workaround does not work in the
    # case where QA in - QA out < 0 because it will then compile a negative
    # (unsupported by ZI) port delay onto the QA in channel.

    port_delays = {}
    # Get mod frequencies for each port clock combos
    for port, clock in _extract_port_clocks_used(schedule):
        # TODO: This adds a signal calibration for every
        #       combination of port, clock, and output / input.
        #       This should be limited to valid experiment signals.

        for exp_signal in [
            _exp_signal(port, clock, output=True),
            _exp_signal(port, clock, input=True),
        ]:
            if not _validate_signal(exp_signal):
                continue
            if (
                latency_corrections is not None
                and exp_signal in compiled_instructions["signal_map"]
            ):
                port_delays[compiled_instructions["signal_map"][exp_signal]] = (
                    latency_corrections.get(exp_signal)
                )
    if port_delays:
        # Replace all None values with 0 in port_delays
        port_delays = {
            key: (0 if value is None else value) for key, value in port_delays.items()
        }
        # Find the minimum value in port_delays
        min_value = min(port_delays.values())
        # If the minimum value is negative, add its absolute value to all values in port_delays
        # now all relative delays are the same but they are all positive.
        if min_value < 0:
            for key in port_delays:
                port_delays[key] += abs(min_value)
        # Make sure all keys are lowercase and check for qachannels and input as well as qachannels and output
        # Check if any key in port_delays contains 'qachannels' and 'input'
        key_input = None
        for key_in in port_delays:
            lower_key = key_in.lower()
            if "qachannels" in lower_key and "input" in lower_key:
                key_input = key_in
        key_output = None
        for key_out in port_delays:
            lower_key = key_out.lower()
            if "qachannels" in lower_key and "output" in lower_key:
                key_output = key_out
        # The port delay for the QA input channel should be the
        port_delays[key_input] = port_delays[key_input] - port_delays[key_output]
        if port_delays[key_input] < 0:
            raise ValueError(
                "Port delay for QA input minus QA output should be positive."
            )

    # Continue by setting the new values from the port_delay to the calibration
    for port, clock in _extract_port_clocks_used(schedule):
        for exp_signal in [
            _exp_signal(port, clock, output=True),
            _exp_signal(port, clock, input=True),
        ]:
            if not _validate_signal(exp_signal):
                continue
            signal_cal = SignalCalibration()

            if port_delays and exp_signal in compiled_instructions["signal_map"]:
                # Get latency correction for this port-clock combination
                pc_latency_correction = port_delays.get(
                    compiled_instructions["signal_map"][exp_signal]
                )
                if pc_latency_correction is not None:
                    signal_cal.port_delay = pc_latency_correction

            if modulation_frequencies is not None:
                # Get mod frequencies for this port-clock combination
                pc_mod_freqs = modulation_frequencies.get(exp_signal)
                if pc_mod_freqs is None:
                    # No modulation frequencies to set for this port-clock combination
                    continue

                # Resolve mod frequencies based on IF + LO = RF
                resolved_mod_freqs = _resolve_modulation_frequencies(
                    rf_freq=schedule.resources[clock]["freq"],
                    interm_freq=pc_mod_freqs.interm_freq,
                    lo_freq=pc_mod_freqs.lo_freq,
                )

                # Check if the local oscillator frequency is a multiple of
                # 100 MHz, else raise error
                if (
                    resolved_mod_freqs.lo_freq is not None
                    and resolved_mod_freqs.lo_freq % 100e6 != 0
                ):
                    raise ValueError(
                        "Local oscillator frequency must be a multiple of 100 MHz"
                        "as a hardware restriction."
                    )
                if "mw" in port:
                    modulation_type = ModulationType.HARDWARE
                else:
                    modulation_type = ModulationType.SOFTWARE

                # Set resolved mod frequencies in calibration
                signal_cal.oscillator = Oscillator(
                    frequency=resolved_mod_freqs.interm_freq,
                    modulation_type=modulation_type,
                )
                signal_cal.local_oscillator = Oscillator(
                    frequency=resolved_mod_freqs.lo_freq
                )

            # For all the pulses in the schedule, find the port-clock combination and
            # the reference power
            power = None
            pulse_power = []
            operations = 0

            for operation in schedule.operations.values():
                operations += 1
                for pulse in operation["pulse_info"] + operation["acquisition_info"]:
                    if (
                        "reference_magnitude" in pulse
                        and pulse["port"] == port
                        and pulse["clock"] == clock
                    ):
                        if not pulse["reference_magnitude"]:
                            # when the value is not added as a `ReferenceMagnitude` object
                            # when no reference magnitude is found in pulse definition
                            # we skip setting power to instrument
                            warnings.warn(
                                "No reference power set for this operation. "
                                "Skipping this pulse.",
                            )
                            continue

                        ref_power = pulse["reference_magnitude"].value
                        unit = pulse["reference_magnitude"].unit

                        if ref_power is None:
                            # when no reference magnitude is found in pulse definition
                            # we skip setting power to instrument
                            warnings.warn(
                                "No reference power set for this operation. "
                                "Skipping this pulse.",
                            )
                            continue

                        if ref_power and unit != "dBm":
                            raise ValueError(
                                "Reference power should be in dBm. "
                                f"Found {unit} instead."
                            )

                        if ref_power and not isinstance(
                            ref_power, (int, float, np.integer, np.floating)
                        ):
                            raise ValueError(
                                "Reference power should be a number. "
                                f"Found {ref_power} instead."
                            )

                        pulse_power.append(ref_power)

            if not pulse_power:
                signal_cal.range = None
            else:
                power = pulse_power[0]
                for i in np.arange(len(pulse_power)):
                    if pulse_power[i] != power:
                        raise ValueError(
                            "Inconsistent reference powers on channel "
                            f"{port}-{clock}. All pulse reference powers on a given "
                            "channel must be equal."
                        )
                if exp_signal.endswith("-output"):
                    if power is None:
                        signal_cal.range = None
                    elif power % 5 == 0 and -30 <= power <= 10:
                        signal_cal.range = power
                    else:
                        allowed_ranges = [-30, -25, -20, -15, -10, -5, 0, 5, 10]
                        adjusted_power = min(
                            allowed_ranges, key=lambda x: abs(x - power)
                        )
                        signal_cal.range = adjusted_power
                        warnings.warn(
                            "Reference power for output channel must be in the range"
                            " of -30 to 10 dBm with steps of 5 dBm. Nearest allowed"
                            " range will be used.",
                            UserWarning,
                        )

                elif exp_signal.endswith("-input"):
                    if power is None:
                        signal_cal.range = None
                    elif power % 5 == 0 and -50 <= power <= 10:
                        signal_cal.range = 10
                    else:
                        allowed_ranges = [
                            -50,
                            -45,
                            -40,
                            -35,
                            -30,
                            -25,
                            -20,
                            -15,
                            -10,
                            -5,
                            0,
                            5,
                            10,
                        ]
                        adjusted_power = min(
                            allowed_ranges, key=lambda x: abs(x - power)
                        )
                        signal_cal.range = 10
                        warnings.warn(
                            "Reference power for input channel must be in the range"
                            " of -50 to 10 dBm with steps of 5 dBm. Nearest allowed"
                            " range will be used.",
                            UserWarning,
                        )
            calibration[exp_signal] = signal_cal
    return schedule


def compile_operations(schedule: Schedule, config: CompilationConfig) -> Schedule:
    """Generate LabOne Q operations from schedule operations."""
    compiled_instructions = CompiledInstructions(schedule, config)
    compiled_instructions["laboneq_ops"] = l1q_ops = {}

    kernel_cache = IntegrationKernelCache()
    readout_pulse_cache = {}

    for op_id, op in schedule.operations.items():

        l1q_op = l1q_ops[op_id] = LabOneQOp(op["name"])

        if isinstance(op, Schedule):
            raise NotImplementedError(
                "Schedule not flattened, check Schedule definition."
            )
        if not (op.valid_pulse or op.valid_acquisition):
            raise ValueError(f"Unsupported operation: {op!s}")
        if op.valid_pulse:
            for pulse_info in op["pulse_info"]:
                if pulse_info.get("reset_clock_phase"):
                    # TODO: support clock phase reset
                    l1q_op.play_ops.append(LabOneQNullOp())
                elif pulse_info["port"] is None:
                    # Skip pulses that are not assigned to a port, like IdlePulses.
                    # These delays are already encoded in the timing table.
                    # The ResetClockPhase is an exception, that is why we check
                    # for it above.
                    pass
                elif (
                    isinstance(pulse_info["port"], str) and "res" in pulse_info["port"]
                ):
                    if pulse_info["port"] in readout_pulse_cache:
                        warnings.warn(
                            f"Readout port parameters for {pulse_info['port']} already set"
                        )
                        readout_pulse = readout_pulse_cache.get(pulse_info["port"])
                        l1q_op.play_ops.append(readout_pulse)
                    else:
                        readout_pulse = _translate_pulse_info(pulse_info, output=True)
                        # update readout pulse cache for the particular port
                        readout_pulse_cache[pulse_info["port"]] = readout_pulse
                        l1q_op.play_ops.append(readout_pulse)
                else:
                    l1q_op.play_ops.append(
                        _translate_pulse_info(pulse_info, output=True)
                    )
        if op.valid_acquisition:
            assert len(op["acquisition_info"]) == 1
            for acquire_info in op["acquisition_info"]:
                l1q_op.acquire_ops.append(
                    _translate_acquistion_info(acquire_info, kernel_cache)
                )

    return schedule


def compile_acquisition_config(
    schedule: Schedule, config: CompilationConfig
) -> Schedule:
    """Compile the acquisition config required to reshape acquired data in the ICC."""
    compiled_instructions = CompiledInstructions(schedule, config)

    acq_protocols = {}
    bin_mode = None
    for op in schedule.operations.values():
        if op.valid_acquisition:
            acq_info = op.data["acquisition_info"][0]
            acq_protocols[acq_info["acq_channel"]] = acq_info["protocol"]
            if bin_mode is not None and bin_mode != acq_info["bin_mode"]:
                raise ValueError(
                    f"Bin mode mismatch for {op}. All acquisitions in the schedule"
                    f" should have the same bin mode."
                )
            bin_mode = acq_info["bin_mode"]

    # For now, we assume all acquisitions on the same element:
    n_acquisitions = len(
        [
            schedulable
            for schedulable in schedule.schedulables.values()
            if schedule.operations[schedulable["operation_id"]].valid_acquisition
        ]
    )

    # whenever acquisitions run in Append mode, we do not want to average the data.
    # Therefore, we need to set the variable that sets the number of acquisition bins
    # to be n_acquisitions * repetitions

    if bin_mode == BinMode.APPEND:
        n_acquisitions = n_acquisitions * schedule.repetitions

    # Check that all acquisitions have the same protocol and determine the
    # acquisition type:
    for protocol in acq_protocols.values():
        if protocol != acq_protocols[0]:
            raise ValueError(
                f"Acquisition protocol mismatch for {op}. All acquisitions in the"
                f" schedule should have the same protocol."
            )
    if not acq_protocols:
        # Use the default acquisition type if no acquisitions are present:
        acquisition_type = AcquisitionType.INTEGRATION
    elif acq_protocols[0] == "Trace":
        acquisition_type = AcquisitionType.RAW
    elif acq_protocols[0] == "SSBIntegrationComplex":
        acquisition_type = AcquisitionType.INTEGRATION
    else:
        raise ValueError(f"Unsupported acquisition protocol: {acq_protocols[0]}")

    acquisition_config = AcquisitionConfig(
        bin_mode=bin_mode,
        acq_protocols=acq_protocols,
        n_acquisitions=n_acquisitions,
        acquisition_type=acquisition_type,
    )

    compiled_instructions["acquisition_config"] = acquisition_config
    return schedule


def snap_timing_to_system_grid(
    schedule: Schedule, config: CompilationConfig
) -> Schedule:
    """Snap the absolute times in the schedule to the 8 ns system timing grid.

    LabOneQ compiler aligns Sections based on the system or signal timing grid.
    Sections containing an acquisition are aligned to the system grid, whereas
    the other sections are aligned to the finer signal grid. This leads to weird
    timing issues since the pulse sheet does not conform to the timing table anymore.
    This function prevents that by ensuring timings are snapped to the system grid.

    We will assume that there is a reset at the start of a schedule and that we
    have freedom with respect to lengthening the time of the reset operation.
    We iterate over all operations up to the first acquisition which will be
    snapped to the grid by adding some time to the reset operation effectively
    shifting the rest of the operations in time. We then move on to the next set
    of operations up to the next acquisition and so forth.
    """
    # TODO: Use the correct system timing grid based on the hardware used.
    # SHFQC has a system grid of 8 ns. For the rules see:
    # https://docs.zhinst.com/labone_q_user_manual/concepts/sections_and_pulses/timing_rules/#rules

    def adjust_time(df: pd.DataFrame, system_grid: float = 8e-9):
        last_acquisition_index = -1
        i = 0
        while i < len(df):
            row = df.iloc[i]
            if row["is_acquisition"]:
                time = round(row["abs_time"] + row["duration"], 10)
                remainder = round(time % system_grid, 10) % system_grid
                if not math.isclose(remainder, 0, abs_tol=1e-10):
                    adjustment = round(system_grid - remainder, 10)
                    df.loc[last_acquisition_index + 1 :, "abs_time"] += adjustment

                last_acquisition_index = i
            i += 1
        df["abs_time"] = df["abs_time"].map(lambda x: round(x, 10))
        return df

    adjusted_timing = adjust_time(schedule.timing_table.data.sort_index())
    schedule._hardware_timing_table = adjusted_timing
    return schedule


def _find_pair(indexed_dict, current_key):
    """Find the previous key in the dictionary that has the same port clock combo.

    Used for finding pairs of measure and acquisition pulses on the QA input and output
    channels. Making pairs with opposite output and input channel.
    """
    current_base = indexed_dict[current_key].rsplit("-", 1)[0]
    current_direction = indexed_dict[current_key].rsplit("-", 1)[1]
    for key in reversed(list(indexed_dict.keys())):
        if key == current_key:
            continue
        base = indexed_dict[key].rsplit("-", 1)[0]
        direction = indexed_dict[key].rsplit("-", 1)[1]
        # check if the signal is on the same port and clock but one is
        # output (measurement pulse) and the other is input (acquisition pulse)
        if current_base == base and current_direction != direction:
            return key, indexed_dict[key]
    return None, None


def compile_experiment(schedule: Schedule, config: CompilationConfig) -> Schedule:
    """Compile a Schedule to a LabOne Q Experiment."""
    compiled_instructions = CompiledInstructions(schedule, config)
    timing_table = schedule._hardware_timing_table
    experiment_signals = compiled_instructions["experiment_signals"]
    signal_map = compiled_instructions["signal_map"]
    calibration = compiled_instructions["calibration"]
    laboneq_ops = compiled_instructions["laboneq_ops"]
    acquisition_config = compiled_instructions["acquisition_config"]

    binmode = acquisition_config.bin_mode

    compiled_instructions["experiment"] = experiment = Experiment(
        uid=schedule.name,
        signals=experiment_signals,
    )

    sections = {signal.uid: Section(uid=signal.uid) for signal in experiment_signals}

    previous_times = {signal.uid: 0.0 for signal in experiment_signals}

    averaging_mode = (
        AveragingMode.SINGLE_SHOT if binmode == BinMode.APPEND else AveragingMode.CYCLIC
    )
    with experiment.acquire_loop_rt(
        uid="shots",
        count=schedule.repetitions,
        acquisition_type=acquisition_config.acquisition_type,
        averaging_mode=averaging_mode,
    ):
        for section in sections.values():
            experiment.add(section)
    pulse_acquire_pairs = {}
    op_sections = {}
    for i, row in timing_table.sort_index().iterrows():
        if row["port"] is None:
            continue
        acq_delay = 0.0
        row_ops = laboneq_ops[row["operation_hash"]]

        if row["is_acquisition"]:
            signal = _exp_signal(row["port"], row["clock"], input=True)
            op = row_ops.acquire_ops[row["wf_idx"]]
        else:
            signal = _exp_signal(row["port"], row["clock"], output=True)
            op = row_ops.play_ops[row["wf_idx"]]

        # We wrap each operation in its own section in order to
        # simplify the section structure for the LabOne Q compiler.
        # Except for the measure and acquisition which should be in the same section.
        # This happens below where we make a new section only if its not an acquisition
        # except if the acquisition has no accompanying measure pulse or if its the
        # first operation in the timing table.

        delay = round(row["abs_time"] - previous_times[signal], 10)
        # extra_delay = round(getattr(op, "_extra_delay", 0.0), 10)
        # The measurement pulse needs to have the acq_delay added afterwards
        # to ensure the durations of the measure and acquisition match up.
        # Since for the acquisition the acq_delay is already incorporated in
        # the timing table. This is only done if the next operation is an acquisition.

        # We should do a similar thing for any other pulse on the measurement channel.
        # We will make pairs of measure and acquisition pulses for any subsequent pairs
        # of measuren and acquire pulses on the QA input and output channels.

        if "res" in row["port"]:
            pulse_acquire_pairs[i] = signal
            previous_key, signal_pair = _find_pair(pulse_acquire_pairs, i)
            if previous_key is not None and signal_pair is not None:
                pulse_acquire_pairs[i] = f"Pair-{i}"
                pulse_acquire_pairs[previous_key] = f"Pair-{i}"
                op_section = op_sections[f"op_section_{previous_key}"]

                if delay > 0:
                    op_section.delay(signal=signal, time=delay)
                elif delay < 0:
                    raise ValueError(
                        f"Negative delay of {delay!r}s encountered on signal {signal!r}."
                    )
                if isinstance(op, LabOneQNullOp):
                    pass
                elif isinstance(op, Operation):
                    op_section.add(op)
                    previous_times[signal] = round(
                        row["abs_time"] + row["duration"], 10
                    )
                else:
                    raise ValueError(f"Unsupported LabOne Q operation: {op!r}")

                if row["duration"] > timing_table.loc[previous_key, "duration"]:
                    extra_delay = round(
                        row["duration"] - timing_table.loc[previous_key, "duration"], 10
                    )
                    op_section.delay(
                        signal=signal_pair,
                        time=extra_delay,
                    )
                    previous_times[signal_pair] += extra_delay
                elif row["duration"] < timing_table.loc[previous_key, "duration"]:
                    extra_delay = round(
                        timing_table.loc[previous_key, "duration"] - row["duration"], 10
                    )
                    op_section.delay(signal=signal, time=extra_delay)
                    previous_times[signal] += extra_delay
                # acq_delay here is the time between the start of the measure and
                # acquisition pulse also if they are swapped around acquistion
                # first and then measure. This is needed to append to the end of
                # the first pulse to ensure durations match up.
                acq_delay = round(
                    row["abs_time"] - timing_table.loc[previous_key, "abs_time"],
                    10,
                )
                if acq_delay > 0:
                    op_section.delay(signal=signal_pair, time=acq_delay)
                    previous_times[signal_pair] += acq_delay

            elif previous_key is None and signal_pair is None:
                section = sections[signal]
                op_sections[f"op_section_{i}"] = Section()
                op_section = op_sections[f"op_section_{i}"]
                section.add(op_section)

                if delay > 0:
                    op_section.delay(signal=signal, time=delay)
                elif delay < 0:
                    raise ValueError(
                        f"Negative delay of {delay!r}s encountered on signal {signal!r}."
                    )
                if isinstance(op, LabOneQNullOp):
                    pass
                elif isinstance(op, Operation):
                    op_section.add(op)
                else:
                    raise ValueError(f"Unsupported LabOne Q operation: {op!r}")

                previous_times[signal] = round(
                    (row["abs_time"] + row["duration"]),
                    10,
                )

        else:
            section = sections[signal]
            op_section = Section()
            section.add(op_section)
            if delay > 0:
                op_section.delay(signal=signal, time=delay)
            elif delay < 0:
                raise ValueError(
                    f"Negative delay of {delay!r}s encountered on signal {signal!r}."
                )
            if isinstance(op, LabOneQNullOp):
                pass
            elif isinstance(op, Operation):
                op_section.add(op)
            else:
                raise ValueError(f"Unsupported LabOne Q operation: {op!r}")

            previous_times[signal] = round((row["abs_time"] + row["duration"]), 10)
    experiment.set_signal_map(signal_map)
    experiment.set_calibration(calibration)

    return schedule
