from math import sqrt, floor, prod


def part1(lines):
    races = parse_races(lines)
    return prod(get_number_ways(*race) for race in races)


def part2(lines):
    return 0


def parse_races(lines):
    raw_times, raw_distances = lines
    _, raw_times = raw_times.split(":")
    times = [int(time) for time in raw_times.split()]
    _, raw_distances = raw_distances.split(":")
    distances = [int(distance) for distance in raw_distances.split()]
    return list(zip(times, distances))


def get_number_ways(time, distance):
    # x1 = (Time - sqrt(Time^2 -4Distance)) / 2
    delta = time ** 2 - 4 * distance
    x1 = (time - sqrt(delta)) / 2
    # Nb solutions = Total possibilities - failing ones = (Times + 1) - 2*(floor(x1) + 1)
    return time + 1 - 2 * (floor(x1) + 1)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
