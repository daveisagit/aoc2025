"""Advent of code 2025
--- Day 5: Cafeteria ---
"""

from itertools import pairwise


def tok(in_str: str, delim=" ") -> list:
    """Tokenize i.e. split and strip"""
    return [e.strip() for e in in_str.split(delim)]


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_data(raw_data):
    """Parse the input"""
    ranges = []
    ingredients = []
    for idx, line in enumerate(raw_data):
        if not line:
            break
        arr = tok(line, "-")
        a = int(arr[0])
        b = int(arr[1]) + 1
        ranges.append((a, b))

    for idx, line in enumerate(raw_data[idx + 1 :]):
        ingredients.append(int(line))

    return ranges, ingredients


def solve_part_a(data) -> int:
    """Solve part A"""
    ranges, ingredients = data
    cnt = 0
    for i in ingredients:
        for a, b in ranges:
            if a <= i < b:
                cnt += 1
                break
    print(cnt)


def solve_part_b(data) -> int:
    """Solve part B"""
    # find the total amount of space covered by
    # the union of all the ranges
    ranges, _ = data
    markers = []
    ra = [a for a, _ in ranges]
    rb = [b for _, b in ranges]
    markers = set(ra) | set(rb)
    markers = sorted(markers)

    # marker are all the points of interest
    # spaces lie between markers
    spaces = {(a, b): False for a, b in pairwise(markers)}

    # for every range, see if the space used
    for a, b in ranges:
        for low, upp in spaces:
            # mark this space as used if it lies in one of the ranges
            if a <= low and upp <= b:
                spaces[(low, upp)] = True

    # return the sum of used space
    total = sum([upp - low for (low, upp), inc in spaces.items() if inc])
    print(total)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
