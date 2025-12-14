"""Advent of code 2025
--- Day 6: Trash Compactor ---
"""

from math import prod


def tok(in_str: str, delim=" ") -> list:
    """Tokenize i.e. split and strip"""
    return [e.strip() for e in in_str.split(delim)]


def file_to_list(filename: str):
    """Read text file to list of strings"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        lines = f.readlines()
    return [line[:-1] for line in lines]


def parse_data(raw_data):
    """Parse the input"""
    rows = len(raw_data)
    data = []
    for r, line in enumerate(raw_data):

        row = []
        arr = tok(line, " ")
        for tk in arr:
            if tk == "" or tk == " ":
                continue
            if r < rows - 1:
                tk = int(tk)
            row.append(tk)

        data.append(row)

    return list(map(list, zip(*data)))


def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    for row in data:
        values = row[:-1]
        if row[-1] == "+":
            v = sum(values)
        else:
            v = prod(values)
        t += v

    print(t)


def solve_part_b(data) -> int:
    """Solve part B using the raw data"""

    data_rows = data[:-1]
    op_row = data[-1]

    # build a list of operations, an operation = [+/* , a , b]
    # the values are between indexes a,b in the data row string
    ops = []
    op = None
    for i, ch in enumerate(op_row):
        if ch != " ":
            if op:
                op[2] = i - 1
                ops.append(op)
            op = [ch, i, 0]
    op[2] = len(op_row) + 1
    ops.append(op)

    t = 0

    # for each operation
    for op_data in ops:
        cs = 0
        op, a, b = op_data

        # build the values list
        values = []

        # for each column, build the value as a string -> wrd
        for idx in range(a, b):
            v = 0
            wrd = ""
            for row in data_rows:
                d = row[idx]
                wrd += d
            v = int(wrd)
            values.append(v)

        if op == "+":
            cs = sum(values)
        else:
            cs = prod(values)
        t += cs

    print(t)


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(RAW_DATA)
