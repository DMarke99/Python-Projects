from agent import Population

# initialises a new population of agents
population = Population(size=250)

# trains the agents to play snake
for i in range(10000):
    population.train()
    if i > 100:
        population.run()
