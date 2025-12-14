"""Advent of code 2025
--- Day 9: Movie Theater ---
"""

import re
from itertools import pairwise, combinations


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
        sr = re.search(r"(\d+),(\d+)", line)
        d = tuple(int(g) for g in sr.groups())
        data.append(d)
    return data


def solve_part_a(data) -> int:
    """Solve part A"""
    max_area = 0
    for a, b in combinations(data, 2):
        x = abs(a[0] - b[0]) + 1
        y = abs(a[1] - b[1]) + 1
        area = x * y
        if area > max_area:
            max_area = area
    print(max_area)


def get_boundaries(outline):
    """Return the boundary as two lists of vertical and horizontal sections
    Range limits are inclusive of the corner at both ends, and limits are ordered
    Example entries:
    vertical:    (5,3,9) would represent the line between corners (5,9) - (5,3)
    horizontal:  (4,1,6) would represent the line between corners (1,4) - (6,4)
    """
    bound_v = []
    bound_h = []
    for a, b in pairwise(outline):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        if ay == by:
            # horizontal
            t = ay, min(ax, bx), max(ax, bx)
            bound_h.append(t)
        else:
            # vertical
            t = ax, min(ay, by), max(ay, by)
            bound_v.append(t)

    return bound_v, bound_h


def solve_part_b(data) -> int:
    """Solve part B"""
    outline = data + [data[0]]
    bound_v, bound_h = get_boundaries(outline)

    # sort the rectangle options, largest area first
    rectangles = {}
    for a, b in combinations(data, 2):
        x = abs(a[0] - b[0]) + 1
        y = abs(a[1] - b[1]) + 1
        area = x * y
        rectangles[(a, b)] = area
    rectangles = sorted(rectangles.items(), key=lambda x: x[1], reverse=True)

    for r, area in rectangles:
        # a,b are points, opposite corners of the rectangle
        # the sides of r being x1: left, x2: right, y1: top, y2: bottom
        a, b = r
        x1 = min(a[0], b[0])
        x2 = max(a[0], b[0])
        y1 = min(a[1], b[1])
        y2 = max(a[1], b[1])

        # check which vertical sections the rectangle could collide with
        # if any of them overlap with the vertical side of the rectangle
        # then we should reject
        overlap = False
        for x, e1, e2 in bound_v:
            # it is valid for a rectangle side to be part of the boundary
            # so we are only looking for vertical sections that lie within
            # the left+right ends (exclusive)
            if x1 < x < x2:
                # if any section lies inside the rectangle then
                # this is an overlap (this representation has been turned 90)
                # e1-------e2
                #      y1--------y2
                if max(y1, e1) < min(y2, e2):
                    overlap = True
                    break

        if overlap:
            continue

        # now the same for the horizontal sections
        for y, e1, e2 in bound_h:
            # just consider horizontal sections that could fit between
            # the top and bottom of the rectangle
            if y1 < y < y2:
                # e1-------e2
                #      x1--------x2
                if max(x1, e1) < min(x2, e2):
                    overlap = True
                    break

        if not overlap:
            print(area)
            return


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
