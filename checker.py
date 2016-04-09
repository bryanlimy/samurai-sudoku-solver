# define global variable
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits


def checker(values, sqrs):
    """
    Given the values and squares of a samurai sudoku
    Return True if its a valid samurai sudoku, False otherwise
    """
    # samurai sudoku in the order of top left, top right, bottom left,
    # bottom right, middle
    samurai = []
    # get all sudokus and insert into samurai
    for sqr in sqrs:
        samurai.append(generate_sudoku(values, sqr))

    for sudoku in samurai:
        if not check_sudoku(sudoku):
            print("Invalid Samurai Sudoku.")
            return False

    corners_coordinate = [
        [[samurai[0], [6, 6]], [samurai[4], [0, 0]]],
        [[samurai[1], [6, 0]], [samurai[4], [0, 6]]],
        [[samurai[2], [0, 6]], [samurai[4], [6, 0]]],
        [[samurai[3], [0, 0]], [samurai[4], [6, 6]]]
    ]
    # check overlapped corners
    for corner in corners_coordinate:
        if not check_corners(corner[0], corner[1]):
            print("Invalid Samurai Sudoku")
            return False

    print("Solution has been verified, valid Samurai Sudoku.")
    return True

def check_sudoku(sudoku):
    """
    Given the sudoku
    Check each uniqueness of each sub box, each row and each column
    Return True if sudoku is valid, False otherwise
    """
    # coordinates of the top left corner for all boxes in a suduko
    box_coordinate = [
        [[0, 0], [0, 3], [0, 6]],
        [[3, 0], [3, 3], [3, 6]],
        [[6, 0], [6, 3], [6, 6]]
    ]
    # check each box in sudoku is unique
    for row in box_coordinate:
        for col in row:
            box = get_box(sudoku, col[0], col[1])
            if not check_unique_list(matrix2list(box)):
                return False

    # check each row and column in sudoku is unique
    for row in sudoku:
        if not check_unique_list(row):
            return False

    # check each column in sudoku is unique
    for col in range(9):
        col_list = []
        for row in range(9):
            col_list.append(sudoku[row][col])
        if not check_unique_list(col_list):
            return False

    return True


def check_corners(box1, box2):
    """
    Given the sudokus and coordinates
    Return True if corners are equal, False otherwise
    """
    box1_list = get_box(box1[0], box1[1][0], box1[1][1])
    box2_list = get_box(box2[0], box2[1][0], box2[1][1])
    return box1_list == box2_list


def check_unique_list(input):
    """
    Given a list, check if it is equal to a sorted list containing 1-9
    Return True if the given list is unique, False otherwise
    """
    # convert list string into list of int and sort it
    int_list = list(map(int, input))
    int_list.sort()
    return int_list == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def generate_sudoku(values, sqr):
    """
    Return a sudoku with the given values and square
    Return the sudoku in a 2D grid format
    """
    sudoku = [[None]*9]*9
    i = 0
    for r in rows:
        sudoku[i] = [values[sqr[(ord(r) - 65) * 9 + int(c) - 1]] for c in cols]
        i += 1
        # if sudoku has reached 9 rows, point samurai to the next sudoku
        if i == 9:
            i = 0
    return sudoku


def get_box(sudoku, row, col):
    """
    Return the box with the given coordinate of the top left corner value in
    the sudoku
    Return a 3 by 3 grid
    """
    box = [[]*3]*3
    count = 3
    for i in range(len(box)):
        box[i] = sudoku[row][col:col+3]
        row += 1
    return box


def matrix2list(matrix):
    """
    Given a two dimensional matrix, return a flatten list
    Return a flatten list
    """
    return [val for sublist in matrix for val in sublist]
