# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We use naked twins in the eliminate step, where upon finding the naked twins in either a column or row or square unit, and for that matter in a diagonal, we knock our the naked twins from the peers in that unit (, where the peer is not finalized yet to a single digit value).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The Diagonal Sudoku constrained will be used in the elimination step where we can reduce the values of non-finalized boxes - within the particular associated diagonal, using the finalized values from the same diagonal. In addition on acheiving an all-single-digit config in the Sudoku, we check the validity of the diagonal constraint being acheived. The check can also be done when selecting one of possible values for a cell/box (out of the many applicable to that cell) to see if such a selection violates the diagonal constraint. This will cut down on the search.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py



