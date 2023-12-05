import pytest

from main import part1, part2, parse_lines, parse_seeds, parse_maps, get_seed_location, find_lowest_location, \
    parse_input, MapElement, CompleteMap, parse_seed_ranges, parse_input_2, Range, get_seed_range_location_ranges, \
    find_lowest_location_from_ranges

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 35


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 46


def test_parse_lines():
    # Given
    lines = ["seeds: 79 14 55 13", "", "seed-to-soil map:", "50 98 2", "52 50 48", "", "soil-to-fertilizer map:",
             "0 15 37", "37 52 2", "39 0 15"]
    # When
    raw_initial_seeds, raw_maps = parse_lines(lines)
    # Then
    assert raw_initial_seeds == "seeds: 79 14 55 13"
    assert raw_maps == [
        ["seed-to-soil map:", "50 98 2", "52 50 48"],
        ["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]
    ]


def test_parse_seeds():
    # Given
    raw_initial_seeds = "seeds: 79 14 55 13"
    # When
    result = parse_seeds(raw_initial_seeds)
    # Then
    assert result == [79, 14, 55, 13]


def test_parse_maps():
    # Given
    raw_maps = [
        ["seed-to-soil map:", "50 98 2", "52 50 3"],
        ["soil-to-fertilizer map:", "0 15 1", "37 52 2", "39 0 3"]
    ]
    # When
    result = parse_maps(raw_maps)
    # Then
    assert len(result) == 2
    # Seed to soil map
    complete_map_1 = result[0]
    assert len(complete_map_1.map_elements) == 2
    map_element_1 = complete_map_1.map_elements[0]
    assert map_element_1.source_range_start == 98
    assert map_element_1.source_range_end == 99
    assert map_element_1.destination_range_start == 50
    map_element_2 = complete_map_1.map_elements[1]
    assert map_element_2.source_range_start == 50
    assert map_element_2.source_range_end == 52
    assert map_element_2.destination_range_start == 52
    # Soil to fertilizer map
    complete_map_2 = result[1]
    map_element_3 = complete_map_2.map_elements[0]
    assert map_element_3.source_range_start == 15
    assert map_element_3.source_range_end == 15
    assert map_element_3.destination_range_start == 0
    map_element_4 = complete_map_2.map_elements[1]
    assert map_element_4.source_range_start == 52
    assert map_element_4.source_range_end == 53
    assert map_element_4.destination_range_start == 37
    map_element_5 = complete_map_2.map_elements[2]
    assert map_element_5.source_range_start == 0
    assert map_element_5.source_range_end == 2
    assert map_element_5.destination_range_start == 39


def test_parse_input():
    # Given
    lines = ["seeds: 79 14 55 13", "", "seed-to-soil map:", "50 98 2", "52 50 3", "", "soil-to-fertilizer map:",
             "0 15 1", "37 52 2", "39 0 3"]
    # When
    seeds, maps = parse_input(lines)
    # Then
    assert seeds == [79, 14, 55, 13]
    assert len(maps) == 2
    # Seed to soil map
    complete_map_1 = maps[0]
    assert len(complete_map_1.map_elements) == 2
    map_element_1 = complete_map_1.map_elements[0]
    assert map_element_1.source_range_start == 98
    assert map_element_1.source_range_end == 99
    assert map_element_1.destination_range_start == 50
    map_element_2 = complete_map_1.map_elements[1]
    assert map_element_2.source_range_start == 50
    assert map_element_2.source_range_end == 52
    assert map_element_2.destination_range_start == 52
    # Soil to fertilizer map
    complete_map_2 = maps[1]
    map_element_3 = complete_map_2.map_elements[0]
    assert map_element_3.source_range_start == 15
    assert map_element_3.source_range_end == 15
    assert map_element_3.destination_range_start == 0
    map_element_4 = complete_map_2.map_elements[1]
    assert map_element_4.source_range_start == 52
    assert map_element_4.source_range_end == 53
    assert map_element_4.destination_range_start == 37
    map_element_5 = complete_map_2.map_elements[2]
    assert map_element_5.source_range_start == 0
    assert map_element_5.source_range_end == 2
    assert map_element_5.destination_range_start == 39


def test_get_seed_location():
    # Given
    maps = [
        # Seed to soil
        CompleteMap([MapElement(79, 79, 81)]),
        # Soil to fertilizer
        CompleteMap([MapElement(81, 81, 81)]),
        # Fertilizer to water
        CompleteMap([MapElement(81, 81, 81)]),
        # Water to light
        CompleteMap([MapElement(81, 81, 74)]),
        # Light to temperature
        CompleteMap([MapElement(74, 74, 78)]),
        # Temperature to humidity
        CompleteMap([MapElement(78, 78, 78)]),
        # Humidity to location
        CompleteMap([MapElement(78, 78, 82)]),
    ]
    # When
    result = get_seed_location(79, maps)
    # Then
    assert result == 82


def test_get_seed_location_with_same_destination_not_mapped():
    # Given
    maps = [
        # Seed to soil
        CompleteMap([MapElement(79, 79, 81)]),
        # Soil to fertilizer
        CompleteMap([]),
        # Fertilizer to water
        CompleteMap([]),
        # Water to light
        CompleteMap([MapElement(81, 81, 74)]),
        # Light to temperature
        CompleteMap([MapElement(74, 74, 78)]),
        # Temperature to humidity
        CompleteMap([]),
        # Humidity to location
        CompleteMap([MapElement(78, 78, 82)]),
    ]
    # When
    result = get_seed_location(79, maps)
    # Then
    assert result == 82


def test_find_lowest_location():
    # Given
    seeds = [79, 14]
    maps = [  # Seed to soil
        CompleteMap([MapElement(79, 79, 81)]),
        # Soil to fertilizer
        CompleteMap([MapElement(14, 14, 53)]),
        # Fertilizer to water
        CompleteMap([MapElement(53, 53, 49)]),
        # Water to light
        CompleteMap([MapElement(81, 81, 74), MapElement(49, 49, 42)]),
        # Light to temperature
        CompleteMap([MapElement(74, 74, 78)]),
        # Temperature to humidity
        CompleteMap([MapElement(42, 42, 43)]),
        # Humidity to location
        CompleteMap([MapElement(78, 78, 82)]),
    ]
    # When
    result = find_lowest_location(seeds, maps)
    # Then
    assert result == 43


def test_map_element_map_source_inside_range():
    # Given
    map_element = MapElement(20, 30, 50)
    # When
    result = map_element.map_source(25)
    # Then
    assert result == 55


def test_map_element_map_source_outside_range():
    # Given
    map_element = MapElement(20, 30, 50)
    # When
    result = map_element.map_source(35)
    # Then
    assert result is False


@pytest.mark.parametrize("test_input,expected",
                         [(25, 55), (47, 87), (36, 36)])
def test_complete_map_map_source(test_input, expected):
    # Given
    map_element1 = MapElement(20, 30, 50)
    map_element2 = MapElement(40, 50, 80)
    complete_map = CompleteMap([map_element1, map_element2])
    # When
    result = complete_map.map_source(test_input)
    # Then
    assert result == expected


def test_parse_seeds_range():
    # Given
    raw_initial_seeds = "seeds: 79 14 55 13"
    # When
    result = parse_seed_ranges(raw_initial_seeds)
    # Then
    assert len(result) == 2
    first_range = result[0]
    assert first_range.start == 79
    assert first_range.end == 92
    second_range = result[1]
    assert second_range.start == 55
    assert second_range.end == 67


def test_parse_input_range():
    # Given
    lines = ["seeds: 79 14 55 13", "", "seed-to-soil map:", "50 98 2", "52 50 3", "", "soil-to-fertilizer map:",
             "0 15 1", "37 52 2", "39 0 3"]
    # When
    seed_ranges, maps = parse_input_2(lines)
    # Then
    assert len(seed_ranges) == 2
    first_range = seed_ranges[0]
    assert first_range.start == 79
    assert first_range.end == 92
    second_range = seed_ranges[1]
    assert second_range.start == 55
    assert second_range.end == 67
    assert len(maps) == 2
    # Seed to soil map
    complete_map_1 = maps[0]
    assert len(complete_map_1.map_elements) == 2
    map_element_1 = complete_map_1.map_elements[0]
    assert map_element_1.source_range_start == 98
    assert map_element_1.source_range_end == 99
    assert map_element_1.destination_range_start == 50
    map_element_2 = complete_map_1.map_elements[1]
    assert map_element_2.source_range_start == 50
    assert map_element_2.source_range_end == 52
    assert map_element_2.destination_range_start == 52
    # Soil to fertilizer map
    complete_map_2 = maps[1]
    map_element_3 = complete_map_2.map_elements[0]
    assert map_element_3.source_range_start == 15
    assert map_element_3.source_range_end == 15
    assert map_element_3.destination_range_start == 0
    map_element_4 = complete_map_2.map_elements[1]
    assert map_element_4.source_range_start == 52
    assert map_element_4.source_range_end == 53
    assert map_element_4.destination_range_start == 37
    map_element_5 = complete_map_2.map_elements[2]
    assert map_element_5.source_range_start == 0
    assert map_element_5.source_range_end == 2
    assert map_element_5.destination_range_start == 39


def test_equal_range():
    # Given
    range_1 = Range(10, 1)
    range_2 = Range(10, 1)
    # When
    result = range_1 == range_2
    # Then
    assert result is True


# Test for case 1.1 and case 3
@pytest.mark.parametrize("test_input",
                         [Range(10, 10), Range(31, 10)])
def test_map_element_map_range_seed_range_outside_map(test_input):
    # Given
    map_element = MapElement(20, 30, 50)
    # When
    result = map_element.map_range(test_input)
    # Then
    assert result is False


# Test for other cases
@pytest.mark.parametrize("test_input, expected_mapped_range, expected_remaining_ranges", [
    # Case 1.2
    (Range(10, 15), Range(50, 5), [Range(10, 10)]),
    # Case 1.3
    (Range(10, 31), Range(50, 11), [Range(10, 10), Range(31, 10)]),
    # Case 2.1
    (Range(20, 8), Range(50, 8), []),
    (Range(22, 6), Range(52, 6), []),
    # Case 2.2
    (Range(20, 15), Range(50, 11), [Range(31, 4)]),
    (Range(22, 13), Range(52, 9), [Range(31, 4)])
])
def test_map_element_map_range_seed_inside_map(test_input, expected_mapped_range, expected_remaining_ranges):
    # Given
    map_element = MapElement(20, 30, 50)
    # When
    mapped_range, remaining_ranges = map_element.map_range(test_input)
    # Then
    assert mapped_range == expected_mapped_range
    assert remaining_ranges == expected_remaining_ranges


def test_map_element_map_range_single_element():
    # Given
    map_element = MapElement(79, 79, 81)
    # When
    mapped_range, remaining_ranges = map_element.map_range(Range(79, 1))
    # Then
    assert mapped_range == Range(81, 1)
    assert remaining_ranges == []


def test_map_element_map_range_single_element_bigger_map():
    # Given
    map_element = MapElement(50, 97, 52)
    # When
    mapped_range, remaining_ranges = map_element.map_range(Range(82, 1))
    # Then
    assert mapped_range == Range(84, 1)
    assert remaining_ranges == []


def test_complete_map_map_ranges():
    # Given
    seed_range = Range(15, 41)
    assert seed_range.start == 15
    assert seed_range.end == 55
    map_element1 = MapElement(20, 30, 120)
    map_element2 = MapElement(40, 50, 80)
    complete_map = CompleteMap([map_element1, map_element2])
    # When
    result = complete_map.map_ranges([seed_range])
    # Then
    assert len(result) == 5
    assert Range(15, 5) in result
    assert Range(120, 11) in result
    assert Range(31, 9) in result
    assert Range(80, 11) in result
    assert Range(51, 5) in result


def test_complete_map_map_ranges_single_element():
    # Given
    seed_range = Range(79, 1)
    complete_map = CompleteMap([MapElement(79, 79, 81)])
    # When
    result = complete_map.map_ranges([seed_range])
    # Then
    assert result == [Range(81, 1)]


def test_get_seed_range_location_range():
    # Given
    maps = [
        # Seed to soil
        CompleteMap([MapElement(79, 79, 81)]),
        # Soil to fertilizer
        CompleteMap([MapElement(81, 81, 81)]),
        # Fertilizer to water
        CompleteMap([MapElement(81, 81, 81)]),
        # Water to light
        CompleteMap([MapElement(81, 81, 74)]),
        # Light to temperature
        CompleteMap([MapElement(74, 74, 78)]),
        # Temperature to humidity
        CompleteMap([MapElement(78, 78, 78)]),
        # Humidity to location
        CompleteMap([MapElement(78, 78, 82)]),
    ]
    # When
    result = get_seed_range_location_ranges(Range(79, 1), maps)
    # Then
    assert result == [Range(82, 1)]


def test_find_lowest_location_from_ranges():
    # Given
    seed_ranges = [Range(79, 1), Range(14, 1)]
    maps = [  # Seed to soil
        CompleteMap([MapElement(79, 79, 81)]),
        # Soil to fertilizer
        CompleteMap([MapElement(14, 14, 53)]),
        # Fertilizer to water
        CompleteMap([MapElement(53, 53, 49)]),
        # Water to light
        CompleteMap([MapElement(81, 81, 74), MapElement(49, 49, 42)]),
        # Light to temperature
        CompleteMap([MapElement(74, 74, 78)]),
        # Temperature to humidity
        CompleteMap([MapElement(42, 42, 43)]),
        # Humidity to location
        CompleteMap([MapElement(78, 78, 82)]),
    ]
    # When
    result = find_lowest_location_from_ranges(seed_ranges, maps)
    # Then
    assert result == 43
