def checker(solution):
    # replace dot ".", new line "\n" and "\r" from string
    solution = solution.replace(".", "").replace("\n", "").replace("\r", "");

    # check if solution has correct amount of values
    if len(solution) != 369:
        print("Incorrect length, solution is incorrect")
        return False

    sudoku1 = sudoku2 = sudoku3 = sudoku4 = sudoku5 = [[[None] * 9] * 9]
    samurai = [sudoku1, sudoku2, sudoku3, sudoku4, sudoku5]
    counter = 0
    current = 0
    for index in range(len(solution)):
        if index < 108:
            if counter < 9:
                samurai[current][counter] = solution[index]
                counter += 1
            else:
                counter = 0


if __name__ == '__main__':
    actual = input("Insert the Samurai Sudoku:")
    print("input: " + actual)
    checker(actual)