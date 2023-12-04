def part1(lines):
    cards = parse_cards(lines)
    return sum(get_points(card) for card in cards)


def part2(lines):
    cards = parse_cards(lines)
    amount_of_each_card = get_amount_of_each_card(cards)
    return sum(amount_of_each_card.values())


class Card:
    def __init__(self, id, winning_numbers, numbers):
        self.id = id
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    def get_number_of_win(self):
        return len(set.intersection(self.numbers, self.winning_numbers))


def parse_cards(lines):
    cards = []
    for line in lines:
        raw_identifier, all_numbers = line.split(':')
        _, identifier = raw_identifier.split()
        raw_winning_numbers, raw_numbers = all_numbers.split('|')
        winning_numbers = {int(winning_number) for winning_number in raw_winning_numbers.split()}
        numbers = {int(number) for number in raw_numbers.split()}
        cards.append(Card(int(identifier), winning_numbers, numbers))
    return cards


def get_points(card):
    number_of_wins = card.get_number_of_win()
    if number_of_wins > 0:
        return 2 ** (number_of_wins - 1)
    else:
        return 0


def get_amount_of_each_card(cards):
    cards_counter = {card.id: 1 for card in cards}
    for card in cards:
        matching_numbers = card.get_number_of_win()
        # For each wining number, we get more of the below cards
        # More specifically, we get one for each instance of the current card
        current_card_counter = cards_counter[card.id]
        for i in range(1, matching_numbers + 1):
            cards_counter[card.id + i] += current_card_counter
    return cards_counter


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
