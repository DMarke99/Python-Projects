import numpy as np
import pygame
from snake import SnakeGame, Direction
from multiprocessing import Pool


# agents which control the snake's movement
class Agent:

    def __init__(self, shape=(10, 12, 4), size=(20, 20)):
        self.NeuralNetwork = NeuralNetwork(shape)
        self.row, self.col = size
        self.game = SnakeGame(self.row, self.col)

    # performs a move in the game according to the agent's recommendation
    def move(self):

        # predicts best move with neural net
        X = self.game.information()
        y = self.NeuralNetwork.predict(X)

        # gets moves in rank order
        move_args = np.argsort(y)
        moves = list(Direction)

        # if selected move turns 180 degrees pick the next best move
        selected_move = moves[move_args[-1]]
        if np.linalg.norm(np.array(selected_move.value) + np.array(self.game.direction.value)) == 0:
            selected_move = moves[move_args[-2]]

        self.game.direction = selected_move
        self.game.step()


# neural net class used for prediction of moves
class NeuralNetwork:

    def __init__(self, shape):
        self.weights = []
        self.shape = shape

        for i in range(len(shape)-1):
            self.weights.append(np.random.randn(shape[i+1], shape[i]+1))

    def predict(self, X):
        y = X

        for w in self.weights:
            if len(np.shape(y)) == 1:
                y = y.reshape(np.shape(y)[0], 1)

            ones = np.ones(np.shape(y)[1])
            y = np.matmul(w, np.append(ones, y))
            y = 1 / (1 + np.exp(-y))

        return y


# AgentRenderer renders a game for an agent
class AgentRenderer:

    # initialises renderer
    def __init__(self, agent, block_size=15, cap=-1):

        self.agent = agent
        self.block_size = block_size
        self.cap = cap
        self.time = 0

        # initializes pygame and display
        self.display = (agent.row * block_size, agent.col * block_size)
        pygame.init()
        self.screen = pygame.display.set_mode(self.display)
        pygame.display.set_caption('Snake - Score: 0')

        # enters event loop
        self.event_loop()

    # define the event loop
    def event_loop(self):
        self.render_grid()
        pygame.display.flip()

        # Event loop
        while True:

            clock_time = pygame.time.get_ticks()
            self.time += 1

            if self.agent.game.finished or self.time == self.cap:
                pygame.quit()
                break

            # gets all recent events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.agent.game.finished:
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.agent.game.finished = True
                    break

            self.agent.move()
            pygame.time.wait(5)

            self.render_grid()
            pygame.display.set_caption('Snake - Score: {}'.format(self.agent.game.score()))
            pygame.display.flip()

            while pygame.time.get_ticks() - clock_time < 50:
                pass

    # renders the grid
    def render_grid(self):
        # blacks out the screen
        self.screen.fill((0, 0, 0))

        col1 = -1
        # loops over the body of the snake and colors in snake
        for i, j in self.agent.game.snake:
            col1 += 1
            if col1 % 2 == 0:
                pygame.draw.rect(self.screen, (0, 120, 0), [self.block_size * x for x in [i, j, 1, 1]])
            else:
                pygame.draw.rect(self.screen, (0, 110, 0), [self.block_size * x for x in [i, j, 1, 1]])

        # draws reward
        x1, y1 = self.agent.game.reward
        pygame.draw.rect(self.screen, (150,30,30), [self.block_size * i for i in [x1, y1, 1, 1]])

        # draws head
        x, y = self.agent.game.snake.first()
        d1, d2 = self.agent.game.direction.value

        head_center = np.array([self.block_size * i for i in [x+0.5, y+0.5]])
        pygame.draw.rect(self.screen, (0, 100, 0), [self.block_size * i for i in [x, y, 1, 1]])

        # draws eyes
        eye1 = head_center + np.array([d1 - d2, d1 + d2]) * (self.block_size/3)
        rect1 = pygame.Rect(0, 0, 0, 0)
        rect1.size = (self.block_size/3, self.block_size/3)
        rect1.center = tuple(eye1)
        pygame.draw.rect(self.screen, (150, 150, 30), rect1)

        eye2 = head_center + np.array([d1 + d2, -d1 + d2]) * (self.block_size/3)
        rect2 = pygame.Rect(0, 0, 0, 0)
        rect2.size = (self.block_size/3, self.block_size/3)
        rect2.center = tuple(eye2)
        pygame.draw.rect(self.screen, (150, 150, 30), rect2)


# class that represents a population of agents
class Population:

    def __init__(self,
                 size=150,
                 population_cutoff=0.5):

        # saves population settings
        self.size = size
        self.population_cutoff = population_cutoff
        self.move_cap = 1000
        self.trials = 10
        self.trial_no = 0
        self.epsilon = 0.1

        # initialises a random population of agents
        self.agents = [Agent() for _ in range(size)]

    # simulates a population of agents, breeding the top agents and destroying the bottom agents
    def train(self, trials=1):
        self.trial_no += 1

        for t in range(trials):

            # generates score for each agent in parallel
            pool = Pool(3)
            scores = pool.map(self.fitness, self.agents)
            print("Trial", self.trial_no, end=" | ")
            print("Avg Score:", np.round(sum(scores) / len(self.agents), 3), end=" | ")
            pool.close()
            pool.join()

            # culls all agents above cutoff
            selected = np.argsort(scores)[int(self.size * self.population_cutoff):]
            print("Best Performance:", np.round(scores[selected[-1]], 3))

            # breeds agents that were selected randomly to fill out rest of the population
            breeding_pool = [self.agents[i] for i in selected]

            children = [self.reproduce(
                breeding_pool[np.random.randint(0, len(breeding_pool))],
                breeding_pool[np.random.randint(0, len(breeding_pool))])
                for _ in range(int((self.size - len(selected)) / 2))]

            breeding_pool.extend([c for child in children for c in child])
            self.agents = breeding_pool

    # fitness function for agents
    def fitness(self, agent):

        score = 0

        # gets average score over a number of trial runs
        for _ in range(self.trials):

            agent.game.reset()
            moves = 0

            while not agent.game.finished and moves <= self.move_cap:
                moves += 1
                agent.move()

            score += agent.game.score()

        agent.game.reset()

        return score / self.trials

    # breeds two agents and produces two children with a combination of the genetic material of their parents
    def reproduce(self, agent1, agent2):

        assert agent1.NeuralNetwork.shape == agent2.NeuralNetwork.shape

        shape = agent1.NeuralNetwork.shape
        child1 = Agent(shape)
        child2 = Agent(shape)

        for i in range(len(shape) - 1):

            # swaps rows of genes in parents randomly in children
            shape = np.shape(child1.NeuralNetwork.weights[i])
            rows = shape[0]
            u = np.repeat(np.random.randint(0, 2, (rows, 1)), shape[1], axis=1)

            # determines elements to mutate
            mutation = np.random.ranf(shape) < self.epsilon

            child1.NeuralNetwork.weights[i] = (
                    agent1.NeuralNetwork.weights[i] * u +
                    agent2.NeuralNetwork.weights[i] * (1 - u))

            child1.NeuralNetwork.weights[i] += mutation * np.random.randn(shape[0], shape[1])

            child2.NeuralNetwork.weights[i] = (
                    agent2.NeuralNetwork.weights[i] * u +
                    agent1.NeuralNetwork.weights[i] * (1 - u))

            child2.NeuralNetwork.weights[i] += mutation * np.random.randn(shape[0], shape[1])

        return [child1, child2]

    # runs a random trial for a given agent
    def run(self, agent_idx=0):
        AgentRenderer(self.agents[agent_idx])

