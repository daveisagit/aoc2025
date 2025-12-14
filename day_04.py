"""Advent of code 2025
--- Day 4: Printing Department ---
"""

from operator import add


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_data(raw_data):
    """Parse the input"""
    cells = set()
    for ri, row in enumerate(raw_data):
        for ci, cell in enumerate(row):
            if cell == "@":
                p = (ri, ci)
                cells.add(p)
    return cells


DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = 0
    for p in data:
        c = 0
        for d in DIRECTIONS:
            np = tuple(map(add, p, d))
            if np in data:
                c += 1
        if c < 4:
            cnt += 1
    print(cnt)


def make_new_grid(data):
    cnt = 0
    new_set = set()
    for p in data:
        c = 0
        for d in DIRECTIONS:
            np = tuple(map(add, p, d))
            if np in data:
                c += 1
        if c < 4:
            cnt += 1
        else:
            new_set.add(p)
    return new_set, cnt


def solve_part_b(data) -> int:
    """Solve part B"""
    t = 0
    while True:
        data, cnt = make_new_grid(data)
        if cnt == 0:
            break
        t += cnt
    print(t)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
