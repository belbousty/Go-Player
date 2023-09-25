# Developpers:
- **EL BOUSTY Badreddine**
- **SOUFARY Farouk**

# My Player: "Ayume"

## Overview

Our player, "Ayume," is a purely defensive player. This defensive approach aims to minimize the opponent's gains as much as possible while capitalizing on certain opportunities as the game progresses to maximize its own gains, all while considering the minimization of the opponent's gains.

## Strategy

The core idea of Ayume's strategy revolves around constructing a weight matrix at the beginning of the game. In this matrix, positions closer to the center of the board are assigned higher weights. As the game progresses, the weight matrix is adjusted based on various criteria and coefficients. The following criteria are taken into account at each move, considering the weight matrix generated at the previous move:

- **Connectivity**: Evaluates how connected the player's pieces are on the board.
- **Degrees of Freedom**: Measures the number of empty spaces around a player's pieces.
- **Opponent's Degrees of Freedom**: Considers the degrees of freedom of the opponent's pieces.
- **Captured Pieces**: Accounts for the number of opponent's pieces captured.
- **Number of Opponent Neighbors for an Empty Position**: Calculates the number of neighboring opponent pieces for an empty position.
- **Distance to the Center (Variable)**: Reflects the distance between a position and the center of the matrix (where the center has the highest weight, and the weight decreases as one moves away).

On the other hand, the coefficients for each criterion are chosen based on their priority. In most cases, the coefficients increase exponentially (2^ or 3^), ensuring that a criterion significantly influences the weight of a position.

After each move, the maximum weight obtained for a position is selected, and the weight matrix is updated, with this position as the new center of the weights.

## Example

Let's illustrate this with an example:

Initial Weight Matrix:
```console 

[2, 2, 2, 2, 2]
[2, 4, 4, 4, 2]
[2, 4, 8, 4, 2]
[2, 4, 4, 4, 2]
[2, 4, 2, 2, 2]

# New Center
Center = (1, 1)

# Updated Weight Matrix:
[4, 4, 4, 2, 0]
[4, 8, 4, 2, 0]
[4, 4, 4, 2, 0]
[2, 2, 2, 2, 0]
[0, 0, 0, 0, 0]
```
