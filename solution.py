
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                  ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    for unit in unitlist:
        twins = find_twins(unit, values)
#        if twins:
#            print('naked twins found: {}\n'.format(twins))
#            display(values)
        for t1, t2 in twins:
            twin_values = values[t1]
            for box in [b for b in unit if b != t1 and b != t2]:
                values[box] = values[box].replace(twin_values[0], '').replace(twin_values[1], '')
        
    return values

def find_twins(unit, values):
    twins = []
    remaining = unit.copy()
    while len(remaining) > 1:
        box = remaining.pop(0)
        if len(values[box]) == 2:
            twins_of_box = [t for t in remaining if values[t] == values[box]]
            if twins_of_box:
                twins.append((box, twins_of_box[0]))
    
    return twins

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for box in (box for box in values if len(values[box]) == 1):
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box], '')
                
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    all_digits = '123456789'
    
    for unit in unitlist:
        for d in all_digits:
            boxes_containing_d = [box for box in unit if d in values[box]]
            if len(boxes_containing_d) == 1:
                values[boxes_containing_d[0]] = d


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        # unsolvable
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = [box for box in values if len(values[box]) > 1]
    if not unsolved_boxes:
        return values
    
    min_len, box = min([(len(values[box]), box) for box in unsolved_boxes])
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[box]:
        new_values = values.copy()
        new_values[box] = v
        result = search(new_values)
        if result:
            return result


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
#    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#    display(grid2values(diag_sudoku_grid))
#    result = solve(diag_sudoku_grid)
#    display(result)
#
#    try:
#        import PySudoku
#        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
#
#    except SystemExit:
#        pass
#    except:
#        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    
    
    diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid2values(diagonal_grid)
    print('\n\nbefore:\n')
    display(values)
    #print('\npeers of A1: {}'.format(peers['A1']))
    #
    #eliminate(values)
    #print('\n\nafter eliminate:\n')
    #display(values)
    
    solution = solve(diagonal_grid)
    print('\n\nafter:\n')
    if solution:
        display(solution)
    else:
        print('no solution')
