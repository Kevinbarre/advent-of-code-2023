from collections import deque

import pytest

from main import part1, Module, Signal, Broadcaster, FlipFlop, State, Conjunction, parse_modules, push_button, \
    count_pulses, push_button_rx, count_min_rx_naive, count_steps_high

filename = "example.txt"


@pytest.mark.parametrize("test_input, expected", [(filename, 32000000), ("example2.txt", 11687500)])
def test_part1(test_input, expected):
    # Given
    with open(test_input) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == expected


def test_part2():
    # No tests here, because examples files do not have rx
    assert True


@pytest.mark.parametrize("test_input", [Signal.LOW, Signal.HIGH])
def test_module_send_signal(test_input):
    # Given
    signal_queue = deque()
    destination_module_1 = Module("destination_module_1", signal_queue)
    destination_module_2 = Module("destination_module_2", signal_queue)
    source_module = Module("source_module", signal_queue)
    source_module.init_destination_modules(destination_module_1, destination_module_2)
    # When
    source_module.send_signal(test_input)
    # Then
    assert signal_queue == deque(
        [(source_module, test_input, destination_module_1), (source_module, test_input, destination_module_2)])


@pytest.mark.parametrize("test_input", [Signal.LOW, Signal.HIGH])
def test_broadcaster_receive_signal(test_input):
    # Given
    signal_queue = deque()
    destination_module_1 = Module("destination_module_1", signal_queue)
    destination_module_2 = Module("destination_module_2", signal_queue)
    broadcaster = Broadcaster("broadcaster", signal_queue)
    broadcaster.init_destination_modules(destination_module_1, destination_module_2)
    # When
    broadcaster.receive_signal(None, test_input)
    # Then
    assert signal_queue == deque(
        [(broadcaster, test_input, destination_module_1), (broadcaster, test_input, destination_module_2)])


def test_flipflop_receive_signal_high():
    # Given
    signal_queue = deque()
    destination_module_1 = Module("destination_module_1", signal_queue)
    destination_module_2 = Module("destination_module_2", signal_queue)
    flipflop = FlipFlop("flipflop", signal_queue)
    flipflop.init_destination_modules(destination_module_1, destination_module_2)
    # Default flipflop state should be OFF
    assert flipflop.state == State.OFF
    # When
    flipflop.receive_signal(None, Signal.HIGH)
    # Then
    # No state change
    assert flipflop.state == State.OFF
    # No new signal
    assert signal_queue == deque()


@pytest.mark.parametrize("test_input, expected", [(State.OFF, Signal.HIGH), (State.ON, Signal.LOW)])
def test_flipflop_receive_signal_low(test_input, expected):
    # Given
    signal_queue = deque()
    destination_module_1 = Module("destination_module_1", signal_queue)
    destination_module_2 = Module("destination_module_2", signal_queue)
    flipflop = FlipFlop("flipflop", signal_queue)
    flipflop.init_destination_modules(destination_module_1, destination_module_2)
    # Force current flipflop state
    flipflop.state = test_input
    # When
    flipflop.receive_signal(None, Signal.LOW)
    # Then
    # State change
    assert flipflop.state == (~test_input)
    # No new signal
    assert signal_queue == deque(
        [(flipflop, expected, destination_module_1), (flipflop, expected, destination_module_2)])


def test_conjunction_default_state_low():
    # Given
    input_module_1 = Module("input_module_1", None)
    input_module_2 = Module("input_module_2", None)
    destination_module_1 = Module("destination_module_1", None)
    destination_module_2 = Module("destination_module_2", None)
    # When
    conjunction = Conjunction("conjunction", None)
    conjunction.init_input_modules(input_module_1, input_module_2)
    conjunction.init_destination_modules(destination_module_1, destination_module_2)
    # Then
    assert conjunction._remembered_pulses == {input_module_1: Signal.LOW, input_module_2: Signal.LOW}


@pytest.mark.parametrize("remembered_pulse_1, remembered_pulse_2, expected", [(Signal.LOW, Signal.LOW, Signal.HIGH),
                                                                              (Signal.HIGH, Signal.LOW, Signal.HIGH),
                                                                              (Signal.LOW, Signal.HIGH, Signal.LOW),
                                                                              (Signal.HIGH, Signal.HIGH, Signal.LOW)])
def test_conjunction_receive_signal(remembered_pulse_1, remembered_pulse_2, expected):
    # Given
    signal_queue = deque()
    input_module_1 = Module("input_module_1", None)
    input_module_2 = Module("input_module_2", None)
    destination_module = Module("destination_module", signal_queue)
    conjunction = Conjunction("conjunction", signal_queue)
    conjunction.init_input_modules(input_module_1, input_module_2)
    conjunction.init_destination_modules(destination_module)
    # Force previously remembered states
    conjunction._remembered_pulses = {input_module_1: remembered_pulse_1, input_module_2: remembered_pulse_2}
    # When
    conjunction.receive_signal(input_module_1, Signal.HIGH)
    # Then
    assert signal_queue == deque([(conjunction, expected, destination_module)])


def test_parse_modules():
    # Given
    lines = ["broadcaster -> a, b, c",
             "%a -> b",
             "%b -> c",
             "%c -> inv",
             "&inv -> a"]
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    modules, flipflops = parse_modules(lines)
    # Then
    assert modules.keys() == {"broadcaster", "a", "b", "c", "inv"}
    result_broadcaster = modules["broadcaster"]
    assert result_broadcaster == broadcaster
    assert result_broadcaster._destination_modules == [a, b, c]
    result_a = modules["a"]
    assert result_a._destination_modules == [b]
    result_b = modules["b"]
    assert result_b._destination_modules == [c]
    result_c = modules["c"]
    assert result_c._destination_modules == [inv]
    result_inv = modules["inv"]
    assert result_inv._remembered_pulses == {c: Signal.LOW}
    assert result_inv._destination_modules == [a]
    assert flipflops == {a, b, c}


def test_push_button():
    # Given
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    low_pulses, high_pulses = push_button(broadcaster)
    # Then
    assert low_pulses == 8
    assert high_pulses == 4


@pytest.mark.parametrize("test_input, expected", [(1, 32), (1000, 32000000)])
def test_count_pulses(test_input, expected):
    # Given
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    result = count_pulses(test_input, broadcaster)
    # Then
    assert result == expected


def test_push_button_rx():
    # Given
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    rx = Module("rx", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c, rx)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    result = push_button_rx(broadcaster)
    # Then
    assert result == 1


def test_count_min_rx():
    # Given
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    rx = Module("rx", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c, rx)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    result = count_min_rx_naive(broadcaster)
    # Then
    assert result == 1


def test_count_steps_high():
    # Given
    signal_queue = deque()
    broadcaster = Broadcaster("broadcaster", signal_queue)
    a = FlipFlop("a", signal_queue)
    b = FlipFlop("b", signal_queue)
    c = FlipFlop("c", signal_queue)
    rx = Module("rx", signal_queue)
    inv = Conjunction("inv", signal_queue)
    broadcaster.init_destination_modules(a, b, c, rx)
    a.init_destination_modules(b)
    b.init_destination_modules(c)
    c.init_destination_modules(inv)
    inv.init_input_modules(c)
    inv.init_destination_modules(a)
    # When
    result = count_steps_high(broadcaster, "a")
    # Then
    assert result == 1
