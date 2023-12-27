from itertools import combinations


def part1(lines, min_boundary, max_boundary):
    hailstones = parse_hailstones(lines)
    return sum(1 for hailstone_1, hailstone_2 in combinations(hailstones, 2) if
               hailstone_1.intersect_xy(hailstone_2, min_boundary, max_boundary))


def part2(lines):
    hailstones = parse_hailstones(lines)
    rock = get_rock(hailstones)
    return rock.px + rock.py + rock.pz


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


def shift_hailstones(hailstones):
    """Shift positions and speeds in the reference system of the first hailstone in the list"""
    new_reference = hailstones[0]
    return [Hailstone(hailstone.px - new_reference.px, hailstone.py - new_reference.py, hailstone.pz - new_reference.pz,
                      hailstone.vx - new_reference.vx, hailstone.vy - new_reference.vy, hailstone.vz - new_reference.vz)
            for hailstone in hailstones], new_reference


def get_normal_vector(hailstone):
    """Get normal vector defined by the positions of hailstone at t0 and t1"""
    u = (hailstone.px, hailstone.py, hailstone.pz)  # u = (u0, u1, u2)
    v = (hailstone.px + hailstone.vx, hailstone.py + hailstone.vy, hailstone.pz + hailstone.vz)  # v = (v0, v1, v2)
    # u ∧ v = (u1v2 - u2v1, u2v0 - u0v2, u0v1 - u1v0)
    return u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]


def get_scalar_product(hailstone_speed, normal):
    return hailstone_speed[0] * normal[0] + hailstone_speed[1] * normal[1] + hailstone_speed[2] * normal[2]


def intersect_plane(hailstone, normal):
    scalar_position = get_scalar_product((-hailstone.px, -hailstone.py, -hailstone.pz), normal)
    scalar_speed = get_scalar_product((hailstone.vx, hailstone.vy, hailstone.vz), normal)
    time = scalar_position // scalar_speed
    position = (
        hailstone.px + hailstone.vx * time, hailstone.py + hailstone.vy * time, hailstone.pz + hailstone.vz * time)
    return position, time


def get_rock(hailstones):
    shifted_hailstones, new_reference = shift_hailstones(hailstones)
    normal = get_normal_vector(shifted_hailstones[1])
    position_2, time_2 = intersect_plane(shifted_hailstones[2], normal)
    position_3, time_3 = intersect_plane(shifted_hailstones[3], normal)
    time_difference = time_2 - time_3
    rock_speed = tuple((position_2[i] - position_3[i]) // time_difference for i in range(3))
    rock_position = tuple(position_2[i] - rock_speed[i] * time_2 for i in range(3))
    # Shift back rock into original coordinates reference
    return Hailstone(rock_position[0] + new_reference.px, rock_position[1] + new_reference.py,
                     rock_position[2] + new_reference.pz, rock_speed[0] + new_reference.vx,
                     rock_speed[1] + new_reference.vy, rock_speed[2] + new_reference.vz)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines, 200000000000000, 400000000000000))
    print("Part 2 : ", part2(f_lines))
