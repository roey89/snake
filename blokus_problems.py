from search import SearchProblem, astar, Duo
import copy

DIRECTIONS = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UP": (0, 1),
    "DOWN": (0, -1),
}
DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']


class SnakeProblem(SearchProblem):

    def __init__(self, snake, fruit, board_size, direction, max_depth):
        self.state = SnakeState(snake, direction, 0)
        self.board_size = board_size
        self.fruit = fruit
        self.expanded = 0
        self.max_depth = max_depth

    def get_start_state(self):
        return self.state

    def is_goal_state(self, state):
        return state.snake[0] == self.fruit or state.depth == self.max_depth

    def get_successors(self, state):
        self.expanded = self.expanded + 1
        return [(state.do_move(move), move, 1) for move in (0, 1, 3)]

    def get_cost_of_actions(self, actions):
        return len(actions)


class SnakeState():

    def __init__(self, snake, direction, depth):
        self.snake = snake
        self.direction = direction
        self.depth = depth

    def do_move(self, move):
        new_direction = (self.direction + move) % 4

        old_head = self.snake[0]
        movement = [DIRECTIONS[DIRS[move]]][0]
        new_head = (old_head[0] + movement[0], old_head[1] + movement[1])

        new_snake = copy.deepcopy(self.snake)
        del new_snake[-1]
        new_snake.insert(0, new_head)
        new_state = SnakeState(new_snake, new_direction, self.depth + 1)

        return new_state


def distance_heuristic(state, SnakeProblem):
    head = state.snake[0]
    for i in range(1, len(state.snake)):
        if head == state.snake[i]:
            return SnakeProblem.board_size ^ 2
    return manhattan_distance(head, SnakeProblem.fruit)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
