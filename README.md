# About the project

Learn2Slither is a 42 school project focused on implementing a reinforcement learning agent for the Snake game.
The project involves creating an AI that learns to navigate through **Q-learning** implementation, enabling the snake to collect apples while avoiding collisions.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ebab6150-fe64-4f54-a344-6780dcea2856" alt="Snake Game Learning Process">
</p>

## Environment Specifications

- Board size: 10x10 grid
- Two green apples randomly placed (increase snake length)
- One red apple randomly placed (decrease snake length)
- Initial snake length: 3 cells
- Game ending conditions: wall collision, self-collision, or zero length

## States and Actions
The snake agent operates with information from **four directions around its head**, representing its local perception of the environment.

![screenshotsnake](https://github.com/user-attachments/assets/0e744551-0f7d-437e-a55e-44d7c04e107d)


This restriction shapes the state space and decision-making process. The agent's actions are limited to four directional movements: **UP, LEFT, DOWN, and RIGHT**.

## Neural Architecture

The agent processes its environment through 20 neurons that capture different aspects of the game state. These neurons provide normalized distance measurements and binary danger indicators in each direction (UP, DOWN, LEFT, RIGHT). The neural architecture consists of:

### Distance Measurements (16 neurons)
Each direction contains four normalized distance values representing:

- Distance to the nearest wall
- Distance to the nearest green apple
- Distance to the nearest red apple
- Distance to the nearest snake body segment

### Danger Detection (4 neurons)
Four binary neurons (0 or 1) detect immediate collision threats in adjacent cells. These neurons activate when:

- A wall is directly adjacent in that direction
- A snake body segment is directly adjacent in that direction

## Bonus Features
Bonus points are awarded for:

- Achieving snake lengths beyond 10 during sessions (15, 20, 25, 30, 35)
- Creating a polished visual interface
- Enabling the snake to generalize its learning across different grid sizes


# Installation

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- git

## Installation instructions

```bash
# Clone repository
git clone https://github.com/Sleleu/AI_Snake.git

# Go to directory
cd AI_snake

# Create virtual environnement
python3 -m venv .venv

# Activate virtual environnement
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Install required packages in virtual environnement
pip install -r requirements.txt
```
