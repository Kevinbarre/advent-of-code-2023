import pytest

from main import part1, part2, parse_input, apply_instruction, reach_zzz, get_starting_nodes, reach_all_z, \
    reach_any_z_from_position

filename = "example.txt"


@pytest.mark.parametrize("test_input, expected",
                         [(filename, 2), ("example2.txt", 6)])
def test_part1(test_input, expected):
    # Given
    with open(test_input) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == expected


def test_part2():
    # Given
    with open("example3.txt") as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 6


def test_parse_input():
    # Given
    lines = ["RL", "", "AAA = (BBB, CCC)", "BBB = (DDD, EEE)", "CCC = (ZZZ, GGG)", "DDD = (DDD, DDD)",
             "EEE = (EEE, EEE)", "GGG = (GGG, GGG)", "ZZZ = (ZZZ, ZZZ)"]
    # When
    instructions, maps = parse_input(lines)
    # Then
    assert instructions == "RL"
    assert maps == {"AAA": ("BBB", "CCC"), "BBB": ("DDD", "EEE"), "CCC": ("ZZZ", "GGG"), "DDD": ("DDD", "DDD"),
                    "EEE": ("EEE", "EEE"), "GGG": ("GGG", "GGG"), "ZZZ": ("ZZZ", "ZZZ")}


@pytest.mark.parametrize("test_input, expected",
                         [("L", "BBB"), ("R", "CCC")])
def test_apply_instruction(test_input, expected):
    # Given
    maps = {"AAA": ("BBB", "CCC")}
    current_position = "AAA"
    # When
    result = apply_instruction(test_input, current_position, maps)
    # Then
    assert result == expected


def test_reach_zzz():
    # Given
    maps = {"AAA": ("BBB", "CCC"), "BBB": ("DDD", "EEE"), "CCC": ("ZZZ", "GGG")}
    instructions = "RL"
    # When
    result = reach_zzz(instructions, maps)
    # Then
    assert result == 2


def test_reach_zzz_recursive():
    # Given
    maps = {"AAA": ("BBB", "BBB"), "BBB": ("AAA", "ZZZ")}
    instructions = "LLR"
    # When
    result = reach_zzz(instructions, maps)
    # Then
    assert result == 6


def test_get_starting_nodes():
    # Given
    maps = {"11A": ("11B", "XXX"), "11B": ("XXX", "11Z"), "11Z": ("11B", "XXX"), "22A": ("22B", "XXX"),
            "22B": ("22C", "22C"), "22C": ("22Z", "22Z"), "22Z": ("22B", "22B"), "XXX": ("XXX", "XXX")}
    # When
    result = get_starting_nodes(maps)
    # Then
    assert result == ["11A", "22A"]


@pytest.mark.parametrize("test_input, expected",
                         [("11A", 2), ("22A", 3)])
def test_reach_any_z_from_position(test_input, expected):
    # Given
    maps = {"11A": ("11B", "XXX"), "11B": ("XXX", "11Z"), "11Z": ("11B", "XXX"), "22A": ("22B", "XXX"),
            "22B": ("22C", "22C"), "22C": ("22Z", "22Z"), "22Z": ("22B", "22B"), "XXX": ("XXX", "XXX")}
    instructions = "LR"
    # When
    result = reach_any_z_from_position(test_input, instructions, maps)
    # Then
    assert result == expected


def test_reach_all_z():
    # Given
    maps = {"11A": ("11B", "XXX"), "11B": ("XXX", "11Z"), "11Z": ("11B", "XXX"), "22A": ("22B", "XXX"),
            "22B": ("22C", "22C"), "22C": ("22Z", "22Z"), "22Z": ("22B", "22B"), "XXX": ("XXX", "XXX")}
    instructions = "LR"
    # When
    result = reach_all_z(instructions, maps)
    # Then
    assert result == 6
