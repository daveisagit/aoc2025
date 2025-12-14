"""Advent of code 2025
--- Day 2: Gift Shop ---
"""


def tok(in_str: str, delim=" ") -> list:
    """Tokenize i.e. split and strip"""
    return [e.strip() for e in in_str.split(delim)]


def file_to_string(filename: str):
    """Read whole file as string"""
    ENCODING = "utf-8"
    with open(filename, encoding=ENCODING) as f:
        content = f.read()
    return content


def parse_data(raw_data):
    """Parse the input"""
    a = tok(raw_data, ",")

    data = []
    for p in a:
        pa = tok(p, "-")
        t = (int(pa[0]), int(pa[1]))
        data.append(t)
    return data


def is_valid(id):
    """Look for a double repeat"""
    sid = str(id)
    if len(sid) % 2 == 1:
        return True
    l = len(sid)
    a = sid[: l // 2]
    b = sid[l // 2 :]
    return a != b


def is_valid_b(id):
    """Look for a multiple repeat"""
    sid = str(id)
    l = len(sid)
    for rl in range(1, l // 2 + 1):

        if l % rl != 0:
            continue

        rc = sid[:rl]
        is_repeat = True
        for i in range(rl, l - rl + 1, rl):
            if sid[i : i + rl] != rc:
                is_repeat = False
                break

        if is_repeat:
            return False

    return True


def solve_part_a(data) -> int:
    """Solve part A"""
    vt = 0
    for a, b in data:
        for p in range(a, b + 1):
            if not is_valid(p):
                vt += p
    print(vt)


def solve_part_b(data) -> int:
    """Solve part B"""
    vt = 0
    for a, b in data:
        for p in range(a, b + 1):
            if not is_valid_b(p):
                vt += p
    print(vt)


FILE_PATH = ""
RAW_DATA = file_to_string(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
