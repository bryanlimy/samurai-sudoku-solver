import samurai
import math
import csv
import signal
import time

from sudoku import *
from collections import Counter


################ Author's Notes ################

# Grid's are stored in two ways: 
#   1. As a dictionary where the keys represent squares on 
#      the grid and follow the format:
#           [A-I][1-9] 
#           Examples. B4, A3, I9
#      and the values of the dictionary represent what is assigned to that square.
#   2. As an 81 character list, where each character represents what is assigned
#      to that square on grid the index of the list corresponds to which square
#      we are on the index increases from left-right and from top-bottom. 
#           Examples. A3 -> index 2, B1 -> index 9


################ Puzzle Constructor ################

overlapping_squares = ['A1', 'A2', 'A3', 'A7', 'A8', 'A9',
                       'B1', 'B2', 'B3', 'B7', 'B8', 'B9',
                       'C1', 'C2', 'C3', 'C7', 'C8', 'C9',
                       'G1', 'G2', 'G3', 'G7', 'G8', 'G9',
                       'H1', 'H2', 'H3', 'H7', 'H8', 'H9',
                       'I1', 'I2', 'I3', 'I7', 'I8', 'I9']

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
       Note: the resulting puzzle is not guaranteed to be solvable. 
             Some have multiple solutions."""
    values = dict((s, digits) for s in squares)

    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N) ## Give up and make a new puzzle

def random_middle_puzzle(N=17, grid='.'*81):
    """Make a random middle puzzle with N or more assignments. Restart on contradictions.
       Note: the resulting puzzle is not guaranteed to be solvable. 
             Some have multiple solutions."""
    values = dict((s, digits) for s in squares)

    for s in overlapping_squares:
        if grid[grid_index(s)] != '.':
            assign(values, s, grid[grid_index(s)])

    ds = [values[s] for s in squares if len(values[s]) == 1]
    if len(ds) >= N and len(set(ds)) >= 8:
        return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)

    for s in shuffled(list(set(squares)-set(overlapping_squares))):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_middle_puzzle(N, grid) ## Give up and make a new puzzle

def random_samurai_puzzle(N_a=17, N_b=17, N_c=17, N_d=17, N_plus=17):
    grid_a = random_puzzle(N_a)
    grid_b = random_puzzle(N_b)
    grid_c = random_puzzle(N_c)
    grid_d = random_puzzle(N_d)
    grid_plus = (grid_a[grid_index('G7'):grid_index('G9')+1] + '...' + grid_b[grid_index('G1'):grid_index('G3')+1]
               + grid_a[grid_index('H7'):grid_index('H9')+1] + '...' + grid_b[grid_index('H1'):grid_index('H3')+1]
               + grid_a[grid_index('I7'):grid_index('I9')+1] + '...' + grid_b[grid_index('I1'):grid_index('I3')+1]
               + '.'*9*3
               + grid_c[grid_index('A7'):grid_index('A9')+1] + '...' + grid_d[grid_index('A1'):grid_index('A3')+1]
               + grid_c[grid_index('B7'):grid_index('B9')+1] + '...' + grid_d[grid_index('B1'):grid_index('B3')+1]
               + grid_c[grid_index('C7'):grid_index('C9')+1] + '...' + grid_d[grid_index('C1'):grid_index('C3')+1])
    
    if not check_middle_puzzle(grid_plus):
        return random_samurai_puzzle(N_a, N_b, N_c, N_d, N_plus)
    grid_plus = random_middle_puzzle(N_plus, grid_plus)
    
    samurai_grid = [grid_a[grid_index('A1'):grid_index('A9')+1].replace('.', '0') + '...' + grid_b[grid_index('A1'):grid_index('A9')+1].replace('.', '0'),
                    grid_a[grid_index('B1'):grid_index('B9')+1].replace('.', '0') + '...' + grid_b[grid_index('B1'):grid_index('B9')+1].replace('.', '0'),
                    grid_a[grid_index('C1'):grid_index('C9')+1].replace('.', '0') + '...' + grid_b[grid_index('C1'):grid_index('C9')+1].replace('.', '0'),
                    grid_a[grid_index('D1'):grid_index('D9')+1].replace('.', '0') + '...' + grid_b[grid_index('D1'):grid_index('D9')+1].replace('.', '0'),
                    grid_a[grid_index('E1'):grid_index('E9')+1].replace('.', '0') + '...' + grid_b[grid_index('E1'):grid_index('E9')+1].replace('.', '0'),
                    grid_a[grid_index('F1'):grid_index('F9')+1].replace('.', '0') + '...' + grid_b[grid_index('F1'):grid_index('F9')+1].replace('.', '0'),
                    grid_a[grid_index('G1'):grid_index('G9')+1].replace('.', '0') + grid_plus[grid_index('A4'):grid_index('A6')+1].replace('.', '0') + grid_b[grid_index('G1'):grid_index('G9')+1].replace('.', '0'),
                    grid_a[grid_index('H1'):grid_index('H9')+1].replace('.', '0') + grid_plus[grid_index('B4'):grid_index('B6')+1].replace('.', '0') + grid_b[grid_index('H1'):grid_index('H9')+1].replace('.', '0'),
                    grid_a[grid_index('I1'):grid_index('I9')+1].replace('.', '0') + grid_plus[grid_index('C4'):grid_index('C6')+1].replace('.', '0') + grid_b[grid_index('I1'):grid_index('I9')+1].replace('.', '0'),
                    '......' + grid_plus[grid_index('D1'):grid_index('D9')+1].replace('.', '0') + '......',
                    '......' + grid_plus[grid_index('E1'):grid_index('E9')+1].replace('.', '0') + '......',
                    '......' + grid_plus[grid_index('F1'):grid_index('F9')+1].replace('.', '0') + '......',
                    grid_c[grid_index('A1'):grid_index('A9')+1].replace('.', '0') + grid_plus[grid_index('G4'):grid_index('G6')+1].replace('.', '0') + grid_d[grid_index('A1'):grid_index('A9')+1].replace('.', '0'),
                    grid_c[grid_index('B1'):grid_index('B9')+1].replace('.', '0') + grid_plus[grid_index('H4'):grid_index('H6')+1].replace('.', '0') + grid_d[grid_index('B1'):grid_index('B9')+1].replace('.', '0'),
                    grid_c[grid_index('C1'):grid_index('C9')+1].replace('.', '0') + grid_plus[grid_index('I4'):grid_index('I6')+1].replace('.', '0') + grid_d[grid_index('C1'):grid_index('C9')+1].replace('.', '0'),
                    grid_c[grid_index('D1'):grid_index('D9')+1].replace('.', '0') + '...' + grid_d[grid_index('D1'):grid_index('D9')+1].replace('.', '0'),
                    grid_c[grid_index('E1'):grid_index('E9')+1].replace('.', '0') + '...' + grid_d[grid_index('E1'):grid_index('E9')+1].replace('.', '0'),
                    grid_c[grid_index('F1'):grid_index('F9')+1].replace('.', '0') + '...' + grid_d[grid_index('F1'):grid_index('F9')+1].replace('.', '0'),
                    grid_c[grid_index('G1'):grid_index('G9')+1].replace('.', '0') + '...' + grid_d[grid_index('G1'):grid_index('G9')+1].replace('.', '0'),
                    grid_c[grid_index('H1'):grid_index('H9')+1].replace('.', '0') + '...' + grid_d[grid_index('H1'):grid_index('H9')+1].replace('.', '0'),
                    grid_c[grid_index('I1'):grid_index('I9')+1].replace('.', '0') + '...' + grid_d[grid_index('I1'):grid_index('I9')+1].replace('.', '0')]
    
    init_square_count = {}
    for s in squares:
        init_square_count[s] = 0
    counts = {}
    counts['a'] = count_initialized_squares(grid_a, init_square_count.copy())
    counts['b'] = count_initialized_squares(grid_b, init_square_count.copy())
    counts['c'] = count_initialized_squares(grid_c, init_square_count.copy())
    counts['d'] = count_initialized_squares(grid_d, init_square_count.copy())
    counts['+'] = count_initialized_squares(grid_plus, init_square_count.copy())

    return samurai_grid, counts


################ Puzzle Helpers ################

square_indices_map = {} # Lazy map of square indices
index_squares_map = {} # Lazy map of index squares

def grid_index(square):
    """Return the index to a list representation of a grid 
       associated with given `square`. 
       Ex. A2 -> 1"""
    if square not in square_indices_map: 
        square_indices_map[square] = ((ord(square[0])-ord('A'))*9 + (int(square[1])-1))
    return square_indices_map[square]

def index_to_square(index):
    """Return the square associated with given `index`
       of a grid represented as a list
       Ex. 1 -> A2"""
    if index not in index_squares_map:
        index_squares_map[index] = chr(math.floor(index/9)+ord('A')) + str(index%9+1)
    return index_squares_map[index]

def count_initialized_squares(grid, count_map):
    for i in range(len(grid)):
        if grid[i] != '.':
            count_map[index_to_square(i)] += 1
    return count_map

def check_middle_puzzle(grid='.'*81):
    values = dict((s, digits) for s in squares)
    for s in squares:
        if grid[grid_index(s)] != '.':
            if not assign(values, s, grid[grid_index(s)]):
                return False
    return True


################ Data Handlers ################

def write_counter_to_database(name, counter):
    writer = csv.writer(open(name, 'w'))
    writer.writerow(['Y-Axis', 'X-Axis' , 'Number of Hits'])
    for key, value in counter.items():
        writer.writerow([key[0], key[1] , value])


################ Testing ################

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

# Change behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

# Initialize Counters for each Sudoku grid 
a = Counter()
b = Counter()
c = Counter()
d = Counter()
plus = Counter()

if __name__ == '__main__':
    success_counter = 0
    timeout_counter = 0
    num_loops = 10000

    for i in range(num_loops):
        # Start timer. Once 10 seconds are over, a SIGALRM signal is sent.
        signal.alarm(10)   

        # This try/except loop ensures that 
        #   you'll catch TimeoutException when it's sent.
        try:
            samurai_grid, counts = random_samurai_puzzle(17, 17, 17, 17, 17)
            ans = samurai.solve(samurai_grid)

            if ans:
                success_counter += 1
                a.update(counts['a'])
                b.update(counts['b'])
                c.update(counts['c'])
                d.update(counts['d'])
                plus.update(counts['+'])
                # samurai.display_samurai(ans)
        except TimeoutException:
            timeout_counter += 1
            print("timout", i)
            continue # continue the for loop if solving takes more than 10 second
        else:
            print("non-timeout", i)
            # Reset alarm
            signal.alarm(0)


    print('#'*100)
    print("Successes:     ", success_counter)
    print("Failures:      ", num_loops-success_counter)
    print("Success Ratio: ", success_counter/num_loops)
    print("Timouts:       ", timeout_counter)
    print("Timout Ratio:  ", timeout_counter/num_loops)
    print('#'*100)

    write_counter_to_database('grid_a_success_hits.csv', a)
    write_counter_to_database('grid_b_success_hits.csv', b)
    write_counter_to_database('grid_c_success_hits.csv', c)
    write_counter_to_database('grid_d_success_hits.csv', d)
    write_counter_to_database('grid_plus_success_hits.csv', plus)

## References used:
## Various StackOverFlow QA's