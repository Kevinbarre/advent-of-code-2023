import pytest

from main import part1, part2, parse_races, get_number_ways

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 288


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_races():
    # Given
    lines = ["Time:      7  15   30", "Distance:  9  40  200"]
    # When
    result = parse_races(lines)
    # Then
    assert len(result) == 3
    assert result == [(7, 9), (15, 40), (30, 200)]


# Speed for Time=7
# 0 : 0*7 = 0
# 1 : 1*6 = 6
# 2 : 2*5 = 10
# 3 : 3*4 = 12
# 4 : 4*3 = 12
# 5 : 5*2 = 10
# 6 : 6*1 = 6
# 7 : 7*0 = 0
# i : i*(Time-i) = -i^2 + Time*i
# Go farther than current record Distance : -i^2 + Time*i > Distance <=> -i^2 + Time*i - Distance > 0
# a : -1 , b : Time , c = -Distance
# Delta : b^2 - 4ac = Time^2 - 4*(-1)*(-Distance) = Time^2 -4Distance
# x1 : (-b + sqrt(Delta))/2a = ( -Time + sqrt(Time^2 -4Distance))/-2 = (Time - sqrt(Time^2 -4Distance)) / 2
# x1 = (7 - sqrt(49 - 36))/2 = (7 - sqrt(13))/2 ~= 1.69
# x2 : (-b - sqrt(Delta))/2a = ( -Time - sqrt(Time^2 -4Distance))/-2 = (Time + sqrt(Time^2 -4Distance)) / 2
# x2 = (7 + sqrt(13))/2 ~= 5.3
# Nb solutions = Total possibilities - failing ones = (Times + 1) - 2*(floor(x1) + 1)

@pytest.mark.parametrize("test_input,expected",
                         [((7, 9), 4), ((15, 40), 8), ((30, 200), 9)])
def test_get_number_ways(test_input, expected):
    # Given
    time, distance = test_input
    # When
    result = get_number_ways(time, distance)
    # Then
    assert result == expected
