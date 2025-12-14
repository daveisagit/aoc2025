"""Advent of code 2025
--- Day 7: Laboratories ---
"""

from functools import lru_cache
from operator import add


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_data(raw_data):
    """Parse the input"""
    grid = {}
    start = None
    sz = len(raw_data), len(raw_data[0])
    for ri, row in enumerate(raw_data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            if ch == "S":
                start = p
                ch = "."
            grid[p] = ch
    return sz, grid, start


def solve_part_a(data) -> int:
    """Solve part A"""

    def do_row(bc: set, r):
        """For this row add/remove beams and count hits on a splitter"""
        cnt = 0
        new_bc = bc.copy()
        for c in bc:
            p = (r, c)
            if p in grid:
                cnt += 1
                new_bc.add(c - 1)
                new_bc.add(c + 1)
                new_bc.remove(c)

        return new_bc, cnt

    sz, grid, start = data
    grid = {p: ch for p, ch in grid.items() if ch == "^"}
    beam_columns = {start[1]}
    t = 0
    for r in range(1, sz[0]):
        beam_columns, cnt = do_row(beam_columns, r)
        t += cnt

    print(t)


def solve_part_b(data) -> int:
    """Solve part B"""

    @lru_cache(maxsize=None)
    def get_splits(cp):

        # Going down
        np = tuple(map(add, cp, (1, 0)))

        # off grid, end of recursion => return 1 path
        if np not in grid:
            return 1

        # no change, whatever next is passed back up the stack
        if grid[np] == ".":
            return get_splits(np)

        # hit a splitter, explore both branches, left and right
        # split count is the sum of both
        elif grid[np] == "^":
            nl = tuple(map(add, cp, (0, -1)))
            nr = tuple(map(add, cp, (0, 1)))
            return get_splits(nl) + get_splits(nr)

    _, grid, start = data
    print(get_splits(start))


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
