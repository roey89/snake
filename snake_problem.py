import copy

import util
from util import PriorityQueue
from util import Queue
import numpy as np


def illegal(next_head, size, curr_snake):
    return next_head[0] < 0 or next_head[0] >= size or next_head[1] < 0 or \
           next_head[1] >= size or next_head in curr_snake


DIRECTIONS = {
    "UP": (0, 1),
    "RIGHT": (1, 0),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
}
DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a lstt of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A lstt of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class Duo(list):
    def __init__(self, lst):
        self.lst = lst


class SnakeProblem(SearchProblem):
    def __init__(self, snake, fruit, board_size, direction, max_depth):
        self.state = SnakeState(snake, board_size, direction, fruit, 0)
        self.fruit = fruit
        self.expanded = 0
        self.max_depth = max_depth

    def get_start_state(self):
        return self.state

    def is_goal_state(self, state):
        if state.dead_end():
            return False
        return state.snake[0] == self.fruit or state.depth == self.max_depth

    def get_successors(self, state):
        if self.expanded == 0:
            state.snake.append(state.snake[-1])
        self.expanded = self.expanded + 1
        successors = []
        for move in (0, 1, 2, 3):
            new_state = state.do_move(move)
            if not illegal(new_state.snake[0], state.board_size, new_state.snake[1:]):
                successors.append((new_state, move))
        return successors

    def get_cost_of_actions(self, actions):
        return len(actions)


class SnakeState:
    def __init__(self, snake, board_size, direction, fruit, depth):
        self.snake = copy.deepcopy(snake)
        self.board_size = board_size
        self.direction = direction
        self.fruit = fruit
        self.depth = depth

    def do_move(self, move):
        new_direction = (self.direction + move) % 4
        old_head = self.snake[0]

        # new_head = old_head + movement (element-wise)
        movement = DIRECTIONS[DIRS[move]]
        new_head = (old_head[0] + movement[0], old_head[1] + movement[1])

        # advance one step
        new_snake = copy.deepcopy(self.snake)
        if not new_head == self.fruit:
            del new_snake[-1]
        new_snake.insert(0, new_head)
        new_state = SnakeState(new_snake, self.board_size, new_direction, self.fruit, self.depth + 1)

        return new_state

    def score(self):
        return len(self.snake)

    def illegal_state(self):
        return illegal_state(self)

    def getLegalActions(self):
        legal_actions = []
        for move in (0, 1, 2, 3):
            if not illegal_state(self.do_move(move)):
                legal_actions.append(move)
        return legal_actions

    def dead_end(self):
        return len(self.getLegalActions()) == 0


def astar(problem, heuristic, agent=None):
    fringe = PriorityQueue()
    been_there = []
    temp_item = Duo([problem.get_start_state(), []])
    fringe.push(temp_item, 0)
    while True:
        if fringe.isEmpty():
            return None
        current_board, actions = fringe.pop().lst
        if problem.is_goal_state(current_board):
            # check_problem = SnakeProblem(current_board.snake, (-1, -1), problem.state.board_size,
            #                             problem.state.direction, 100)
            # if check_goal_state(check_problem):
            return actions
        # else:
        #    been_there.append(current_board)
        if current_board not in been_there:
            for item in problem.get_successors(current_board):
                temp_actions = actions[:]
                temp_actions.append(item[1])
                temp_item = Duo([item[0], temp_actions])
                priority = problem.get_cost_of_actions(temp_actions) + heuristic(item[0], problem, agent)
                fringe.push(temp_item, priority)
            been_there.append(current_board)


def check_goal_state(problem):
    fringe = Queue()
    been_there = []
    fringe.push((problem.get_start_state(), []))
    for i in range(snake_to_check_depth(len(problem.state.snake))):
        if fringe.isEmpty():
            return False
        current_board, actions = fringe.pop()
        if illegal(current_board.snake[0], current_board.board_size, current_board.snake[1:]):
            pass
        if current_board not in been_there:
            successors = problem.get_successors(current_board)
            for item in successors:
                temp_lst = actions[:]
                temp_lst.append(item[1])
                fringe.push((item[0], temp_lst))
            been_there.append(current_board)
    return True


def snake_to_check_depth(length):
    """
    Works only with a 10x10 board.
    """
    if length <= 20:
        return 400
    elif length <= 40:
        return int(length ** 1.6) + 300
    elif length <= 70:
        return int(length ** 1.8)
    elif length <= 90:
        return 2000
    else:
        return 1000


