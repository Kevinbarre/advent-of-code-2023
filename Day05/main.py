from itertools import groupby


def part1(lines):
    seeds, maps = parse_input(lines)
    return find_lowest_location(seeds, maps)


def part2(lines):
    return 0


def parse_lines(lines):
    raw_initial_seeds = lines[0]
    raw_maps = [list(g) for k, g in groupby(map(str.strip, lines[2:]), key=lambda line: line != '') if k]
    return raw_initial_seeds, raw_maps


def parse_seeds(raw_initial_seeds):
    _, seeds = raw_initial_seeds.split(":")
    return [int(seed) for seed in seeds.split()]


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


def find_lowest_location(seeds, maps):
    return min(get_seed_location(seed, maps) for seed in seeds)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
