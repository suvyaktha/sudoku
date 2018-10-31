assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def diagonals(A, B):
    assert len(A) == len(B), "A and B must be strings of same length"
    diag1 = []
    diag2 = []
    slen = len(A)
    for ii in range(0, len(A)):
        diag1.append(A[ii]+B[ii])
        diag2.append(A[ii]+B[slen-ii-1])
    return [diag1, diag2]





rows = 'ABCDEFGHI'
cols = '123456789'
row_units = [cross(r, cols) for r in rows]
boxes = cross(rows, cols)
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diags = diagonals(rows, cols)
unitlist = row_units + column_units + square_units + diags
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def check_diagonal_constraint(values):
    for diag in diags:
        vdict = {values[bx]: bx for bx in diag}
        #print("Vdict : ", vdict)
        if len(vdict) != 9:
            return False
    return values

def precheck_diagonal_constraint(values):
    for diag in diags:
        if all(len(values[bx]) == 1 for bx in diag):
            vdict = {values[bx]: bx for bx in diag}
            if len(vdict) != 9:
                return False
    return values

def eliminate_in_diagonals(values):
    for diag in diags:
        solved_values = [box  for box in diag if len(values[box]) == 1]
        ##print("Xyz: ", solved_values)
        for box in solved_values:
            for peer_box in diag:
                if (peer_box != box) and (len(values[peer_box]) != 1):
                    assign_value(values, peer_box, values[peer_box].replace(values[box], ''))
    return values

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def add_double_digit_box(double_digit_dict, ddigit_val, ddigit_box):
    if (ddigit_val in double_digit_dict) :
        double_digit_dict[ddigit_val].append(ddigit_box)
    else:
        double_digit_dict[ddigit_val] = [ddigit_box]

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find all instances of naked twins
        # track all boxes with double digits, maintain them in a dict with ddigit:list_of_boxes
        double_digit_boxes = {}
        for box in unit:
            if (len(values[box]) == 2):
                add_double_digit_box(double_digit_boxes, values[box], box)
        # Eliminate the naked twins as possibilities for their peers
        #print(double_digit_boxes)
        for ddgt, box_list in double_digit_boxes.items():
            if (len(box_list) == 2):
                for box in unit:
                    if (box not in box_list) and (len(values[box]) > 1):
                        rval = values[box].replace(ddgt[0], '').replace(ddgt[1], '')
                        ### print("attempting to replace value ", values[box], " for box ", box, " with ", rval)
                        assign_value(values, box, rval)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        ###values = eliminate_in_diagonals(values) ## as diagonal units are added to unitlist, the eliminate above
        ## shall take care of this.
        ## Do the next level elimination using naked_twins
        values = naked_twins(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return check_diagonal_constraint(values) ## Solved only if diag contraint is also met!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        ##new_sudoku[s] = value
        assign_value(new_sudoku, s, value)
        ## after selectig a value for the box, see if this violates the diagonal constraint before next search-reduce..
        ## if it violates, continue to pick the next feasible selection
        if precheck_diagonal_constraint(new_sudoku):
            attempt = search(new_sudoku)
            if attempt:
                return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return(search(grid_values(grid)))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
