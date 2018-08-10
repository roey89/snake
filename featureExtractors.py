# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Snake game states"

import util
import snake_problem


class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()


class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state, action)] = 1.0
        return feats


def illegal(next_head, size, curr_snake):
    return next_head[0] < 0 or next_head[0] >= size or next_head[1] < 0 or \
           next_head[1] >= size or next_head in curr_snake


def areaAroundSnake(state):
    areas = get_componnents(state)
    head_area = []
    for area in areas:
        if pointNearArea(area, state.snake[0]):
            head_area = area
            break

    if pointNearArea(head_area, state.snake[-1]):
        bool_var = 1
    else:
        bool_var = 0

    return len(head_area), bool_var


def get_componnents(state):
    points = []
    for x in range(state.board_size):
        for y in range(state.board_size):
            if not (x, y) in state.snake:
                points.append(Point((x, y)))
    for point in points:
        for other_point in points:
            if neighbors(point.position, other_point.position):
                point.add_link(other_point)
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


class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Snake:
    - whether the action will result in loss
    - whether the fruit will be eaten
    - how far away the next fruit is
    - how far away the tail is
    - number of turns (in the snake)
    - how many directions can the snake go in the next step
    -
    - what is the snake size
    """

    def getFeatures(self, state, action):
        nextState = state.do_move(action)
        boardSize = state.board_size
        fruit = nextState.fruit
        snake = nextState.snake
        head = snake[0]
        features = util.Counter()

        features["bias"] = 1.0
        features["head-fruit-distance"] = snake_problem.manhattan_distance(head, fruit) / boardSize ** 2
        if state.fruit == head:
            features["eats-fruit"] = 1.0
        if snake_problem.illegal(head, boardSize, snake):
            features["illegal"] = 1.0

        area, near_tail = areaAroundSnake(nextState)
        features["head-area"] = area / 100
        features["head-tail"] = near_tail
        features.divideAll(10.0)

        return features


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
