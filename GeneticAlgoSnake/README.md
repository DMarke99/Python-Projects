# A Genetic Algorithmic Approach to Snake

A Snake game implemented in Python 3.6 using Pygame, with a genetic algorithm that attempts to learn how to play the game.

## Prerequisites

To open and run the project on your computer you will need:

```
Python 3.6+
Pygame 1.9.3+
```

## Setup

1) Ensure you have the above dependencies installed.
2) Download the GeneticAlgoSnake folder
3) Execute genetic algorithm by running main.py, and play game manually by running snake.py

## Usage

Use arrow keys to control the direction of the snake

## Insight

Genetic algorithms are a powerful tool for learning how to play games. Algorithmic/systematic approaches to games have a massive advantage in the ability to process and react to information much quicker than most humans. However, there must exist a systemised approach to playing a game for this to be effective. In the case of Snake, it is possible to win any game with an even number of rows or columns by winding down a hamiltonian path on the grid, so I felt it uninteresting to hard code this approach. The aim of this project for me was to find out whether a computer could develop a strategy to play Snake given a limited amount of information about the grid, and to gain an intuition as to how genetic algorithms work, and their potential benefits over other approaches.

Each agent is given the distance to each wall, direction of food and whether the snake would die if it walked into a space, and uses an artificial neural network to pick between moving up, down, left or right. The weight values of the neural network are the 'genetic material' that is breeded in the algorithm. The fitness function of each agent is the average score over 10 games for a snake, with the number of moves in a game capped.

The learning process takes the population of agents and scores them using the fitness function. The bottom portion of the population are deleted, and genetic material from random surviving pairs of agents are mixed to create 'children', which are then added to the population. Genetic material also has a small change of mutation on each trial, which increases diversity in the population and avoids the process being stuck in a local maximum. The process works effectively by natural selection; agents with good characteristics are more likely to survive than agents with bad ones, thus good genetic traits are more likely to be spread in the population.

The learning process managed to achieve reasonable performance over all runs I did; average score in the population increased from less than 1 to more than 20, usually within about 200 trials. The highest performance I achieved was an average score of 35 in the population after training for 5 hours.

Overall I am pleased with the performance of the genetic algorithm in this situation. This proved to me that they are a powreful technique that can be used to datamine strategies to play games, however some care needs to be taken in tuning parameters for optimal learning; if population size or mutation chance are too small the program becomes very unlikely to pick up on good techniques, and thus do not train very well, but if mutation chance is too high good traits get corrupted very easily, and so don't spread as well. A larger population size is usually good but obviously increases computation costs. This cost can be curved significantly by parallelising the scoring process and running on a computer with many cores/threads.

## Contributors

This project was created entirely by myself in two days in January
