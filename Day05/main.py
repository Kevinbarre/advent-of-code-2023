from itertools import groupby


def part1(lines):
    seeds, maps = parse_input(lines)
    return find_lowest_location(seeds, maps)


def part2(lines):
    seed_ranges, maps = parse_input_2(lines)
    return find_lowest_location_from_ranges(seed_ranges, maps)


def parse_lines(lines):
    raw_initial_seeds = lines[0]
    raw_maps = [list(g) for k, g in groupby(map(str.strip, lines[2:]), key=lambda line: line != '') if k]
    return raw_initial_seeds, raw_maps


def parse_seeds(raw_initial_seeds):
    _, seeds = raw_initial_seeds.split(":")
    return [int(seed) for seed in seeds.split()]


def parse_seed_ranges(raw_initial_seeds):
    _, raw_seeds = raw_initial_seeds.split(":")
    raw_seeds = raw_seeds.split()
    seed_ranges = []
    while raw_seeds:
        start = int(raw_seeds.pop(0))
        range_length = int(raw_seeds.pop(0))
        seed_ranges.append(Range(start, range_length))
    return seed_ranges


class MapElement:
    def __init__(self, source_range_start, source_range_end, destination_range_start):
        self.source_range_start = source_range_start
        self.source_range_end = source_range_end
        self.destination_range_start = destination_range_start

    def map_source(self, source_value):
        if self.source_range_start <= source_value <= self.source_range_end:
            # Between range, compute destination value (Difference between value and the source start, and then we add this to the destination start
            return source_value - self.source_range_start + self.destination_range_start
        return False

    def map_range(self, range_value):
        # Case 1 : Range start is strictly before MapElement start
        if range_value.start < self.source_range_start:
            # Case 1.1 : Range end is strictly before MapElement start
            if range_value.end < self.source_range_start:
                # No mapping, as the range is outside the map
                return False
            # Case 1.2 : Range end is before MapElement end
            if range_value.end <= self.source_range_end:
                # Mapped range has length of difference between range_value.end and source_range_start + 1
                mapped_range = Range(self.destination_range_start,
                                     range_value.end - self.source_range_start + 1)
                # Still need to map the remaining range smaller than the map
                remaining_ranges = [Range(range_value.start, self.source_range_start - range_value.start)]
                return mapped_range, remaining_ranges
            # Case 1.3 : Range end is after MapElement end
            else:
                # Mapped range has length of self
                mapped_range = Range(self.destination_range_start, self.source_range_end - self.source_range_start + 1)
                # Still need to map the remaining range before and after the map
                remaining_ranges = [Range(range_value.start, self.source_range_start - range_value.start),
                                    Range(self.source_range_end + 1, range_value.end - self.source_range_end)]
                return mapped_range, remaining_ranges
        # Case 2 : Range start is before MapElement end
        elif range_value.start <= self.source_range_end:
            # Case 2.1 : Range end is before MapElement end
            if range_value.end <= self.source_range_end:
                # Mapped range with offset of range_value.start - source_range_start and has length of input range
                mapped_range = Range(self.destination_range_start + range_value.start - self.source_range_start,
                                     range_value.end - range_value.start + 1)
                # The whole range has been mapped, no remaining range
                remaining_ranges = []
                return mapped_range, remaining_ranges
            # Case 2.2 : Range end is after MapElement end
            else:
                # Mapped range with offset of range_value.start - source_range_start has length of difference between source_range_end and range_value.start
                mapped_range = Range(self.destination_range_start + range_value.start - self.source_range_start,
                                     self.source_range_end - range_value.start + 1)
                # Still need to map the remaining range after the map
                remaining_ranges = [Range(self.source_range_end + 1, range_value.end - self.source_range_end)]
                return mapped_range, remaining_ranges
        # Case 3 : Range start is after MapElement end
        else:
            # No mapping, as the range is outside the map
            return False


