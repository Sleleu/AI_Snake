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


This restriction shapes the state space and decision-making process. The agent's actions are limited to four directional movements: UP, LEFT, DOWN, and RIGHT.

## Neural Architecture

The agent processes information about the game state through a simple **deep neural network (DNN)** with multiple layers. The architecture begins with 20 input neurons that capture essential environmental data, processes this through two hidden layers, and produces action values through the output layer.

### Input Layer (20 neurons)
The input layer consists of two types of environmental sensors:

#### Distance Measurements (16 neurons)
Each direction contains 4 normalized distance values representing:

- Distance to the nearest **wall**
- Distance to the nearest **green apple**
- Distance to the nearest **red apple**
- Distance to the nearest **snake body segment**

#### Danger Detection (4 neurons)
Four binary neurons (0 or 1) detect **immediate collision threats in adjacent cells**. These neurons activate when:

- A wall is directly adjacent in that direction
- A snake body segment is directly adjacent in that direction

### Hidden Layers

The network processes this input through two hidden layers:

- **First hidden layer** contains 128 neurons, allowing for complex pattern recognition
- **Second hidden layer** contains 64 neurons, further refining these patterns

### Output Layer

The final layer consists of 4 neurons, each corresponding to a possible movement direction (UP, DOWN, LEFT, RIGHT). These neurons output **Q-values**, representing the **expected future reward for each action** in the current state.

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

# Usage

The program can be run with various options to control its behavior:

`python3 main.py [options]`

## Available Options

#### Training and Model Management
- `-t, --train`: Enable training mode for the AI agent
- `-e EPISODE, --episode EPISODE`: Specify the number of episodes to run
- `-m MODEL, --model MODEL`: Load a pre-trained model from a specified path

#### Visualization and Debug
- `-v {on,off}, --visual {on,off}`: Enable or disable the GUI (if you want to train your model faster, disable visualization to reduce computational overhead)
- `-step-by-step`: Enable step-by-step mode for detailed observation
- `-plot OUTPUT_FILENAME`: Save training statistics plots to a specified filename

Example of a training statistics plot:

<p align="center">
  <img src="https://github.com/user-attachments/assets/b1c45ba2-bc71-4a03-bee6-717c135ee9fd" alt="Training Statistics Plot" width="600">
</p>

#### Game Modes

- `-p, --player`: Enable player mode to play the game manually

## Usage Examples
Train the AI for 1000 episodes with visualization:
```bash
python3 main.py -t -e 1000
```

Load a pre-trained model and watch it play:
```bash
python3 main.py -m model/trained_model.pth
```

Train without visualization for faster processing:
```bash
python3 main.py -t -e 1000 -v off
```

## Settings

You can modify basic parameters in `settings.py` like grid size, fruit population, initial snake length and game speed. Since a model can generalize its learning across different grid sizes, you can experiment with settings like:

```python
# Default game size
GRID_SIZE = 30
CELL_SIZE = 15
...
# Default game settings
SNAKE_SIZE = 3
GREEN_FRUITS_NB = 300
RED_FRUITS_NB = 300
...
# Game speed
FPS = 150
```
Here's what it looks like in action:
<p align="center">
  <img src="https://github.com/user-attachments/assets/548346d3-9ac9-4d2c-a130-b12b671396e6" alt="Large Snake Game Environment">
</p>
