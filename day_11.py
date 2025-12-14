"""Advent of code 2025
--- Day 11: Reactor ---
"""

from functools import lru_cache


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
    data = {}
    for line in raw_data:
        a = line[:3]
        bs = tok(line[5:], " ")
        data[a] = {}
        for b in bs:
            data[a][b] = 1
    return data


def solve_part_a(data) -> int:
    """Solve part A"""

    @lru_cache(maxsize=None)
    def get_path_count(u):
        cnt = 0
        for v in data[u]:
            if v == "out":
                return 1
            else:
                cnt += get_path_count(v)
        return cnt

    total = 0
    for v in data["you"]:
        total += get_path_count(v)
    print(total)


def solve_part_b(data) -> int:
    """Solve part B"""

    @lru_cache(maxsize=None)
    def get_path_count(u, fft_flag, dac_flag):
        inc = 0
        exc = 0
        for v in data[u]:
            if v == "out":
                if fft_flag and dac_flag:
                    inc += 1
                else:
                    exc += 1
            else:
                if v == "fft":
                    fft_flag = True
                if v == "dac":
                    dac_flag = True
                v_inc, v_exc = get_path_count(v, fft_flag, dac_flag)
                inc += v_inc
                exc += v_exc
        return inc, exc

    total_inc = 0
    for v in data["svr"]:
        cnt_inc, _ = get_path_count(v, False, False)
        total_inc += cnt_inc

    print(total_inc)
    return


FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
