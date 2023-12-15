from collections import OrderedDict

import pytest

from main import part1, part2, parse_steps, hash_algorithm, add_lens, remove_lens, initialize_boxes, get_focusing_power

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 1320


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 145


def test_parse_steps():
    # Given
    steps = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    # When
    result = parse_steps(steps)
    # Then
    assert result == ["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]


def test_hash_algorithm():
    # Given
    string = "HASH"
    # When
    result = hash_algorithm(string)
    # Then
    assert result == 52


def test_add_lens():
    # Given
    boxes = {}
    # When
    add_lens(boxes, "cm", 1)
    # Then
    assert boxes == {0: {"cm": 1}}


def test_add_lens_replace_old():
    # Given
    boxes = {0: OrderedDict({"cm": 1})}
    # When
    add_lens(boxes, "cm", 9)
    # Then
    assert boxes == {0: {"cm": 9}}


def test_remove_lens():
    # Given
    boxes = {0: OrderedDict({"cm": 1})}
    # When
    remove_lens(boxes, "cm")
    # Then
    assert boxes == {0: {}}


def test_remove_lens_from_non_existing_box():
    # Given
    boxes = {}
    # When
    remove_lens(boxes, "cm")
    # Then
    assert boxes == {}


def test_initialize_boxes():
    # Given
    steps = ["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]
    # When
    result = initialize_boxes(steps)
    # Then
    assert result == {0: OrderedDict({"rn": 1, "cm": 2}),
                      1: OrderedDict(),
                      3: OrderedDict({"ot": 7, "ab": 5, "pc": 6})}


@pytest.mark.parametrize("test_input, expected", [(0, 5), (1, 0), (3, 140)])
def test_get_focusing_power(test_input, expected):
    # Given
    boxes = {0: OrderedDict({"rn": 1, "cm": 2}),
             1: OrderedDict(),
             3: OrderedDict({"ot": 7, "ab": 5, "pc": 6})}
    # When
    result = get_focusing_power(boxes, test_input)
    # Then
    assert result == expected
