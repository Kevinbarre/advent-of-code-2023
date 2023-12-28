from networkx import parse_adjlist, stoer_wagner


def part1(lines):
    graph = parse_graph(lines)
    first, second = get_separate_groups(graph)
    return len(first) * len(second)


def part2(lines):
    return 0


def parse_graph(lines):
    lines = [line.replace(":", "") for line in lines]
    return parse_adjlist(lines)


def get_separate_groups(graph):
    _, groups = stoer_wagner(graph)
    first = set(groups[0])
    second = set(groups[1])
    if len(first) > len(second):
        return first, second
    else:
        return second, first


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
