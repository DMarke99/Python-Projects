from random import sample


# creates a slider class that performs the function of a slider
class Slider:

    # initialises a slider
    def __init__(self, width: int, height: int, random: bool):

        # sets minimum width and height to 4
        if (height < 4) or (width < 4):
            raise ValueError('Dimensions too small')

        # set object parameters
        self.vals = {}
        self.width = width
        self.height = height
        self.moves = 0
        self.blank_loc = (width, height)

        # sets the numbers on each of the faces of the tiles
        for i in range(width):
            for j in range(height):
                self.vals[i+1, j+1] = j * width + i + 1

        self.vals[width, height] = 0

        # randomises the board to a solvable combination
        # all solutions have even parity; require an even number of transpositions to reach the solved state
        if random:
            self.shuffle()

    # defines the Von-Neumann neighbourhood of a point; all points with Manhattan distance 1
    def neighbourhood(self, x: int, y: int):

        # nbhd takes the coordinate and maps them to the value at the point
        nbhd = {}

        # if the point isn't on the grid return blank dictionary
        if x < 1 or y < 1 or y > self.height or x > self.width:
            return nbhd

        # checks the validity of all 4 points before adding them to the neighbourhood
        # top point
        if x + 1 <= self.width:
            nbhd[x + 1, y] = self.vals[x + 1, y]

        # right point
        if y + 1 <= self.height:
            nbhd[x, y + 1] = self.vals[x, y + 1]

        # bottom point
        if x - 1 > 0:
            nbhd[x - 1, y] = self.vals[x - 1, y]

        # left point
        if y - 1 > 0:
            nbhd[x, y - 1] = self.vals[x, y - 1]

        return nbhd

    # defines Manhattan distance for points
    def dist(x1: int, y1: int, x2: int, y2: int):
        return abs(x1 - x2) + abs(y1 - y2)

    # performs a move in the sliding tile game
    def move(self, x: int, y: int):

        if Slider.dist(x, y, self.blank_loc[0], self.blank_loc[1]) == 1:
            self.vals[self.blank_loc] = self.vals[x, y]
            self.vals[x, y] = 0
            self.moves = self.moves + 1
            self.blank_loc = (x, y)

    # shuffles the board
    def shuffle(self):
        for _ in range(7 * self.height * self.width + 1):
            loc = sample(list(Slider.neighbourhood(self, self.blank_loc[0],self.blank_loc[1]).keys()), 1)[0]
            self.vals[self.blank_loc] = self.vals[loc]
            self.vals[loc] = 0
            self.blank_loc = loc

    # prints the current board to the console
    def print(self):
        for j in range(self.height):
            for i in range(self.width):
                print(self.vals[i+1, j+1], end=" ")
            print()
