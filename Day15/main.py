from collections import OrderedDict


def part1(lines):
    steps = parse_steps(lines[0])
    return sum(hash_algorithm(step) for step in steps)


def part2(lines):
    steps = parse_steps(lines[0])
    boxes = initialize_boxes(steps)
    return sum(get_focusing_power(boxes, box_number) for box_number in boxes)


def parse_steps(steps):
    return [step for step in steps.split(',')]


def hash_algorithm(string):
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def add_lens(boxes, label, focal):
    box_number = hash_algorithm(label)
    if box_number not in boxes:
        boxes[box_number] = OrderedDict()
    boxes[box_number][label] = focal


def remove_lens(boxes, label):
    box_number = hash_algorithm(label)
    try:
        del boxes[box_number][label]
    except KeyError:
        # Ignore deleting a non existing label / box
        pass


def initialize_boxes(steps):
    boxes = {}
    for step in steps:
        if "=" in step:
            # Add lens
            label, focal = step.split("=")
            add_lens(boxes, label, int(focal))
        else:
            # Remove lens
            remove_lens(boxes, step[:-1])
    return boxes


def get_focusing_power(boxes, box_number):
    box = boxes[box_number]
    focusing_power = 0
    for i, label in enumerate(box):
        focusing_power += (box_number + 1) * (i + 1) * box[label]
    return focusing_power


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
