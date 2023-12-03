MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def part1(lines):
    games = [parse_game(line) for line in lines]
    return sum(game.id for game in games if is_game_possible(game))


def part2(lines):
    return 0


class Game:
    def __init__(self, id, sets):
        self.id = id
        self.sets = sets


class Set:
    red = 0
    green = 0
    blue = 0

    def __init__(self):
        pass


def parse_game(line):
    raw_game, raw_sets = line.split(':')
    _, game_number = raw_game.split(' ')
    raw_sets = raw_sets.split(';')
    sets = []
    for raw_set in raw_sets:
        new_set = Set()
        colors = raw_set.split(',')
        for raw_color in colors:
            raw_color = raw_color.strip()
            amount, color = raw_color.split(' ')
            setattr(new_set, color, int(amount))
        sets.append(new_set)
    return Game(int(game_number), sets)


def is_set_possible(set):
    return set.red <= MAX_RED and set.green <= MAX_GREEN and set.blue <= MAX_BLUE


def is_game_possible(game):
    return all(is_set_possible(game_set) for game_set in game.sets)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.readlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
