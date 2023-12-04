def part1(lines):
    cards = parse_cards(lines)
    return sum(get_points(card) for card in cards)


def part2(lines):
    return 0


class Card:
    def __init__(self, winning_numbers, numbers):
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    def get_number_of_win(self):
        return len(set.intersection(self.numbers, self.winning_numbers))


def parse_cards(lines):
    cards = []
    for line in lines:
        _, all_numbers = line.split(':')
        raw_winning_numbers, raw_numbers = all_numbers.split('|')
        winning_numbers = {int(winning_number) for winning_number in raw_winning_numbers.split()}
        numbers = {int(number) for number in raw_numbers.split()}
        cards.append(Card(winning_numbers, numbers))
    return cards


def get_points(card):
    number_of_wins = card.get_number_of_win()
    if number_of_wins > 0:
        return 2 ** (number_of_wins - 1)
    else:
        return 0


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
