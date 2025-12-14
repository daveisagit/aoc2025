"""Advent of code 2025
--- Day 10: Factory ---
"""

from collections import Counter
from fractions import Fraction
from itertools import chain, combinations, product
from math import inf, prod


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
    data = []
    for line in raw_data:
        arr = tok(line)

        # indicator
        ind = arr[0][1:-1]
        iv = int("".join(["0" if d == "." else "1" for d in ind]), base=2)

        # buttons
        btns = []
        for btn in arr[1:-1]:
            btn = tok(btn[1:-1], ",")
            btn = tuple([int(i) for i in btn])
            btns.append(btn)
        btns = tuple(btns)

        # joltages
        js = tok(arr[-1][1:-1], ",")
        js = tuple([int(j) for j in js])

        t = (ind, iv, btns, js)

        data.append(t)

    return data


def convert_btn(bts, bl):
    """Each button has a binary value which we can use to XOR"""
    res = []
    for bt in bts:
        v = 0
        for b in bt:
            b = bl - b - 1
            v += 2**b
        res.append(v)
    return tuple(res)


def powerset(iterable):
    """Return the powerset of an iterable
    for example powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def solve_machine_a(row):
    ind_s, iv, btns, _ = row
    btns = convert_btn(btns, len(ind_s))
    # the powerset generator will yield 0 to all presses in that order
    # so the first match will be minimal
    for bs in powerset(btns):
        v = 0
        for b in bs:
            v = v ^ b
        if v == iv:
            return len(bs)

    # we have failed
    assert False


def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    for r in data:
        v = solve_machine_a(r)
        t += v
    print(t)


def get_reduced_ref(btns, js):
    """Return a Reduced REF matrix of the linear system"""
    # Aim: use row reduction to arrive at a matrix where
    # the columns of non-free (pivot) variables are all 0s
    # except for the pivot row. In other words if you removed
    # the free variable columns you would have a zero matrix
    # but with a diagonal of non-zeros.
    #
    # From there you could take the final step to convert those
    # non-zeros to 1's which puts it in reduced Row Echelon Form (RREF)
    # but for our purposes we can divide by the pivot value later
    # when calculating the fixed values for a specific instance
    # of the free variables.
    #
    # So for the 1st example the system looks like this
    #
    # pressing button 5 E times + button 6 F times should give a joltage of 3
    # or in other words
    #
    # E+F   = 3 (these affect indicator 0)
    # B+F   = 5 (these affect indicator 1)
    # C+D+E = 4 (these affect indicator 2)
    # A+B+D = 7 (these affect indicator 3)
    #
    #   0 0 0 0 1 1  x  |A| = 3
    #   0 1 0 0 0 1     |B|   5
    #   0 0 1 1 1 0     |C|   4
    #   1 1 0 1 0 0     |D|   7
    #                   |E|
    #                   |F|
    #
    # So starting with the augmented matrix
    #   0 0 0 0 1 1 3
    #   0 1 0 0 0 1 5
    #   0 0 1 1 1 0 4
    #   1 1 0 1 0 0 7
    #
    # using elimination we want to arrive at this
    # where variables 3 and 5 (marked v) are free
    #            v     v
    #   1  0  0  1  0 -1  2
    #   0  1  0  0  0  1  5
    #   0  0  1  1  0 -1  1
    #   0  0  0  0  1  1  3
    #
    # Ignoring the free variable and augmented columns would
    # leave us with a matrix where only the diagonal
    # was non-zero (in this case the identity)

    # From here we can explore all the valid options
    # for the free variables and for each option we can
    # derive what the fixed values must be
    #
    # fixed = (Aug - free) / pv
    #
    # Aug:  value in the last column
    # free: sum(opt[i] x mtx[i]) where i is the ith free variable
    # pv:   the value of the pivot (the diagonal)
    #
    # When then just need to validate the fixed values
    # for being positive integers and if so the option
    # is valid for being a possible minimal solution.

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Here we go
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # perform Gaussian elimination (its a fiddly business)
    # https://en.wikipedia.org/wiki/Gaussian_elimination
    # In order to avoid floating point issues we will work in fractions

    # initially create an augmented matrix with equation
    # coefficients defaulted to 0
    m = [[Fraction(0, 1) for _ in range(len(btns) + 1)] for _ in range(len(js))]

    # set the last (augmented column) from the joltages
    for i, jv in enumerate(js):
        m[i][-1] = Fraction(jv, 1)

    # set 1s for when a button increases a joltage
    for i, btn in enumerate(btns):
        for j in btn:
            m[j][i] = Fraction(1, 1)

    # because some columns might be free we need to track the
    # current row are pivoting on as this will not always be the same as
    # the current column we are considering
    row_idx = 0

    # the indexes of the free variables
    free = []

    for i in range(len(btns)):
        # we are currently considering the ith column (or button)
        # go down the column start from the row_idx
        # looking for the first non-zero value

        # assume one does not exist
        row_to_use = None
        for j, row in enumerate(m[row_idx:]):

            if row[i] != Fraction(0, 1):
                # we've found a non zero value
                # go to the next stage
                row_to_use = j + row_idx
                break

        # if there weren't any this is a free variable
        if row_to_use is None:
            free.append(i)
            continue

        # if this pivot row is not our current row
        # then swap the rows
        if row_idx != row_to_use:
            m[row_idx], m[row_to_use] = m[row_to_use], m[row_idx]

        # now make this ith column = 0 for all the other rows
        for k, row in enumerate(m):
            # this is us, leave alone
            if k == row_idx:
                continue
            # we might have to multiply our row
            # by some factor so that when we add it
            # to the other row the value in this ith column
            # becomes zero
            orig_row_i = row[i]
            for j, cell in enumerate(row):
                row[j] = cell - m[row_idx][j] * orig_row_i / m[row_idx][i]

            # the result of the above loop adjusts the whole row
            # keeping the equation balanced and in keeping with the
            # system, but means we have effectively eliminated
            # all variables from it except for the pivot

            # having leading zeros in the future rows means
            # we not upset our previous manipulations in prior
            # column when we come to future adjustments

        row_idx += 1

    # turn fractions into integers for readability
    for row in m:
        for i, cell in enumerate(row):
            if cell == int(cell):
                row[i] = int(cell)

    # pivot variables are the non-free variables
    pivot_vars = [i for i in range(len(btns)) if i not in free]
    return m, pivot_vars, free


def assess_free(data):
    """How much freedom do we have"""
    free_stats = []
    for i, r in enumerate(data):
        _, _, btns, js = r
        _, pv, free = get_reduced_ref(btns, js)
        if console_logging:
            print(
                f"Row:{i} Free={len(free)} Buttons={len(btns)} Joltages={len(js)} Pivots={len(pv)}"
            )
        free_stats.append(len(btns) - len(pv))
    print()
    print("Free variable frequency")
    cnt = Counter(free_stats)
    for k, v in cnt.items():
        print(f"{k} : {v}")
    print()


def check_ref_is_reduced(data):
    """Ignoring the columns for the free variables, make sure
    we are left with a matrix which is just zeros except for the diagonal
    """
    _, _, btns, js = data
    m, pv, _ = get_reduced_ref(btns, js)

    # remove the free variables
    squ_m = []
    for r in m:
        nr = [c for i, c in enumerate(r) if i in pv]
        if all([c == 0 for c in nr]):
            continue
        squ_m.append(nr)

    # after removing the free variables and augmented column
    # make sure we left with just a diagonal in a square matrix
    for i, r in enumerate(squ_m):
        assert len(r) == len(squ_m)  # rows=columns (for every row)
        assert r[i] != 0  # diagonal is not zero
        nd = [c for j, c in enumerate(r) if i != j]  # non-diagonals
        assert all([c == 0 for c in nd])  # are all zeros


def get_minimum_presses(data):
    """Return the minimum presses required"""

    def get_fixed_values(opt):
        """Given this option for the free values figure out
        what the fixed values must be"""
        vals = []
        for ri, r in enumerate(mtx):
            if all([x == 0 for x in r]):
                break
            # the adjustment is the contribution
            # of this option
            adj = 0
            for i, j in enumerate(free):
                adj += r[j] * opt[i]
            # the fixed value is the augmented column
            # less the adjustment
            x = r[-1] - adj
            # divided by the pivot value
            pivot_value = r[pv[ri]]
            x = Fraction(x, pivot_value)

            vals.append(x)
        return vals

    _, _, btns, js = data

    # obtain the system in RREF
    mtx, pv, free = get_reduced_ref(btns, js)

    # find the limits for button pressing
    max_presses = [min([js[i] for i in b]) for b in btns]

    # how many options will we need to consider
    total_options = prod(max_presses[fv] + 1 for fv in free)

    if console_logging:
        print(f"Free={free} MaxPresses={max_presses} Total options={total_options}")

    lowest_press_cnt = inf
    example_pressing = None
    for opt in product(*[range(max_presses[fv] + 1) for fv in free]):
        fixed = get_fixed_values(opt)
        # only positive integer values for fixed considered
        # as a valid option
        if any([v < 0 or v != int(v) for v in fixed]):
            continue
        press_cnt = sum(opt) + sum(fixed)
        if press_cnt < lowest_press_cnt:
            lowest_press_cnt = press_cnt
            example_pressing = []
            for i in range(len(btns)):
                if i in pv:
                    x = int(fixed[pv.index(i)])
                else:
                    x = int(opt[free.index(i)])
                example_pressing.append(x)
    return lowest_press_cnt, example_pressing


def solve_part_b(data) -> int:
    """Solve part B"""

    # Some checks on our data to ensure our approach is valid
    # as well as our reduction code
    assess_free(data)
    for r in data:
        check_ref_is_reduced(r)

    total = 0
    for i, r in enumerate(data):
        if console_logging:
            print()
            print(f"Doing row: {i}")
        min_presses, example = get_minimum_presses(r)
        if console_logging:
            print(f"Minimum={min_presses} eg:{example}")
        total += min_presses
    print(total)


console_logging = False

FILE_PATH = ""
RAW_DATA = file_to_list(FILE_PATH)
DATA = parse_data(RAW_DATA)

solve_part_a(DATA)
solve_part_b(DATA)
