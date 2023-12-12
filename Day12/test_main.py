import pytest

from main import part1, part2, parse_input, count_arrangements, unfold

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 21


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 525152


def test_parse_input():
    # Given
    lines = ["???.### 1,1,3", ".??..??...?##. 1,1,3"]
    # When
    result = parse_input(lines)
    # Then
    assert len(result) == 2
    assert result[0] == ("???.###", (1, 1, 3))
    assert result[1] == (".??..??...?##.", (1, 1, 3))


@pytest.mark.parametrize("conditions, groups, expected", [("", (1,), 0),
                                                          (".", (1,), 0),
                                                          ("#", (1,), 1),
                                                          ("?", (1,), 1),
                                                          ("??", (1,), 2),
                                                          ("#?", (1,), 1),
                                                          ("?#", (1,), 1),
                                                          ("???", (1, 1), 1),
                                                          ("???.###", (1, 1, 3), 1),
                                                          (".??..??...?##.", (1, 1, 3), 4),
                                                          ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
                                                          ("????.#...#...", (4, 1, 1), 1),
                                                          ("????.######..#####.", (1, 6, 5), 4),
                                                          ("?###????????", (3, 2, 1), 10)])
def test_count_arrangements(conditions, groups, expected):
    # Given
    # When
    result = count_arrangements(conditions, groups)
    # Then
    assert result == expected


def test_unfold():
    # Given
    record = (".#", [1])
    # When
    result = unfold(record)
    # Then
    assert result == (".#?.#?.#?.#?.#", [1, 1, 1, 1, 1])


@pytest.mark.parametrize("conditions, groups, expected", [("???.###", (1, 1, 3), 1),
                                                          (".??..??...?##.", (1, 1, 3), 16384),
                                                          ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
                                                          ("????.#...#...", (4, 1, 1), 16),
                                                          ("????.######..#####.", (1, 6, 5), 2500),
                                                          ("?###????????", (3, 2, 1), 506250)])
def test_count_unfolded_arrangements(conditions, groups, expected):
    # Given
    unfolded_conditions, unfolded_groups = unfold((conditions, groups))
    # When
    result = count_arrangements(unfolded_conditions, unfolded_groups)
    # Then
    assert result == expected
