"""Advent of code 2025
--- Day 8: Playground ---
"""

from math import prod
import re

from collections import Counter
from itertools import combinations


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
        sr = re.search(r"(\d+),(\d+),(\d+)", line)
        d = tuple(int(g) for g in sr.groups())
        data.append(d)
    return data


def hyp2(a, b):
    """Return the hypotenuse squared"""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def get_possible_connections(jbs):
    """Return a sorted (shortest lead first) list of possible connections"""
    dist = {}
    for a, b in combinations(jbs, 2):
        dist[(a, b)] = hyp2(a, b)
    return sorted(dist.items(), key=lambda x: x[1])


def solve_part_a(data, leads=10) -> int:
    """Solve part A"""
    # each junction box is its own circuit to start with
    circuits = {jb: jb for jb in data}
    all_possible_connections = get_possible_connections(data)
    for p, _ in all_possible_connections[:leads]:
        a, b = p
        ca = circuits[a]
        cb = circuits[b]
        # move junction boxes on circuit b to circuit a
        merge = [jb for jb, cir in circuits.items() if cir == cb]
        for jb in merge:
            circuits[jb] = ca

    cnt = Counter(circuits.values())
    top3 = cnt.most_common(3)
    print(prod(amt for _, amt in top3))


def solve_part_b(data) -> int:
    """Solve part B"""
    circuits = {jb: jb for jb in data}
    all_possible_connections = get_possible_connections(data)
    for p, _ in all_possible_connections:
        a, b = p
        ca = circuits[a]
        cb = circuits[b]
        # move junction boxes on circuit b to circuit a
        merge = [jb for jb, cir in circuits.items() if cir == cb]
        for jb in merge:
            circuits[jb] = ca

        # same as part A but quit once all are connected
        result = [jb for jb, cir in circuits.items() if cir == ca]
        if len(result) == len(data):
            print(a[0] * b[0])
            return


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

# set leads=10 for example or 1000 for puzzle
solve_part_a(DATA, leads=1000)
solve_part_b(DATA)