class CompleteMap:
    def __init__(self, map_elements):
        self.map_elements = map_elements

    def map_source(self, source_value):
        for map_element in self.map_elements:
            destination = map_element.map_source(source_value)
            if destination:
                # Destination found with one of the MapElement, can return this value
                return destination
        # No mapping found, default to returning the source value
        return source_value

    def map_ranges(self, range_values):
        ranges_to_map = range_values
        mapped_ranges = []
        for map_element in self.map_elements:
            future_remaining_ranges = []
            for range_to_map in ranges_to_map:
                map_result = map_element.map_range(range_to_map)
                if not map_result:
                    # No mapping performed, we'll have to handle this range with the next MapElement
                    future_remaining_ranges.append(range_to_map)
                else:
                    mapped_range, remaining_ranges = map_result
                    mapped_ranges.append(mapped_range)
                    future_remaining_ranges += remaining_ranges
            if not future_remaining_ranges:
                # No more ranges to map, we're done with this mapping step
                return mapped_ranges
            else:
                # Moving on with the next MapElement
                ranges_to_map = future_remaining_ranges
        # Remaining range to map are kept as they are
        return mapped_ranges + ranges_to_map


class Range:
    def __init__(self, start, length):
        self.start = start
        self.end = start + length - 1

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return "Range(start=%r, end=%r)" % (self.start, self.end)


def parse_maps(raw_maps):
    maps = []
    for raw_map in raw_maps:
        map_elements = []
        # Ignore map name
        raw_map = raw_map[1:]
        for map_line in raw_map:
            raw_destination, raw_source, raw_length = map_line.split()
            destination_range_start, source_range_start, range_length = int(raw_destination), int(raw_source), int(
                raw_length)
            new_map_element = MapElement(source_range_start, source_range_start + range_length - 1,
                                         destination_range_start)
            map_elements.append(new_map_element)
        new_map = CompleteMap(map_elements)
        # Add new map to the list of maps
        maps.append(new_map)

    return maps


def parse_input(lines):
    raw_initial_seeds, raw_maps = parse_lines(lines)
    seeds = parse_seeds(raw_initial_seeds)
    maps = parse_maps(raw_maps)
    return seeds, maps


def parse_input_2(lines):
    raw_initial_seeds, raw_maps = parse_lines(lines)
    seed_ranges = parse_seed_ranges(raw_initial_seeds)
    maps = parse_maps(raw_maps)
    return seed_ranges, maps


def get_seed_location(seed, maps):
    seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = maps
    soil = seed_to_soil.map_source(seed)
    fertilizer = soil_to_fertilizer.map_source(soil)
    water = fertilizer_to_water.map_source(fertilizer)
    light = water_to_light.map_source(water)
    temperature = light_to_temperature.map_source(light)
    humidity = temperature_to_humidity.map_source(temperature)
    location = humidity_to_location.map_source(humidity)

    return location


def get_seed_range_location_ranges(seed_range, maps):
    seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = maps
    soil_ranges = seed_to_soil.map_ranges([seed_range])
    fertilizer_ranges = soil_to_fertilizer.map_ranges(soil_ranges)
    water_ranges = fertilizer_to_water.map_ranges(fertilizer_ranges)
    light_ranges = water_to_light.map_ranges(water_ranges)
    temperature_ranges = light_to_temperature.map_ranges(light_ranges)
    humidity_ranges = temperature_to_humidity.map_ranges(temperature_ranges)
    location_ranges = humidity_to_location.map_ranges(humidity_ranges)
    return location_ranges


def find_lowest_location(seeds, maps):
    return min(get_seed_location(seed, maps) for seed in seeds)


def find_lowest_location_from_ranges(seed_ranges, maps):
    location_ranges = []
    for seed_range in seed_ranges:
        location_ranges += get_seed_range_location_ranges(seed_range, maps)
    return min(location_range.start for location_range in location_ranges)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
