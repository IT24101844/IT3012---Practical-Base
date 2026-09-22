# IT3012 - Intelligent Agents Practical Repository

**Student ID:** IT24101844  
**Academic Year:** Year 3, Semester 1 - 2026  
**Repository:** IT3012 Practical Base

## Overview

This repository contains the implementations and documentation completed from Practical 01 to Practical 04 for the Intelligent Agents module. The practical series begins with a basic agent-environment interaction and gradually develops the agent through reflex, model-based, uninformed-search, and informed-search architectures.

The final version includes a visual grid environment in which agents move through a two-dimensional grid, avoid walls, locate food, and select actions using different search strategies.

## Practical Progression

| Practical | Topic | Main Outcome | Branch |
|---|---|---|---|
| Practical 01 | Agent-Environment Architecture | Built the grid environment and basic agent interaction cycle | `lab1` |
| Practical 02 | Reflex and Model-Based Agents | Implemented condition-action rules and internal memory | `lab2` |
| Practical 03 | Uninformed Search | Implemented BFS, DFS, and UCS planning agents | `lab3` |
| Practical 04 | Informed Search | Implemented heuristic functions and A* Search | `lab4` |

---

## Practical 01 - Agent-Environment Architecture

### Objective

The first practical introduced the basic relationship between an agent and its environment. A grid-based environment was created so that the agent could receive percepts, select actions, and affect the state of the environment.

### Implemented Features

- A small grid-world environment
- Agent position and movement in four directions
- Randomly selected agent actions
- Food locations and wall obstacles
- Rewards for collecting food
- Penalties for attempting to move into walls
- A step limit and termination condition
- A terminal-based simulator for observing the agent-environment cycle
- A visual grid environment using Tkinter

### Main Interaction Cycle

```text
Environment -> Percept -> Agent -> Action -> Environment
```

The `GridHuntGame` environment provides information such as the agent's position, remaining food, wall collisions, and score. The `GreedyGridAgent` receives this information and selects an action.

### Run the Basic Simulation

```bash
python simulator.py
```

---

## Practical 02 - Simple Reflex and Model-Based Agents

### Objective

The second practical explored partially observable environments. The agent was first implemented as a Simple Reflex Agent and was then improved into a Model-Based Agent with an internal state.

### Simple Reflex Agent

The Simple Reflex Agent uses only the current percept. It follows condition-action rules such as:

```text
IF food is here      -> Suck
IF a wall is ahead   -> TurnLeft
ELSE                 -> MoveForward
```

Because it does not remember previous percepts or actions, it can repeat the same behaviour and become trapped in a loop.

### Model-Based Agent

The Model-Based Agent maintains an internal state using:

- Percept history
- Previous action
- Repeated-percept count

When it detects that the same situation is repeating, it selects a different action to escape the loop.

### Implemented Features

- Local percepts such as `wall_ahead` and `food_here`
- Simple condition-action rules
- Partial observability
- Percept and action history
- Repeated-state detection
- Alternative action selection when a loop is detected
- Comparison between reflex and model-based behaviour

---

## Practical 03 - Uninformed Search

### Objective

The third practical introduced a goal-based planning agent. The environment exposes its global state so that the agent can calculate a complete route before executing actions.

The percept was extended with:

```python
'grid_size': (width, height)
'walls': list(walls)
'all_food': list(food_positions)
```

### Breadth-First Search - BFS

- Uses a FIFO queue
- Explores the shallowest nodes first
- Finds a shortest path when every movement has the same cost

### Depth-First Search - DFS

- Uses a LIFO stack
- Explores one path deeply before backtracking
- Uses less frontier memory but may return a longer path

### Uniform-Cost Search - UCS

- Uses a priority queue
- Expands the node with the lowest accumulated path cost, `g(n)`
- Finds an optimal path when movement costs are non-negative

### Graph Search and Planning

Each algorithm maintains a reached or visited collection. This prevents the agent from repeatedly exploring the same position and avoids infinite cycles.

