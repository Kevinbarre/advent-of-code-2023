from itertools import groupby


def part1(lines):
    workflows, parts = parse_input(lines)
    accepted_parts = get_accepted_parts(workflows, parts)
    return sum(get_part_value(part) for part in accepted_parts)


def part2(lines):
    return 0


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


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
