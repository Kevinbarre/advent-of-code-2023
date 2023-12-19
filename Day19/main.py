from itertools import groupby


def part1(lines):
    workflows, parts = parse_input(lines)
    accepted_parts = get_accepted_parts(workflows, parts)
    return sum(get_part_value(part) for part in accepted_parts)


def part2(lines):
    workflows = parse_input_2(lines)
    accepted_ranges = get_accepted_ranges(workflows, PartRange(1, 4000, 1, 4000, 1, 4000, 1, 4000))
    return sum(get_range_distinct_combinations(accepted_range) for accepted_range in accepted_ranges)


class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __eq__(self, other):
        return self.x == other.x and self.m == other.m and self.a == other.a and self.s == other.s

    def __repr__(self):
        return "Part(x=%r, m=%r, a=%r, s=%r)" % (self.x, self.m, self.a, self.s)


class PartRange:
    def __init__(self, x_min, x_max, m_min, m_max, a_min, a_max, s_min, s_max):
        self.x_min = x_min
        self.x_max = x_max
        self.m_min = m_min
        self.m_max = m_max
        self.a_min = a_min
        self.a_max = a_max
        self.s_min = s_min
        self.s_max = s_max

    def __eq__(self, other):
        return (self.x_min == other.x_min and self.x_max == other.x_max
                and self.m_min == other.m_min and self.m_max == other.m_max
                and self.a_min == other.a_min and self.a_max == other.a_max
                and self.s_min == other.s_min and self.s_max == other.s_max)

    def __hash__(self):
        return hash((self.x_min, self.x_max, self.m_min, self.m_max, self.a_min, self.a_max, self.s_min, self.s_max))

    def __repr__(self):
        return "Part(x=[%r, %r], m=[%r, %r], a=[%r, %r], s=[%r, %r])" % (
            self.x_min, self.x_max, self.m_min, self.m_max, self.a_min, self.a_max, self.s_min, self.s_max)

    def slice(self, attribute, value):
        """
        Create new range, replacing current attribute by value, keeping other attributes
        :param attribute: Attribute to replace
        :param value: New value to set in attribute
        :return: New range with replaced attribute by value
        """
        return PartRange(*[getattr(self, attr) if attr != attribute else value for attr in self.__dict__.keys()])


def parse_input(lines):
    workflow_lines, part_lines = [list(g) for k, g in groupby(lines, key=bool) if k]
    parts = []
    for part_line in part_lines:
        raw_x, raw_m, raw_a, raw_s = part_line[1:-1].split(',')
        parts.append(Part(*(parse_raw_part(i) for i in (raw_x, raw_m, raw_a, raw_s))))

    workflows = {}
    for workflow_line in workflow_lines:
        name, raw_workflow = workflow_line[:-1].split('{')
        workflows[name] = parse_raw_workflow(raw_workflow)
    return workflows, parts


def parse_raw_part(raw_part):
    _, value = raw_part.split('=')
    return int(value)


def parse_raw_workflow(raw_workflow):
    workflow = get_eval_workflow(raw_workflow)
    return eval(workflow)


def get_eval_workflow(raw_workflow):
    steps = raw_workflow.split(',')
    eval_steps = "lambda p: "
    for step in steps:
        if ':' in step:
            if_part, result = step.split(':')
            if_part = if_part[0] + ' ' + if_part[1] + ' ' + if_part[2:]
            eval_steps += '"{}" if p.{} else '.format(result, if_part)
        else:
            eval_steps += '"{}"'.format(step)
    return eval_steps


def process_part(workflows, part):
    current_workflow = "in"
    while current_workflow not in ('A', 'R'):
        current_workflow = workflows[current_workflow](part)
    return current_workflow == 'A'


def get_accepted_parts(workflows, parts):
    return [part for part in parts if process_part(workflows, part)]


def get_part_value(part):
    return part.x + part.m + part.a + part.s


def parse_input_2(lines):
    workflow_lines, _ = [list(g) for k, g in groupby(lines, key=bool) if k]
    workflows = {}
    for workflow_line in workflow_lines:
        name, raw_workflow = workflow_line[:-1].split('{')
        workflows[name] = raw_workflow
    return workflows


def parse_raw_workflow_for_ranges(raw_workflow, part_ranges):
    workflows_for_ranges = {}
    steps = raw_workflow.split(',')
    ranges_to_map = part_ranges
    for step in steps:
        if ':' in step:
            if_part, name = step.split(':')
            attribute, condition, value = if_part[0], if_part[1], int(if_part[2:])
            remaining_ranges = set()
            for range_to_map in ranges_to_map:
                matching_range, remaining_range = split_range(attribute, condition, value, range_to_map)
                if matching_range:
                    workflows_for_ranges.setdefault(name, set()).add(matching_range)
                if remaining_range:
                    remaining_ranges.add(remaining_range)
            ranges_to_map = remaining_ranges
        else:
            workflows_for_ranges.setdefault(step, set()).update(ranges_to_map)
    return workflows_for_ranges


def split_range(attribute, condition, value, part_range):
    attr_min = attribute + "_min"
    attr_max = attribute + "_max"
    current_min = getattr(part_range, attr_min)
    current_max = getattr(part_range, attr_max)
    if condition == '<':
        if value < current_min:
            return None, part_range
        elif value > current_max:
            return part_range, None
        else:  # current_min <= value <= current_max
            return part_range.slice(attr_max, value - 1), part_range.slice(attr_min, value)
    else:  # '>'
        if value < current_min:
            return part_range, None
        elif value > current_max:
            return None, part_range
        else:  # current_min <= value <= current_max
            return part_range.slice(attr_min, value + 1), part_range.slice(attr_max, value)


def get_range_distinct_combinations(part_range):
    return (part_range.x_max - part_range.x_min + 1) * (part_range.m_max - part_range.m_min + 1) * (
            part_range.a_max - part_range.a_min + 1) * (part_range.s_max - part_range.s_min + 1)


def get_accepted_ranges(workflows, initial_range):
    ranges_to_map = {"in": {initial_range}}
    accepted_ranges = set()
    while ranges_to_map:
        future_ranges_to_map = {}
        for name, ranges in ranges_to_map.items():
            parsed_ranges_by_workflow = parse_raw_workflow_for_ranges(workflows[name], ranges)
            try:
                accepted_ranges.update(parsed_ranges_by_workflow.pop("A"))
            except KeyError:
                # No accepted range for this workflow
                pass
            # Remove rejected ranges, we don't need them
            parsed_ranges_by_workflow.pop("R", None)
            for parsed_name, parsed_ranges in parsed_ranges_by_workflow.items():
                future_ranges_to_map.setdefault(parsed_name, set()).update(parsed_ranges)
            ranges_to_map = future_ranges_to_map
    return accepted_ranges


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
