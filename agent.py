# agent.py
import random
from collections import deque
import heapq

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:
    """A goal-based agent that finds paths using search algorithms."""

    def __init__(self, active_algo='BFS'):
        self.plan = []
        self.active_algo = active_algo.upper()

    def get_neighbors(self, position, grid_size, walls):
        """Return all valid neighbouring positions and actions."""

        x, y = position
        width, height = grid_size

        possible_moves = [
            ('Up', (x, y + 1)),
            ('Down', (x, y - 1)),
            ('Left', (x - 1, y)),
            ('Right', (x + 1, y))
        ]

        valid_neighbors = []

        for action, next_position in possible_moves:
            next_x, next_y = next_position

            inside_grid = (
                0 <= next_x < width
                and 0 <= next_y < height
            )

            if inside_grid and next_position not in walls:
                valid_neighbors.append((next_position, action))

        return valid_neighbors

    def bfs_search(self, start, goal, grid_size, walls):
        """Find the shortest path using Breadth-First Search."""

        # FIFO queue containing: (current position, path)
        frontier = deque([(start, [])])

        # Record positions that have already been discovered
        reached = {start}

        while frontier:
            current_position, path = frontier.popleft()

            if current_position == goal:
                return path

            neighbors = self.get_neighbors(
                current_position,
                grid_size,
                walls
            )

            for next_position, action in neighbors:
                if next_position not in reached:
                    reached.add(next_position)

                    new_path = path + [action]

                    frontier.append(
                        (next_position, new_path)
                    )

        # Return an empty list if no route exists
        return []

    def dfs_search(self, start, goal, grid_size, walls):
                """Find a path using Depth-First Search."""

                # LIFO stack containing: (current position, path)
                frontier = [(start, [])]

                # Record positions that have already been discovered
                reached = {start}

                while frontier:
                    # pop() removes the newest item
                    current_position, path = frontier.pop()

                    if current_position == goal:
                        return path

                    neighbors = self.get_neighbors(
                        current_position,
                        grid_size,
                        walls
                    )

                    for next_position, action in neighbors:
                        if next_position not in reached:
                            reached.add(next_position)

                            new_path = path + [action]

                            frontier.append(
                                (next_position, new_path)
                            )

                # Return an empty list when no path exists
                return []

    def ucs_search(self, start, goal, grid_size, walls):
                    """Find the lowest-cost path using Uniform-Cost Search."""

                    # Priority queue items:
                    # (total cost, current position, path)
                    frontier = [(0, start, [])]

                    # Store the lowest known cost for each reached position
                    reached = {start: 0}

                    while frontier:
                        total_cost, current_position, path = heapq.heappop(frontier)

                        # Ignore an outdated, more expensive entry
                        if total_cost > reached[current_position]:
                            continue

                        if current_position == goal:
                            return path

                        neighbors = self.get_neighbors(
                            current_position,
                            grid_size,
                            walls
                        )

                        for next_position, action in neighbors:
                            # Every grid movement has a cost of 1
                            new_cost = total_cost + 1

                            if (
                                next_position not in reached
                                or new_cost < reached[next_position]
                            ):
                                reached[next_position] = new_cost

                                new_path = path + [action]

                                heapq.heappush(
                                    frontier,
                                    (new_cost, next_position, new_path)
                                )

                    # Return an empty list when no path exists
                    return []


    def convert_to_actions(self, movement_path, starting_facing):
                        """Convert Up/Down/Left/Right into turns and MoveForward actions."""

                        directions = ['Up', 'Right', 'Down', 'Left']
                        current_facing = starting_facing
                        action_plan = []

                        for required_direction in movement_path:
                            current_index = directions.index(current_facing)
                            required_index = directions.index(required_direction)

                            difference = (required_index - current_index) % 4

                            if difference == 1:
                                action_plan.append('TurnRight')

                            elif difference == 2:
                                action_plan.append('TurnRight')
                                action_plan.append('TurnRight')

                            elif difference == 3:
                                action_plan.append('TurnLeft')

                            action_plan.append('MoveForward')
                            current_facing = required_direction

                        return action_plan

    def sense_and_act(self, percept):
                        """Create a plan when necessary and execute one action at a time."""

                        # Collect the food when the agent reaches it
                        if percept['food_here']:
                            self.plan = []
                            return 'Suck'

                        # Create a new plan when the current plan is empty
                        if not self.plan:
                            start = tuple(percept['agent_pos'])
                            grid_size = tuple(percept['grid_size'])
                            walls = set(tuple(wall) for wall in percept['walls'])
                            all_food = [
                                tuple(food)
                                for food in percept['all_food']
                            ]

                            # Stop if there is no food remaining
                            if not all_food:
                                return 'NoOp'

                            # Find the closest food using Manhattan distance
                            goal = min(
                                all_food,
                                key=lambda food: (
                                    abs(food[0] - start[0])
                                    + abs(food[1] - start[1])
                                )
                            )

                            # Select the configured search algorithm
                            if self.active_algo == 'BFS':
                                movement_path = self.bfs_search(
                                    start,
                                    goal,
                                    grid_size,
                                    walls
                                )

                            elif self.active_algo == 'DFS':
                                movement_path = self.dfs_search(
                                    start,
                                    goal,
                                    grid_size,
                                    walls
                                )

                            elif self.active_algo == 'UCS':
                                movement_path = self.ucs_search(
                                    start,
                                    goal,
                                    grid_size,
                                    walls
                                )

                            else:
                                raise ValueError(
                                    "active_algo must be 'BFS', 'DFS', or 'UCS'"
                                )

                            # Convert directions into actions understood by the environment
                            self.plan = self.convert_to_actions(
                                movement_path,
                                percept['facing']
                            )

                            # No route was found
                            if not self.plan:
                                return 'NoOp'

                        # Execute and remove the first action in the plan
                        return self.plan.pop(0)
