from itertools import combinations


def part1(lines, min_boundary, max_boundary):
    hailstones = parse_hailstones(lines)
    return sum(1 for hailstone_1, hailstone_2 in combinations(hailstones, 2) if
               hailstone_1.intersect_xy(hailstone_2, min_boundary, max_boundary))


def part2(lines):
    return 0


class Hailstone:
    def __init__(self, px, py, pz, vx, vy, vz):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __eq__(self, other):
        return (self.px == other.px and self.py == other.py and self.pz == other.pz
                and self.vx == other.vx and self.vy == other.vy and self.vz == other.vz)

    def __hash__(self):
        return hash((self.px, self.py, self.pz, self.vx, self.vy, self.vz))

    def __repr__(self):
        return "Hailstone(px=%r, py=%r, pz=%r, vx=%r, vy=%r, vz=%r)" % (
            self.px, self.py, self.pz, self.vx, self.vy, self.vz)

    def intersect_xy(self, other, min_boundary, max_boundary):
        # y = a1 * x + b1 and y = a2 * x + b2
        # a1 = vy1 / vx1 , b1 = py1 - px1 * a1
        # a2 = vy2 / vx2 , b2 = py2 - px2 * a2
        a1 = self.vy / self.vx
        b1 = self.py - self.px * a1
        a2 = other.vy / other.vx
        b2 = other.py - other.px * a2
        # a1 * x + b1 = a2 * x + b2
        # (a1 - a2) * x = b2 - b1
        # x = (b2 - b1) / (a1 - a2)
        try:
            x = (b2 - b1) / (a1 - a2)
        except ZeroDivisionError:
            # Parallel lines
            return False
        # y = a1 * x + b1
        y = a1 * x + b1
        # x = px1 + t1 * vx1
        # t1 = (x - px1) / vx1
        t1 = (x - self.px) / self.vx
        t2 = (x - other.px) / other.vx
        if t1 < 0 or t2 < 0:
            return False
        return min_boundary < x < max_boundary and min_boundary < y < max_boundary


def parse_hailstones(lines):
    hailstones = []
    for line in lines:
        raw_position, raw_velocity = line.split(" @ ")
        px, py, pz = map(int, raw_position.split(", "))
        vx, vy, vz = map(int, raw_velocity.split(", "))
        hailstones.append(Hailstone(px, py, pz, vx, vy, vz))
    return hailstones


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines, 200000000000000, 400000000000000))
    print("Part 2 : ", part2(f_lines))
