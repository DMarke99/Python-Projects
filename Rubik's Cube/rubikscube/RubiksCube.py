from random import choices

# A class that encapsulates a Rubik's Cube
class RubiksCube:
    # Defines initialisation
    def __init__(self):

        # Sets each face to their initial color
        self.top = [['W' for i in range(3)] for i in range(3)]
        self.bot = [['Y' for i in range(3)] for i in range(3)]
        self.left = [['G' for i in range(3)] for i in range(3)]
        self.right = [['B' for i in range(3)] for i in range(3)]
        self.front = [['R' for i in range(3)] for i in range(3)]
        self.back = [['O' for i in range(3)] for i in range(3)]

        # Generates a list of all possible moves
        moves = ["R", "L", "U", "D", "F", "B", "M", "E", "S", "x", "y", "z"]
        addons = ["", "2", "'"]
        self.moveset = [move + addon for move in moves for addon in addons]

    # Prints out a net of the cube to the console
    def print(self):

        # Prints out top face
        for i in range(3):
            print(' ' * 12, end='')
            for j in self.top[i]:
                print(str(j).rjust(2), end='')
            print()

        # Prints out back, left, front and right face
        for i in range(3):
            for j in self.back[i]:
                print(str(j).rjust(2), end='')

            for j in self.left[i]:
                print(str(j).rjust(2), end='')

            for j in self.front[i]:
                print(str(j).rjust(2), end='')

            for j in self.right[i]:
                print(str(j).rjust(2), end='')

            print()

        # Prints out bottom face
        for i in range(3):
            print(' ' * 12, end='')
            for j in self.bot[i]:
                print(str(j).rjust(2), end='')
            print()

    # Performs the input moves on the rubix cube
    def move(self, *args):

        # Handles single moves
        if len(args) is 1:

            # Clockwise rotation of front face
            if args[0] is "F":
                for i in range(3):
                    self.top[2][i], self.left[2 - i][2], self.bot[0][2 - i], self.right[i][0] \
                        = self.left[2 - i][2], self.bot[0][2 - i], self.right[i][0], self.top[2][i]

                self.front[0][0], self.front[2][0], self.front[2][2], self.front[0][2] \
                    = self.front[2][0], self.front[2][2], self.front[0][2], self.front[0][0]

                self.front[0][1], self.front[1][0], self.front[2][1], self.front[1][2] \
                    = self.front[1][0], self.front[2][1], self.front[1][2], self.front[0][1]

            # Clockwise rotation of right face
            elif args[0] is "R":
                for i in range(3):
                    self.front[i][2], self.top[i][2], self.back[2 - i][0], self.bot[i][2] \
                        = self.bot[i][2], self.front[i][2], self.top[i][2], self.back[2 - i][0]

                self.right[0][0], self.right[2][0], self.right[2][2], self.right[0][2] \
                    = self.right[2][0], self.right[2][2], self.right[0][2], self.right[0][0]

                self.right[0][1], self.right[1][0], self.right[2][1], self.right[1][2] \
                    = self.right[1][0], self.right[2][1], self.right[1][2], self.right[0][1]

            # Clockwise rotation of top face
            elif args[0] is "U":
                for i in range(3):
                    self.front[0][i], self.left[0][i], self.back[0][i], self.right[0][i] \
                        = self.right[0][i], self.front[0][i], self.left[0][i], self.back[0][i]

                self.top[0][0], self.top[2][0], self.top[2][2], self.top[0][2] \
                    = self.top[2][0], self.top[2][2], self.top[0][2], self.top[0][0]

                self.top[1][0], self.top[2][1], self.top[1][2], self.top[0][1] \
                    = self.top[2][1], self.top[1][2], self.top[0][1], self.top[1][0]

            # Clockwise rotation of left face
            elif args[0] is "L":
                for i in range(3):
                    self.bot[i][0], self.front[i][0], self.top[i][0], self.back[2 - i][2] \
                        = self.front[i][0], self.top[i][0], self.back[2 - i][2], self.bot[i][0]

                self.left[0][0], self.left[2][0], self.left[2][2], self.left[0][2] \
                    = self.left[2][0], self.left[2][2], self.left[0][2], self.left[0][0]

                self.left[0][1], self.left[1][0], self.left[2][1], self.left[1][2] \
                    = self.left[1][0], self.left[2][1], self.left[1][2], self.left[0][1]

            # Clockwise rotation of back face
            elif args[0] is "B":
                for i in range(3):
                    self.left[2 - i][0], self.bot[2][2 - i], self.right[i][2], self.top[0][i] \
                        = self.top[0][i], self.left[2 - i][0], self.bot[2][2 - i], self.right[i][2]

                self.back[0][0], self.back[2][0], self.back[2][2], self.back[0][2] \
                    = self.back[2][0], self.back[2][2], self.back[0][2], self.back[0][0]

                self.back[0][1], self.back[1][0], self.back[2][1], self.back[1][2] \
                    = self.back[1][0], self.back[2][1], self.back[1][2], self.back[0][1]

            # Clockwise rotation of bottom face
            elif args[0] is "D":
                for i in range(3):
                    self.right[2][i], self.front[2][i], self.left[2][i], self.back[2][i] \
                        = self.front[2][i], self.left[2][i], self.back[2][i], self.right[2][i]

                self.bot[0][0], self.bot[2][0], self.bot[2][2], self.bot[0][2] \
                    = self.bot[2][0], self.bot[2][2], self.bot[0][2], self.bot[0][0]

                self.bot[1][0], self.bot[2][1], self.bot[1][2], self.bot[0][1] \
                    = self.bot[2][1], self.bot[1][2], self.bot[0][1], self.bot[1][0]

            # Rotation of the equatorial layer
            elif args[0] is "E":
                for i in range(3):
                    self.right[1][i], self.front[1][i], self.left[1][i], self.back[1][i] \
                        = self.front[1][i], self.left[1][i], self.back[1][i], self.right[1][i]

            # Rotation of the middle layer
            elif args[0] is "M":
                for i in range(3):
                    self.bot[i][1], self.front[i][1], self.top[i][1], self.back[2 - i][1] \
                        = self.front[i][1], self.top[i][1], self.back[2 - i][1], self.bot[i][1]

            # Rotation of the standing layer
            elif args[0] is "S":
                for i in range(3):
                    self.top[1][i], self.left[2 - i][1], self.bot[1][2 - i], self.right[i][1] \
                        = self.left[2 - i][1], self.bot[1][2 - i], self.right[i][1], self.top[1][i]

            # Rotates the whole cube in the same direction as R
            elif args[0] is "x":
                self.move("R", "M'", "L'")

            # Rotates the whole cube in the same direction as U
            elif args[0] is "y":
                self.move("U", "E'", "D'")

            # Rotates the whole cube in the same direction as F
            elif args[0] is "z":
                self.move("F", "S", "B'")

            # If move is a standard move with ' after, perform the opposite of the move
            # The opposite of any move is the same move applied twice
            elif len(args[0]) is 2 and args[0][1] is "'":
                for i in range(3):
                    self.move(args[0][0])

            # If move is a standard move with ' after, perform the move twice
            elif len(args[0]) is 2 and args[0][1] is "2":
                for i in range(2):
                    self.move(args[0][0])

            # Any other move is invalid
            else:
                print(args[0], ' is an invalid move')

        # If there are more than one move then perform all the moves in order
        else:

            # Checks if all the moves are valid moves
            if all(arg in self.moveset for arg in args):

                # Perform all moves if valid
                for arg in args:
                    self.move(arg)

            # Else print out all invalid moves
            else:
                invalid = [arg for arg in args if arg not in self.moveset]
                for move in invalid:
                    print(move, 'is not a valid move')

    # Scrambles Rubik's Cube
    def scramble(self):

        # Randomly selects with replacement 50 moves from the moveset
        moves = choices(self.moveset, k=50)

        # Performs moves on the cube
        for move in moves:
            self.move(move)

    # Defines equality for rubiks cubes
    def __eq__(self, other):

        # If all the faces are equal then the cubes are equal
        return ((self.top == other.top) &
                (self.bot == other.bot) &
                (self.front == other.front) &
                (self.back == other.back) &
                (self.left == other.left) &
                (self.right == other.right))