def distance_heuristic(state, snakeproblem=None, agent=None):
    head = state.snake[0]
    if illegal(head, state.board_size, state.snake[1:]):
        return state.board_size ** 3
    if snakeproblem == None:
        fruit = state.fruit
    else:
        fruit = snakeproblem.fruit
    return manhattan_distance(head, fruit)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def illegal_state(state):
    head = state.snake[0]
    cond1 = not head in state.snake[1:len(state.snake)]
    cond2 = head[0] >= 0 and head[1] >= 0
    cond3 = head[0] < state.board_size and head[1] < state.board_size

    return not (cond1 and cond2 and cond3)


def learned_heuristic(state, snakeproblem, agent):
    return state.board_size - agent.getValue(state)


def combined_heuristic(state, snakeproblem, agent):
    if blockedDirections(state) <= 0:
        return distance_heuristic(state, snakeproblem, agent)
    area_heuristic = areaAroundSnake(state)
    if area_heuristic == None:
        return distance_heuristic(state, snakeproblem, agent)
    if area_heuristic <= 0:
        return state.board_size ** 3
    score = (len(state.snake) * 1.0) / (state.board_size ** 2)
    return distance_heuristic(state, snakeproblem, agent) + 10 * (2 - score) / (area_heuristic ** (1 + score))


def areaAroundSnake(state):
    areas = get_componnents(state)
    if len(areas) <= 1 or len(areas[0]) > state.board_size ** 2 - state.board_size:
        return None
    head_areas = []
    for area in areas:
        if pointNearArea(area, state.snake[0]):
            head_areas.append(area)

    max_rank = -np.inf
    for area in head_areas:
        size = len(area)
        i = len(state.snake) - 1
        while i > 0:
            if pointNearArea(area, state.snake[i]):
                break
            i = i - 1
        rank = size - len(state.snake) + i
        if rank > max_rank:
            max_rank = rank

    return max_rank


def get_componnents(state):
    points = []
    for x in range(state.board_size):
        for y in range(state.board_size):
            if not (x, y) in state.snake:
                points.append(Point((x, y)))
    for i in range(len(points) - 1):
        for j in range(i + 1, min(i + state.board_size, len(points))):
            point = points[i]
            other_point = points[j]
            if neighbors(point.position, other_point.position):
                point.add_link(other_point)
                other_point.add_link(point)
    points = set(points)
    return connected_components(points)


def connected_components(points):
    # List of connected components found. The order is random.
    result = []

    # Make a copy of the set, so we can modify it.
    points = set(points)

    # Iterate while we still have nodes to process.
    while points:

        # Get a random node and remove it from the global set.
        point = points.pop()

        # This set will contain the next group of nodes connected to each other.
        group = {point}

        # Build a queue with this node in it.
        queue = [point]

        # Iterate the queue.
        # When it's empty, we finished visiting a group of connected nodes.
        while queue:
            # Consume the next item from the queue.
            point = queue.pop(0)

            # Fetch the neighbors.
            neighbors = point.links

            # Remove the neighbors we already visited.
            neighbors.difference_update(group)

            # Remove the remaining nodes from the global set.
            points.difference_update(neighbors)

            # Add them to the group of connected nodes.
            group.update(neighbors)

            # Add them to the queue, so we visit them in the next iterations.
            queue.extend(neighbors)

        # Add the group to the list of groups.
        result.append(group)

    # Return the list of groups.
    return result


def pointNearArea(area, point):
    for otherPoint in area:
        if neighbors(point, otherPoint.position):
            return True


def neighbors(point1, point2):
    if point1 == point2:
        return False
    if abs(point2[0] - point1[0]) + abs(point2[1] - point1[1]) < 2:
        return True
    return False


class Point(object):
    def __init__(self, position):
        self.__position = position
        self.__links = set()

    @property
    def position(self):
        return self.__position

    @property
    def links(self):
        return set(self.__links)

    def add_link(self, other):
        self.__links.add(other)
        other.__links.add(self)


def blockedDirections(state):
    """
    Counts the number of direction in which the snake is blocked
    """
    snake_copy = copy.deepcopy(state.snake)
    boardSize = state.board_size
    if len(snake_copy) < 3:
        return 1
    blocked = 0
    head = snake_copy[0]
    del snake_copy[-1]
    for direction in DIRECTIONS.values():
        if illegal((head[0] + direction[0], head[1] + direction[1]), boardSize, snake_copy):
            blocked += 1
    return blocked
