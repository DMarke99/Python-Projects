import numpy as np
from enum import Enum
import random
import pygame


class Direction(Enum):

    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


class Node:

    def __init__(self, val, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev


class DoublyLinkedList:

    def __init__(self):
        self.head = self.tail = None
        self.curr = None
        self.length = 0

    def prepend(self, val):
        if self.head is None:
            self.head = self.tail = self.curr = Node(val)

        else:
            new_node = Node(val)
            self.head.prev = new_node
            new_node.next = self.head
            self.head = self.curr = new_node

        self.length += 1

    def append(self, val):
        if self.head is None:
            self.head = self.tail = self.curr = Node(val)

        else:
            new_node = Node(val)
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.length += 1

    def premove(self):
        if self.head is not None:
            self.head = self.head.next

            if self.head is None:
                self.tail = self.curr = None
            else:
                self.head.prev = None

            self.length -= 1

    def remove(self):
        if self.tail is not None:
            self.tail = self.tail.prev

            if self.tail is None:
                self.head = self.curr = None
            else:
                self.tail.next = None

            self.length -= 1

    def __len__(self):
        return self.length

    def first(self):
        if self.head is None:
            return None
        else:
            return self.head.val

    def last(self):
        if self.tail is None:
            return None
        else:
            return self.tail.val

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr is None:
            self.curr = self.head
            raise StopIteration

        else:
            val = self.curr.val
            self.curr = self.curr.next
            return val


# class to handle snake game dynamics
class SnakeGame:

    def __init__(self, row, col):
        self.row = row
        self.col = col

        assert row > 4, 'grid must have more than 4 rows'
        assert col > 4, 'grid must have more than 4 columns'
        assert type(row) == int
        assert type(col) == int

        self.reset()

    def reset(self):
        self.finished = False
        self.coords = np.zeros((self.row, self.col))

        # initialises snake
        x = np.random.randint(1, self.row-1)
        y = np.random.randint(1, self.col-1)

        self.snake = DoublyLinkedList()
        self.snake.append(np.array((x, y)))
        self.coords[x, y] = 1
        self.direction = random.choice(list(Direction))

        self.generate_reward()

    def generate_reward(self):
        if (self.coords != np.ones((self.row, self.col))).any():
            x = np.random.randint(0, self.row)
            y = np.random.randint(0, self.col)

            while self.coords[x, y] == 1:
                x = np.random.randint(0, self.row)
                y = np.random.randint(0, self.col)

            self.reward = np.array((x, y))

    def step(self):
        # does nothing if game is over
        if self.finished:
            return None

        # finds new position
        new_pos = self.snake.first() + np.array(self.direction.value)
        x, y = new_pos

        # determines if game is over
        if x >= self.row or x < 0 or y >= self.col or y < 0 or self.coords[x, y] == 1:
            self.finished = True
            return None

        if self.snake.length == self.row * self.col:
            self.finished = True

        # adds new position to snake
        self.snake.prepend(new_pos)
        self.coords[x, y] = 1

        # extends snake if snake eats reward
        if np.all(new_pos == self.reward):
            self.generate_reward()
        else:
            x1, y1 = self.snake.last()
            self.coords[x1, y1] = 0
            self.snake.remove()

    def __repr__(self):
        x, y = self.reward
        new_grid = self.coords
        new_grid[x, y] = 2

        return str(new_grid)

    # information vector to be used by agents
    def information(self):
        x, y = self.snake.first()

        # checks if tile immediately east is clear
        if x >= self.row-1 or self.coords[x+1, y] == 1:
            cl_e = 1
        else:
            cl_e = 0

        # checks if tile immediately west is clear
        if x <= 0 or self.coords[x-1, y] == 1:
            cl_w = 1
        else:
            cl_w = 0

        # checks if tile immediately north is clear
        if y <= 0 or self.coords[x, y-1] == 1:
            cl_n = 1
        else:
            cl_n = 0

        # checks if tile immediately south is clear
        if y >= self.col-1 or self.coords[x, y+1] == 1:
            cl_s = 1
        else:
            cl_s = 0

        # gets distance from walls
        d_n = x / (self.col - 1)
        d_e = y / (self.row - 1)
        d_s = 1 - x / (self.col - 1)
        d_w = 1 - y / (self.row - 1)

        # gets direction of food
        x1, y1 = self.reward
        food_x = np.sign(x - x1)
        food_y = np.sign(y - y1)

        # returns all information as a vector to be used in prediction of the best move
        return np.array([cl_n, cl_e, cl_s, cl_w, d_n, d_e, d_s, d_w, food_x, food_y])

    def score(self):
        return len(self.snake) - 1


# SliderRenderer renders a Slider object
class SnakeRenderer:

    # initialises renderer
    def __init__(self, row, col, block_size=20):

        # sets initial slider and the slider it is compared to to determine completion
        self.snake = SnakeGame(row, col)
        self.row = row
        self.col = col
        self.block_size = block_size

        # sets the display size to the appropriate size
        self.display = (row * block_size, col * block_size)

        # initializes pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.display)
        pygame.display.set_caption('Snake - Score: 0')

        # sets font
        self.render_grid()
        self.event_loop()

    # define the event loop
    def event_loop(self):
        pygame.display.flip()

        # Event loop
        while True:
            if self.snake.finished:
                pygame.quit()
                quit()

            curr_dir = self.snake.direction

            # gets all recent events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.snake.finished:
                    pygame.quit()
                    quit()

                # changes the snakes direction if it isn't doing a 180 degree turn
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if curr_dir != Direction.S:
                            self.snake.direction = Direction.N

                    if event.key == pygame.K_DOWN:
                        if curr_dir != Direction.N:
                            self.snake.direction = Direction.S

                    if event.key == pygame.K_RIGHT:
                        if curr_dir != Direction.W:
                            self.snake.direction = Direction.E

                    if event.key == pygame.K_LEFT:
                        if curr_dir != Direction.E:
                            self.snake.direction = Direction.W

            self.snake.step()
            pygame.time.wait(2)

            self.render_grid()
            pygame.display.set_caption('Snake - Score: {}'.format(self.snake.score()))
            pygame.display.flip()

    # renders the grid
    def render_grid(self):
        # blacks out the screen
        self.screen.fill((0, 0, 0))

        # loops over the body of the snake and colors in snake in alternating shades of green
        col1 = -1
        for i, j in self.snake.snake:
            col1 += 1
            if col1 % 2 == 0:
                pygame.draw.rect(self.screen, (0, 120, 0), [self.block_size * x for x in [i, j, 1, 1]])
            else:
                pygame.draw.rect(self.screen, (0, 110, 0), [self.block_size * x for x in [i, j, 1, 1]])

        # draws reward
        x1, y1 = self.snake.reward
        pygame.draw.rect(self.screen, (150,30,30), [self.block_size * i for i in [x1, y1, 1, 1]])

        # draws head
        x, y = self.snake.snake.first()
        d1, d2 = self.snake.direction.value

        head_center = np.array([self.block_size * i for i in [x+0.5, y+0.5]])
        pygame.draw.rect(self.screen, (0, 100, 0), [self.block_size * i for i in [x, y, 1, 1]])

        # draws eyes
        eye1 = head_center + np.array([d1 - d2, d1 + d2]) * (self.block_size / 3)
        rect1 = pygame.Rect(0, 0, 0, 0)
        rect1.size = (self.block_size/3, self.block_size/3)
        rect1.center = tuple(eye1)
        pygame.draw.rect(self.screen, (150, 150, 30), rect1)

        eye2 = head_center + np.array([d1 + d2, -d1 + d2]) * (self.block_size / 3)
        rect2 = pygame.Rect(0, 0, 0, 0)
        rect2.size = (self.block_size/3, self.block_size/3)
        rect2.center = tuple(eye2)
        pygame.draw.rect(self.screen, (150, 150, 30), rect2)


# if script directly run create a new game
if __name__ == "__main__":

    S = SnakeRenderer(40, 40, 16)


