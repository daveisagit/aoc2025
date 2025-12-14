"""Advent of code 2025
--- Day 12: Christmas Tree Farm ---

Didn't need to solve the packing problem, Eric's Taskmaster joke was that
you could get the same answer from just a sanity check on
a) the total area
b) if that's fine the number 3x3 blocks available

(Grr)

A valuable lesson on checking the bleeding obvious before
diving down a rabbit hole
"""

from collections import Counter
from math import prod


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def tok(in_str: str, delim=" ") -> list:
    """Tokenize i.e. split and strip"""
    return [e.strip() for e in in_str.split(delim)]


def parse_data(raw_data):
    """Parse the input"""

    presents = []
    present = ""
    regions = []
    for idx, line in enumerate(raw_data):
        if len(line) <= 2 or len(line) > 2 and line[2] != "x":
            if idx % 5 == 4:
                presents.append(present)
                present = ""
            elif 1 <= idx % 5 < 3:
                present += line
            continue

        if len(line) > 2 and line[2] == "x":
            arr = tok(line, ":")
            arr1 = tok(arr[0], "x")
            sz = tuple([int(x) for x in arr1])
            arr2 = tok(arr[1], " ")
            pis = tuple([int(x) for x in arr2])
            rd = sz, pis
            regions.append(rd)

    return presents, regions


def get_shapes(presents):
    """Return a list, each entry is the number of # in the shape"""
    shapes = []
    for p in presents:
        cnt = Counter(p)
        shapes.append(cnt["#"])
    return shapes


def get_fitting_order(region):
    """Return the list of shapes to be added in this order
    The order itself is not important but saves using a counter"""
    fitting_order = []
    for si, cnt in enumerate(region[1]):
        for _ in range(cnt):
            fitting_order.append(si)
    return fitting_order


def can_fit(shapes, region):
    """Return True if a solution exists"""

    sz = region[0]
    fitting_order = tuple(get_fitting_order(region))

    # sanity check / Taskmaster joke
    required_space = sum([shapes[shp_id] for shp_id in fitting_order])
    area_available = prod(sz)
    if required_space > area_available:
        # print(f"Rq={required_space} Size={area_available}")
        return False
    else:
        max_3x3_grids = (sz[0] // 3) * (sz[1] // 3)
        # print(f"3x3s:{max_3x3_grids} Presents:{len(fitting_order)}")
        if max_3x3_grids >= len(fitting_order):
            return True
        else:
            return False


def solve_part_a(data) -> int:
    """Solve part A"""
    presents, regions = data
    shapes = get_shapes(presents)
    t = 0
    for r in regions:
        if can_fit(shapes, r):
            t += 1
    print(t)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
