def part1(lines):
    bricks = parse_bricks(lines)
    bricks = sort_bricks_vertically(bricks)
    settled_bricks = settle_bricks(bricks)
    return len(get_destructible_bricks(settled_bricks))


def part2(lines):
    return 0


class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.supported_bricks = set()
        self.supported_by = set()
        self.cubes = {(x, y) for x in range(self.start[0], self.end[0] + 1) for y in
                      range(self.start[1], self.end[1] + 1)}

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __repr__(self):
        return "Brick(start=%r, end=%r)" % (self.start, self.end)

    def collide(self, possible_colling_brick):
        """
        Check if two brick, that are expected to be on the same z axis, collide
        :param possible_colling_brick: Other brick to check collision
        :return: True if the two bricks collide, False otherwise
        """
        return not self.cubes.isdisjoint(possible_colling_brick.cubes)

    def supports(self, supported_brick):
        self.supported_bricks.add(supported_brick)

    def is_supported_by(self, supporting_brick):
        self.supported_by.add(supporting_brick)


def parse_bricks(lines):
    bricks = []
    for line in lines:
        raw_start, raw_end = line.split('~')
        start = tuple(int(xyz) for xyz in raw_start.split(','))
        end = tuple(int(xyz) for xyz in raw_end.split(','))
        bricks.append(Brick(start, end))
    return bricks


def sort_bricks_vertically(bricks):
    return sorted(bricks, key=lambda brick: (brick.start[2], brick.start[1], brick.start[0]))


def fall_brick(brick, stable_bricks):
    if brick.start[2] == 1:
        # Brick on floor, no need to check anymore
        stable_bricks.append(brick)
        return stable_bricks
    else:
        for z in range(1, brick.start[2]):
            # Make brick fall of z
            falling_brick = Brick((brick.start[0], brick.start[1], brick.start[2] - z),
                                  (brick.end[0], brick.end[1], brick.end[2] - z))
            # Get all stable_bricks that have an end position at the start height of brick
            possible_colling_bricks = [brick for brick in stable_bricks if brick.end[2] == falling_brick.start[2]]
            if len(possible_colling_bricks) != 0:
                # Need to check if one of the identified brick collide with the falling brick
                colliding_bricks = []
                for possible_colling_brick in possible_colling_bricks:
                    if falling_brick.collide(possible_colling_brick):
                        # Found a colliding brick, remember it
                        colliding_bricks.append(possible_colling_brick)
                if len(colliding_bricks) != 0:
                    # At least one colliding brick have been found. Need to stop the falling brick one step above
                    fallen_brick = Brick((brick.start[0], brick.start[1], brick.start[2] - z + 1),
                                         (brick.end[0], brick.end[1], brick.end[2] - z + 1))
                    # Remember that these bricks are supporting the new fallen brick
                    for colliding_brick in colliding_bricks:
                        colliding_brick.supports(fallen_brick)
                        fallen_brick.is_supported_by(colliding_brick)
                    stable_bricks.append(fallen_brick)
                    return stable_bricks
        # Brick made it to the ground without colliding, can return it laying on ground
        height = brick.start[2] - 1
        brick_on_ground = Brick((brick.start[0], brick.start[1], brick.start[2] - height),
                                (brick.end[0], brick.end[1], brick.end[2] - height))
        stable_bricks.append(brick_on_ground)
        return stable_bricks


def settle_bricks(bricks):
    settled_bricks = []
    for brick in bricks:
        fall_brick(brick, settled_bricks)
    return settled_bricks


def get_destructible_bricks(settled_bricks):
    required_bricks = set()
    for brick in settled_bricks:
        if len(brick.supported_by) == 1:
            required_bricks.update(brick.supported_by)
    return {brick for brick in settled_bricks if brick not in required_bricks}


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
