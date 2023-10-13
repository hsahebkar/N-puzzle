# N-Puzzle Solver

![Python](https://img.shields.io/badge/Python-3.1x-blue.svg)

A Python program to solve the N-puzzle problem using A* algorithms.

## Table of Contents

- [Introduction](#introduction)
- [Setup](#Setup)
- [Algorithms](#algorithms)
- [Contributing](#contributing)

## Introduction

The N-puzzle is a classic and fun Puzzle in computer science.
This Python program provides a solver for the N-puzzle problem (Not in the Optimise Way).


## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/hsahebkar/N-puzzle.git
   cd N-puzzle
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Puzzle

   ```bash
   python main.py
   ```

## Algorithms

This program currently supports the following search algorithm (More coming soon):
1. A* Search
   - Heuristic:<br> 
      The `Heuristic` function calculates how far the current state of the board is from the goal state by measuring the total Manhattan distance of each element from its expected position. It also considers linear conflicts. The function returns a pair of values - one indicating if the board is solved, and the other is a heuristic score that guides the search algorithm to find efficient solutions.



## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository on GitHub.
2. Create a new branch and make your changes.
3. Submit a pull request with a clear description of your changes.
