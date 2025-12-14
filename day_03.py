"""Advent of code 2025
--- Day 3: Lobby ---
"""


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        digits = [int(d) for d in line]
        data.append(digits)
    return data


def get_max(digits: list, batteries=2):
    """Find the largest digit to the left but
    no further than the required length to the right.
    Call recursively"""
    if batteries == 0:
        return 0
    # how far right can we look, must leave room
    # remaining digits
    scope = len(digits) - batteries

    # (left) these are the digits we can pick from
    left = digits[: scope + 1]
    d = max(left)

    # find the first occurrence of it
    di = left.index(d)

    # (right) is the remaining portion we can pick from
    # on the next iteration
    right = digits[di + 1 :]

    # call recursively, 1 less battery
    return digits[di] * 10 ** (batteries - 1) + get_max(right, batteries - 1)


def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    for digits in data:
        t += get_max(digits)
    print(t)


def solve_part_b(data) -> int:
    """Solve part B"""
    t = 0
    for digits in data:
        t += get_max(digits, batteries=12)
    print(t)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
