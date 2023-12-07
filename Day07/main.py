from collections import Counter

CARD_VALUE = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


def part1(lines):
    hands = parse_hands(lines)
    return get_total_winnings(hands)


def part2(lines):
    return 0


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid

    def __repr__(self):
        return "Hand(cards=%r, bid=%r)" % (self.cards, self.bid)

    def __eq__(self, other):
        return self.cards == other.cards and self.bid == other.bid

    def __lt__(self, other):
        self_cards_occurrence = sorted(Counter(self.cards).values(), reverse=True)
        other_cards_occurrence = sorted(Counter(other.cards).values(), reverse=True)
        # Compare types first
        for self_nb, other_nb in zip(self_cards_occurrence, other_cards_occurrence):
            if self_nb != other_nb:
                return self_nb < other_nb
        # Same hand type, compare by cards order
        for self_card, other_card in zip(self.cards, other.cards):
            self_card_value = CARD_VALUE[self_card]
            other_card_value = CARD_VALUE[other_card]
            if self_card_value != other_card_value:
                return self_card_value < other_card_value


def parse_hands(lines):
    hands = []
    for line in lines:
        cards, raw_bid = line.split()
        hands.append(Hand(cards, int(raw_bid)))
    return hands


def get_total_winnings(hands):
    hands.sort()
    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
