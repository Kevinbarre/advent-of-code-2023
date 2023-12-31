from math import prod


def part1(lines):
    return sum(find_part_numbers(lines))


def part2(lines):
    return sum(find_gear_ratios(lines))


def find_part_numbers(rows):
    part_numbers = []
    for j, row in enumerate(rows):
        current_number = ""
        start_index = -1
        for i, char in enumerate(row):
            if char.isdigit():
                current_number += char
                if start_index == -1:
                    # New number found
                    start_index = i
            else:
                if current_number == "":
                    # No current number, can continue safely
                    continue
                else:
                    # End of number is previous index
                    end_index = i - 1
                    # Check if number is part number
                    if is_part_number(j, start_index, end_index, rows):
                        # Add number to list of part numbers
                        part_numbers.append(int(current_number))
                    # Reset number
                    current_number = ""
                    start_index = -1
        # End of row loop, need to check if we don't have a pending current_number
        if current_number != "":
            # End of number is last column
            end_index = len(row) - 1
            # Check if number is part number
            if is_part_number(j, start_index, end_index, rows):
                # Add number to list of part numbers
                part_numbers.append(int(current_number))
    return part_numbers


def is_part_number(j, start_index, end_index, rows):
    if start_index != 0:
        # Not on first column, can check on left
        start_iterate = start_index - 1
    else:
        # On first column, check only from start index
        start_iterate = start_index

    if end_index != len(rows[0]) - 1:
        # Not on last column, can check on right
        end_iterate = end_index + 1
    else:
        # On last column, check only until end index
        end_iterate = end_index

    if j > 0:
        # Not on first row, can check above
        for i in range(start_iterate, end_iterate + 1):
            current_char = rows[j - 1][i]
            if is_symbol(current_char):
                # Symbol found !
                return True

    if j < len(rows) - 1:
        # Not on last row, can check below
        for i in range(start_iterate, end_iterate + 1):
            current_char = rows[j + 1][i]
            if is_symbol(current_char):
                # Symbol found !
                return True
    # Check on left
    if start_iterate != start_index:
        current_char = rows[j][start_iterate]
        if is_symbol(current_char):
            return True

    # Check on right
    if end_iterate != end_index:
        current_char = rows[j][end_iterate]
        if is_symbol(current_char):
            return True

    # No symbol found around the number
    return False


def is_symbol(current_char):
    return not current_char.isdigit() and current_char != '.'


def is_gear_symbol(current_char):
    return current_char == '*'


def is_gear(j, i, rows):
    part_numbers = []
    # Check on left
    if i != 0:
        current_char = rows[j][i - 1]
        if current_char.isdigit():
            # Found a digit directly left
            part_numbers.append(get_part_number(rows[j], i - 1))

    # Check on right
    if i != len(rows[0]) - 1:
        current_char = rows[j][i + 1]
        if current_char.isdigit():
            # Found a digit directly left
            part_numbers.append(get_part_number(rows[j], i + 1))

    if j > 0:
        # Not on first row, can check above
        # Check on top
        current_char = rows[j - 1][i]
        if current_char.isdigit():
            # Found a digit directly above, can't have two numbers separated by a symbol
            part_numbers.append(get_part_number(rows[j - 1], i))
        else:
            # Check on top-left
            current_char = rows[j - 1][i - 1]
            if current_char.isdigit():
                # Found a digit on top-left, get corresponding number
                part_numbers.append(get_part_number(rows[j - 1], i - 1))
            # Check on top-right
            current_char = rows[j - 1][i + 1]
            if current_char.isdigit():
                # Found a digit on top-right, get corresponding number
                part_numbers.append(get_part_number(rows[j - 1], i + 1))

    if j < len(rows) - 1:
        # Not on last row, can check below
        # Check on down
        current_char = rows[j + 1][i]
        if current_char.isdigit():
            # Found a digit directly below, can't have two numbers separated by a symbol
            part_numbers.append(get_part_number(rows[j + 1], i))
        else:
            # Check on down-left
            current_char = rows[j + 1][i - 1]
            if current_char.isdigit():
                # Found a digit on down-left, get corresponding number
                part_numbers.append(get_part_number(rows[j + 1], i - 1))
            # Check on top-right
            current_char = rows[j + 1][i + 1]
            if current_char.isdigit():
                # Found a digit on down-right, get corresponding number
                part_numbers.append(get_part_number(rows[j + 1], i + 1))

    if len(part_numbers) == 2:
        return prod(part_numbers)
    return False


def get_part_number(row, i):
    # Left digits
    left_digits = ""
    k = i - 1
    while k >= 0:
        current_char = row[k]
        if not current_char.isdigit():
            break
        left_digits += current_char
        k -= 1
    # Reverse digits as they've been added from right to left
    left_digits = left_digits[::-1]

    # Right digits
    right_digits = ""
    k = i + 1
    while k < len(row):
        current_char = row[k]
        if not current_char.isdigit():
            break
        right_digits += current_char
        k += 1

    return int(left_digits + row[i] + right_digits)


def find_gear_ratios(rows):
    gear_ratios = []
    for j in range(len(rows)):
        for i in range(len(rows[0])):
            current_char = rows[j][i]
            if is_gear_symbol(current_char):
                gear_ratio = is_gear(j, i, rows)
                if gear_ratio:
                    gear_ratios.append(gear_ratio)
    return gear_ratios


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
