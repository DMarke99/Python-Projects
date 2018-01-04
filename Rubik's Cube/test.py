# Imports modules
from rubikscube.RubiksCube import RubiksCube
import copy

# Test 1; checks whether performing F R F' R' 6 times maps to the initial cube,
# whereas mapping 5 times doesn't

# Creates a new cube and scrambles it
r = RubiksCube()
r.scramble()

# Saves an unedited copy of it
before = copy.deepcopy(r)

# Performs F R F' R' 5 times
for i in range(5):
    r.move("F", "R", "F'", "R'")

# Checks if cubes are not equal
result = r != before
assert result

# Performs algorithm one more time
r.move("F", "R", "F'", "R'")

# Checks if cubes are equal
# If cubes are equal now and weren't equal previously then the test passes
assert result & (r == before)
print('moves verified')

# Test 2; Checks whether tkinter is installed properly

# Imports tkinter
import tkinter as tk

# Creates a new form
root = tk.Tk()

# If both tests pass the script should run uninterrupted
print('passed tests')
