from search import SearchProblem, astar, Duo
import copy

ARRAY_SIZE = 60


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


class SnakeProblem(SearchProblem):

    def __init__(self, snake, fruit, board_size, direction, max_depth):
        self.state = SnakeState(snake, board_size, direction)
        self.fruit = fruit
        self.expanded = 0
        self.max_depth = max_depth

    def get_start_state(self):
        return self.state

    def is_goal_state(self, state):
        return state.snake[0] == self.fruit or self.expanded == self.max_depth

    def get_successors(self, state):
        self.expanded = self.expanded + 1
        successors = []
        for move in (0, 1, 3):
            new_state = state.do_move(move)
            if not illegal(new_state.snake[0], ARRAY_SIZE, new_state.snake[1:]):
                successors.append((new_state, move))
        return successors

    def get_cost_of_actions(self, actions):
        return len(actions)


class SnakeState:
    def __init__(self, snake, board_size, direction):
        self.snake = copy.deepcopy(snake)
        self.board_size = board_size
        self.direction = direction

    def do_move(self, move):
        new_direction = (self.direction + move) % 4
        old_head = self.snake[0]

        # new_head = old_head + movement (element-wise)
        movement = [DIRECTIONS[DIRS[move]]][0]
        new_head = (old_head[0] + movement[0], old_head[1] + movement[1])

        # advance one step
        new_snake = copy.deepcopy(self.snake)
        del new_snake[-1]
        new_snake.insert(0, new_head)
        new_state = SnakeState(new_snake, self.board_size, new_direction)

        return new_state


def distance_heuristic(state, SnakeProblem):
    head = state.snake[0]
    if illegal(head, state.board_size, state.snake[1:]):
        return state.board_size ** 2
    return manhattan_distance(head, SnakeProblem.fruit)


def manhattan_distance(p1, p2):
    return 0.5*(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
