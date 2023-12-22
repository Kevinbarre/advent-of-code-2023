from collections import deque
from enum import Enum, Flag


def part1(lines):
    modules, flipflops = parse_modules(lines)
    broadcaster = modules["broadcaster"]
    return count_pulses(1000, broadcaster)


def part2(lines):
    return count_min_rx(lines)


class Signal(Enum):
    LOW = 0
    HIGH = 1


class State(Flag):
    OFF = False
    ON = True


class Module:
    def __init__(self, name, signal_queue):
        self._destination_modules = []
        self.name = name
        self.signal_queue = signal_queue

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "%s(name=%r)" % (type(self).__name__, self.name)

    def receive_signal(self, input_module, signal):
        pass

    def init_destination_modules(self, *destination_modules):
        self._destination_modules.extend(destination_modules)

    def send_signal(self, signal):
        for module in self._destination_modules:
            self.signal_queue.append((self, signal, module))


class Broadcaster(Module):
    def receive_signal(self, input_module, signal):
        # Propagate signal to all modules
        self.send_signal(signal)


class FlipFlop(Module):
    def __init__(self, name, signal_queue):
        super().__init__(name, signal_queue)
        self.state = State.OFF

    def __repr__(self):
        return "FlipFlop(name=%r, state=%r)" % (self.name, self.state)

    def receive_signal(self, input_module, signal):
        if signal == Signal.HIGH:
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens
            pass
        else:  # Low pulse
            # Signal to send depends on current state
            signal_to_send = Signal.HIGH if self.state == State.OFF else Signal.LOW
            # Flips between on and off (invert operator)
            self.state = ~self.state
            # Send signal depending on previous state
            self.send_signal(signal_to_send)


class Conjunction(Module):
    def __init__(self, name, signal_queue):
        super().__init__(name, signal_queue)
        self._remembered_pulses = {}

    def __repr__(self):
        return "Conjunction(name=%r, remembered_pulses=%r)" % (self.name, self._remembered_pulses)

    def init_input_modules(self, *input_modules):
        self._remembered_pulses.update({input_module: Signal.LOW for input_module in input_modules})

    def receive_signal(self, input_module, signal):
        # First update remembered pulse of received input
        self._remembered_pulses[input_module] = signal
        # Send a low pulse only if all remembered inputs are HIGH, otherwise send high pulse
        signal_to_send = Signal.LOW if all(
            remembered_pulse == Signal.HIGH for remembered_pulse in self._remembered_pulses.values()) else Signal.HIGH
        self.send_signal(signal_to_send)


def parse_modules(lines):
    modules = {}
    signal_queue = deque()
    flipflops = set()
    conjunctions = []
    # First iteration to create modules
    for line in lines:
        name, _ = line.split(" -> ")
        if name.startswith('%'):
            name = name[1:]
            flipflop = FlipFlop(name, signal_queue)
            modules[name] = flipflop
            flipflops.add(flipflop)
        elif name.startswith('&'):
            name = name[1:]
            conjunction = Conjunction(name, signal_queue)
            modules[name] = conjunction
            conjunctions.append(conjunction)  # Remember conjunction for initializing input modules later
        else:  # broadcaster
            modules[name] = Broadcaster(name, signal_queue)
    # Second iteration to initialize input and destination modules
    for line in lines:
        name, destination_modules = line.split(" -> ")
        try:
            module = modules[name]
        except KeyError:
            # Name starts with a % or a &
            module = modules[name[1:]]
        for destination_module in destination_modules.split(", "):
            if destination_module not in modules:
                # Case for the example output that is only a destination module. Add it as a simple module
                modules[destination_module] = Module(destination_module, signal_queue)
            module.init_destination_modules(modules[destination_module])
        # For conjunctions, need to initialize input modules
        if name.startswith('&'):
            _initialize_input_modules(module, lines, modules)
    return modules, flipflops


def _initialize_input_modules(conjunction, lines, modules):
    input_modules = []
    for line in lines:
        name, destination_modules = line.split(" -> ")
        destination_modules = destination_modules.split(", ")
        if conjunction.name in destination_modules:
            # Found a module that has conjunction as destination, remember it as input
            if name[0] in ('%', '&'):
                name = name[1:]
            input_modules.append(name)
    conjunction.init_input_modules(*[modules[input_module_name] for input_module_name in input_modules])


def push_button(broadcaster):
    signal_queue = broadcaster.signal_queue
    # Push button to send low signal to broadcaster
    broadcaster.send_signal(Signal.LOW)
    low_pulses, high_pulses = 1, 0  # Account for first low signal sent to broadcaster
    while signal_queue:
        input_module, signal, destination_module = signal_queue.popleft()
        destination_module.receive_signal(input_module, signal)
        if signal == Signal.LOW:
            low_pulses += 1
        else:  # Signal.HIGH
            high_pulses += 1
    return low_pulses, high_pulses


def count_pulses(nb_cycles, broadcaster):
    total_low = 0
    total_high = 0
    for i in range(nb_cycles):
        low_pulses, high_pulses = push_button(broadcaster)
        total_low += low_pulses
        total_high += high_pulses
    return total_low * total_high


def push_button_rx(broadcaster):
    signal_queue = broadcaster.signal_queue
    # Push button to send low signal to broadcaster
    broadcaster.send_signal(Signal.LOW)
    count_low_rx = 0
    while signal_queue:
        input_module, signal, destination_module = signal_queue.popleft()
        destination_module.receive_signal(input_module, signal)
        if signal == Signal.LOW and destination_module.name == "rx":
            count_low_rx += 1
    return count_low_rx


def count_min_rx_naive(broadcaster):
    nb_push_button = 1  # Account for first button pushed
    while push_button_rx(broadcaster) != 1:
        nb_push_button += 1
    return nb_push_button


def count_steps_high(broadcaster, target):
    signal_queue = broadcaster.signal_queue
    steps = 0
    while True:
        # Push button to send low signal to broadcaster
        broadcaster.send_signal(Signal.LOW)
        steps += 1
        while signal_queue:
            input_module, signal, destination_module = signal_queue.popleft()
            destination_module.receive_signal(input_module, signal)
            if signal == Signal.HIGH and input_module.name == target:
                return steps


def reset_modules(lines):
    modules, flipflops = parse_modules(lines)
    return modules["broadcaster"]


# rx comes from conjunction qn
# qn has the following input: qz, cq, jx, tt
def count_min_rx(lines):
    # Steps to get qz high
    broadcaster = reset_modules(lines)
    steps_qz = count_steps_high(broadcaster, "qz")
    # Steps to get cq high
    broadcaster = reset_modules(lines)
    steps_cq = count_steps_high(broadcaster, "cq")
    # Steps to get jx high
    broadcaster = reset_modules(lines)
    steps_jx = count_steps_high(broadcaster, "jx")
    # Steps to get tt high
    broadcaster = reset_modules(lines)
    steps_tt = count_steps_high(broadcaster, "tt")
    return steps_qz * steps_cq * steps_jx * steps_tt


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
