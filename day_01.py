"""Advent of code 2025
--- Day 1: Secret Entrance ---
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
        d = 1
        if line[0] == "L":
            d = -1
        v = int(line[1:]) * d
        data.append(v)

    return data


def solve_part_a(data) -> int:
    """Solve part A"""
    cv = 50
    zeros = 0
    for t in data:
        cv += t
        cv = cv % 100
        if cv == 0:
            zeros += 1
    print(zeros)


def solve_part_b(data) -> int:
    """Solve part B"""
    cv = 50
    zeros = 0
    for i, t in enumerate(data):

        # the number of full turns regardless of direction
        full_turns = abs(t) // 100

        # the new position of the dial
        nv = cv + t
        nv = nv % 100

        # we will have definitely clocked this many zeros
        zeros += full_turns

        # if starting from 0 then we need not consider any
        # extra cases since
        # the number of zeros clocked = the number of full turns
        if cv != 0:

            # we did not start from zero

            if nv == 0:
                # we landed on zero so add an extra 1, i.e. 99 + 101
                zeros += 1
            else:
                # we passed over a zero with a movement smaller than a full turn
                # indicated by the dial difference not matching the direction of travel
                if t < 0 and nv >= cv or t > 0 and nv <= cv:
                    zeros += 1

        cv = nv

    print(zeros)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
