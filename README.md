# samurai-sudoku-solver
Samurai Sudoku solver in Python for CSC384H Project

# How To Run The Code
~: Indicates command prompt
>: Indicates python command prompt

# samurai.py
This is our solver, when running this program as __main__ it solves any user fed samurai sudoku puzzle given in the format exampled by the files in our tests/ folder.

~ python samurai.py (Note: this can be used if python refers to a 3.x version)

OR

~ python3 samurai.py

Once the program runs, you will be prompted to give a path to a Samurai Sudoku puzzle. We have 8 hand-made puzzles available to you in the tests/ folder. An example input is:

> ./tests/easy1.txt

# analyse.py
This program is used to analyse our solvers solution to randomly generated Samurai Sudoku puzzles. It is currently set to analyse only 100 different puzzles. However, in our testing we usually run it on 1,000 to 10,000 test cases. The program will output 5 csv files containing data on counts of which squares were initially assigned values in solved Samurai Sudoku puzzles.

~ python analyse.py 

OR

~ python3 analyse.py

# imaging.py
This program is used to create the hashmaps seen in the project report and in the heatmaps/ folder. This program works by feeding it a path to a specifically formatted .csv file, the program then generates a heatmap from that file and outputs to screen.
*Note: Unfortunately, the heatmap library used is incompatible with cdf computers and require external libraries to use. Since the point of the program is just to generate heatmaps for data visualization for the report it shouldn't be considered a main feature of our assignment. You could instead find all the same conclusions from the data in the .csv files available in the data/ folder. This program just provides a nice visualization of that data.

~ python imaging.py PATH_TO_CSV_FILE (must be python 2.7X)






