## reference: http://norvig.com/sudoku.html
import itertools

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

cols = digits
squares = cross(rows, cols)

unit_list = ([cross(rows, c) for c in cols] +
             [cross(r, cols) for r in rows] +
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

units = dict((s, [unit for unit in unit_list if s in unit]) for s in squares)

# peers = {}
# for s in squares:
#     temp = []
#     for u in units[s]:
#         temp = u + temp
#     peers[s] = set(temp) - set(s)
peers = dict((s, set(sum(units[s],[]) ) - set([s])) for s in squares)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '0' or '.' for empties
    :param squares: a list of square names -> 'A1', 'A2', etc..
    :param grid
    """
    chars = [c for c in grid if c in digits or c in '0.']
    assert(len(chars) == 81)
    return dict(zip(squares, chars))


def parse_grid(grid):
    """
    Convert grid into a dict of possible values, {square: digits}
    or return False is a contradiction is detected
    :param grid:
    :param squares"""
    possible_values = dict((s, digits) for s in squares)
    values_from_grid = grid_values(grid).items()

    for sq, digit in values_from_grid:
        # for every square and its provided value in the grid:
        #     propagate the constraint for this value through the grid
        if digit in digits:
            assign_success = assign(possible_values, sq, digit)
            if not assign_success:
                return False

    return possible_values


def assign(possible_values, sq, digit):
    """
    :param possible_values: {square: digits} where square is 'A1', 'A2', etc. and digits is '12343...'
    :param sq: the particular square
    :param digit:  the square's value
    :return: If updating every value was successful, return true
    """
    print 'assign:', sq, digit
    other_digits = possible_values[sq].replace(digit, '')
    if all([eliminate(possible_values, sq, other_digit) for other_digit in other_digits]):
        return possible_values
    else:
        return False


def eliminate(possible_values, sq, other_digit):
    """
    eliminates the parameter 'other_val' from possible_values for sq
    implements the rules to solve the sudoku:
    1. if a square has only one possible value, eliminate that value from all its peers
    2. if a unit is reduced to only one possible value for a single place, then that value should be assigned
    :param possible_values:
    :param sq:
    :param other_digit:
    """
    if other_digit not in possible_values[sq]:
        return possible_values
    else:
        possible_values[sq] = possible_values[sq].replace(other_digit, '')

    if len(possible_values[sq]) == 0:
        return False    # Contradiction. We can't have zero possible values for a square

    ## rule 1 applies here
    elif len(possible_values[sq]) == 1:
        # eliminate this value from possible_values of all peer squares
        digit_for_this_sq = possible_values[sq]

        print peers[sq]
        for peer in peers[sq]:
            print 'eliminating:', peer, digit_for_this_sq
            val = eliminate(possible_values, peer, digit_for_this_sq)
            if not val:
                return False

        # if not all( eliminate(possible_values, peer, digit_for_this_sq) for peer in peers[sq] ):
        #     return False

    ## rule 2 applies here
    # all_sq_in_units = itertools.chain.from_iterable(units[sq])
    # digit_places = [s for s in all_sq_in_units if other_digit in possible_values[s]]
    for unit in units[sq]:
        digit_places = [s for s in unit if other_digit in possible_values[s]]
        print other_digit, digit_places
        if len(digit_places) == 0:
            return False

        elif len(digit_places) == 1:
            if not assign(possible_values, digit_places[0], other_digit):
                return False

    return possible_values


def display(values):
    pass


values = parse_grid(grid_sample)
print values