The `SearchAgent` calculates a movement path, stores it in `self.plan`, converts the directions into executable actions, and performs one action at a time.

The visual interface supports:

- **Run BFS**
- **Run DFS**
- **Run UCS**

---

## Practical 04 - Informed Search

### Objective

The fourth practical extends the Search Agent by implementing A* Search. Unlike uninformed algorithms, A* uses a heuristic to estimate the remaining cost from the current position to the goal.

### A* Evaluation Function

```text
f(n) = g(n) + h(n)
```

Where:

- `g(n)` is the path cost from the starting position to the current position.
- `h(n)` is the estimated cost from the current position to the goal.
- `f(n)` is the estimated total cost of the path through the current node.

Each frontier entry uses the format:

```text
(f_cost, g_cost, current_position, path_taken)
```

### Manhattan Distance

Manhattan Distance is used for four-way movement:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

### Euclidean Distance

Euclidean Distance measures the straight-line distance between two positions:

```text
h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

### Implemented Features

- Manhattan Distance heuristic
- Euclidean Distance heuristic
- A* Search using `heapq`
- Selection between the two heuristic functions
- Explored-state tracking using `reached_states`
- Four-way neighbor expansion
- Closest-food goal selection
- A* integration with `sense_and_act()`
- A **Run A*** button in the visual interface

### Heuristic Testing Checkpoint

```text
Start position: (0, 0)
Goal position:  (3, 4)

Manhattan: 7
Euclidean: 5.0
```

### A* Path Test

```text
A* path: ['Up', 'Right', 'Right', 'Right', 'Up', 'Up']
Path length: 6
```

This confirms that A* found a six-movement shortest path in the test grid.

---

## Running the Visual Application

Open a terminal inside the project folder and run:

```bash
python visual_grid_game.py
```

The interface provides:

- **Run BFS**
- **Run DFS**
- **Run UCS**
- **Run A***
- **Reset**

In the environment:

- The blue circle represents the agent.
- Orange circles represent food.
- Grey cells marked with `W` represent walls.

## Running the Automated Tests

```bash
python -m unittest -v test_suite.py
```

Expected result:

```text
Ran 4 tests
OK
```

The current test suite verifies:

- Simple Reflex Agent behaviour
- Model-Based Agent memory behaviour
- BFS shortest-path behaviour
- BFS handling of an unreachable goal

The Lab 4 heuristic and A* checkpoints were also tested separately and produced the expected results.

---

## Project Files

| File | Description |
|---|---|
| `agent.py` | Contains the basic agent and the BFS, DFS, UCS, and A* search implementations. |
| `grid_game.py` | Contains the original small grid-world environment. |
| `visual_grid_game.py` | Contains the Tkinter environment, reflex agents, and search controls. |
| `simulator.py` | Runs the original terminal-based simulation. |
| `test_suite.py` | Contains automated tests for the reflex, model-based, and BFS implementations. |
| `IT24101844 - ISLab01.pdf` | Practical 01 documentation in its relevant repository branch. |
| `IT24101844 - ISlab02.pdf` | Practical 02 documentation. |
| `IT24101844 - ISLab03.pdf` | Practical 03 documentation. |
| `IT24101844 - ISlab04.pdf` | Practical 04 documentation. |

## Technologies Used

- Python 3
- Tkinter
- `collections.deque`
- `heapq`
- `math`
- `unittest`
- Git and GitHub

## Repository Branches

```text
main  - Base repository
lab1  - Practical 01
lab2  - Practical 02
lab3  - Practical 03
lab4  - Practical 04
```

## Final Outcome

Across the four practicals, the agent progressed from basic environment interaction to intelligent path planning:

```text
Basic Agent
    -> Simple Reflex Agent
    -> Model-Based Agent
    -> Goal-Based Search Agent
    -> Informed A* Search Agent
```

The final A* agent can use knowledge of the grid and heuristic estimates to navigate around walls and move efficiently toward food.

## Author

**Student ID:** IT24101844  
**Module:** IT3012 - Intelligent Agents
