Pegs: mastermind game and solvers
===============================

Program is launced through main.py

Configuration is done directly in the main.py script:

NUM_PEGS   = 4
NUM_COLORS = 6
SOLVER     = "elimination"
DEBUG      = True

Solver Types
==============

User Solver: "user"
------------------------
Asks for user input at each guess (numbers 1-NUM_COLORS separated by spaces)

Brute Solver: "brute"
------------------------
Tries all posible combinations, one by one.

Color Elimination: "elimination"
------------------------
Two step solve:
- Tries each color one by one, to figure out which ones are used
- Try all combinations of found colors
