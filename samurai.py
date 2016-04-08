## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

import os

#os.chdir("C:\\Users\\Kieran\\Documents\\Work\\CSC384\\Project\\")

def cross(A, B, c = ''):
    "Cross product of elements in A and elements in B."
    return [a+b+c for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits

id_var = 'a' #top left
square_a = cross(rows, cols, id_var)
unitlist_a = ([cross(rows, c, id_var) for c in cols] +
            [cross(r, cols, id_var) for r in rows] +
            [cross(rs, cs, id_var) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
            
id_var = 'b' #top right
square_b = cross(rows, cols, id_var)
unitlist_b = ([cross(rows, c, id_var) for c in cols] +
            [cross(r, cols, id_var) for r in rows] +
            [cross(rs, cs, id_var) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
            
id_var = 'c' #bottom left
square_c = cross(rows, cols, id_var)
unitlist_c = ([cross(rows, c, id_var) for c in cols] +
            [cross(r, cols, id_var) for r in rows] +
            [cross(rs, cs, id_var) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
            
id_var = 'd' #bottom right
square_d = cross(rows, cols, id_var)
unitlist_d = ([cross(rows, c, id_var) for c in cols] +
            [cross(r, cols, id_var) for r in rows] +
            [cross(rs, cs, id_var) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
            
def repl(c):
    a = b = 0
    s = ""
    if c[0] in 'ABCGHI' and c[1] in '123789':
        if c[0] in 'ABC':
            s += chr(ord(c[0]) + 6)
            a = 1
        elif c[0] in 'GHI':
            s += chr(ord(c[0]) - 6)
            a = 2
        if c[1] in '123':
            s += chr(ord(c[1]) + 6)
            b = 1
        elif c[1] in '789':
            s += chr(ord(c[1]) - 6)
            b = 2
    else: return c
    if a == 1 and b == 1:
        s += 'a'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s
            
id_var = '+'
square_mid = [repl(x) for x in cross(rows, cols, id_var)]
unitlist_mid = ([square_mid[x*9:x*9+9] for x in range(0,9)] +
                [square_mid[x::9] for x in range(0,9)] +
                [cross(rs, cs, id_var) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789') if not (rs in 'ABCGHI' and cs in '123789')])

all_squares = set(square_a + square_b + square_c + square_d + square_mid)
all_unitlists = unitlist_a + unitlist_b + unitlist_c + unitlist_d + unitlist_mid

units = dict((s, [u for u in all_unitlists if s in u])
             for s in all_squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in all_squares)
            

################ Parse a Grid ################

def parse_grid_samurai(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in all_squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values
    
def flatten(arr):
    return [x for sub in arr for x in sub]

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    a = flatten([x[:9] for x in grid[:9]])
    b = flatten([x[12:] for x in grid[:9]])
    c = flatten([x[:9] for x in grid[12:]])
    d = flatten([x[12:] for x in grid[12:]])
    mid = flatten([x[6:15] for x in grid[6:15]])
    chars = a + b + c + d + mid
    sqrs = square_a + square_b + square_c + square_d + square_mid
    assert len(chars) == 405
    return dict(zip(sqrs, chars))

################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

################ Display as 2-D grid ################

def display(values, sqr): #works for regular sudokus only
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in sqr)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[sqr[(ord(r) - 65) * 9 + int(c) - 1]].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    print()

def display_samurai(vals): #prints the squares in order of: top left, top right, bottom left, bottom right, middle. Note that the middle square overlaps with the other 4 and will contain duplicate values
    if not vals:
        print("Sudoku was not solved")
        return
    print("Top left:")
    display(vals, square_a)
    print("Top right:")
    display(vals, square_b)
    print("Bottom left:")
    display(vals, square_c)
    print("Bottom right:")
    display(vals, square_d)
    print("Middle:")
    display(vals, square_mid)

    
################ Search ################

def solve(grid): return search(parse_grid_samurai(grid))

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in all_squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in all_squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename, 'r').read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################  UNUSED

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in all_unitlists)

#####################################

if __name__ == '__main__':
    txt = input("input the name of the file containing the samurai sudoku to be solved (with path if necessary).\n")
    f = open(txt, 'r')
    samurai_grid = f.read().split('\n')
    ans = solve(samurai_grid)
    display_samurai(ans)
    

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/