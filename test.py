## reference: http://norvig.com/sudoku.html

grid_sample = """
4 . . |. . . |8 . 5
. 3 . |. . . |. . .
. . . |7 . . |. . .
------+------+------
. 2 . |. . . |. 6 .
. . . |. 8 . |4 . .
. . . |. 1 . |. . .
------+------+------
. . . |6 . 3 |. 7 .
5 . . |2 . . |. . .
1 . 4 |. . . |. . .
"""
digits = '123456789'
rows = 'ABCDEFGHI'


def cross(A, B):
    #result = []
    #for a in A:
    #    for b in B:
    #        result.append(a + b)
    #return result
    return [a + b for a in A for b in B]


def grid_values(squares, grid):
    """
    Convert grid into a dict of {square: char} with '0' or '.' for empties
    :param squares: a list of square names -> 'A1', 'A2', etc..
    :param grid
    """
    chars = [c for c in grid if c in digits or c in '0.']
    assert(len(chars) == 81)
    return dict(zip(squares, chars))


def parse_grid(squares, grid):
    """
    Convert grid into a dict of possible values, {square: digits}
    or return False is a contradiction is detected
    :param grid:
    :param squares"""
    values = dict((s, digits) for s in squares)

    for s, d in grid_values(squares, grid).items():
        # for every square and its provided value in the grid:
        #     propagate the constraint for this value through the grid
        assign_success = assign(values, s, d)
        if d in digits and not assign_success:
            return False

    return values


def assign(values, square, digit):
    """

    :param values: {square: digits} where square is 'A1', 'A2', etc. and digits is '12343...'
    :param square: the particular square
    :param digit:  the square's value
    :return: If updating every value was successful
    """

    return True


cols = digits
squares = cross(rows, cols)

unit_list = ([cross(rows, c) for c in cols] +
             [cross(r, cols) for r in rows] +
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

units = dict((s, [unit for unit in unit_list if s in unit]) for s in squares)

peers = {}
for s in squares:
    temp = []
    for u in units[s]:
        temp = u + temp
    peers[s] = set(temp) - set(s)

values = parse_grid(squares, grid_sample)
print values