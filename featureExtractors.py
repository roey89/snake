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


def numberOfTurns(snake):
    """
    Counts the number of turns. snake is an array of (x,y) coordinates
    """
    if len(snake) < 3:
        return 0
    turns = 0
    for i in range(len(snake) - 2):
        if (snake(i + 2)[0] - snake(i + 1)[0], snake(i + 2)[1] - snake(i + 1)[1]) != \
                (snake(i + 1)[0] - snake(i)[0], snake(i + 1)[1] - snake(i)[1]):
            turns += 1
    return turns


def blockedDirections(snake, boardSize):
    """
    Counts the number of direction in which the snake is blocked
    """
    if len(snake) < 3:
        return 0
    blocked = 0
    head = snake[0]
    for direction in snake.DIRECTIONS.values():
        if snake.illegal((head[0] + direction[0], head[1] + direction[1]), boardSize, snake):
            blocked += 1
    return blocked

def areaAroundSnake(state):
  areas = get_componnents(state)
  head_area = []
  for area in areas:
    if pointNearArea(area,state.snake[0]):
      head_area = area
      break

  if pointNearArea(head_area,state.snake[-1]):
    bool_var = 10
  else:
    bool_var = 0

  return len(head_area), bool_var



def get_componnents(state):
    points = []
    for x in range(state.board_size):
      for y in range(state.board_size):
        if not (x,y) in state.snake:
          points.append(Point((x,y)))
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
    if neighbors(point,otherPoint.position):
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
        fruit = nextState.getFruit()
        snake = nextState.getSnake()
        head = snake[0]
        tail = snake[-1]
        boardSize = state.board_size

        features = util.Counter()
        features["bias"] = 1.0

        # Tried to order by importance
        """
        if not snake.illegal(head, boardSize, snake):
            features["legal-move"] = 1.0
            if fruit == (head(0), head(1)):
                features["eats-fruit"] = 1.0
        features["head-fruit-distance"] = snake_problem.manhattan_distance(head, fruit)
        features["#-of-blocked-directions"] = blockedDirections(snake, boardSize)
        if features["#-of-blocked-directions"] == 4:
            features["is-totally=blocked"] = 1.0
        """
        features["head-fruit-distance"] = snake_problem.manhattan_distance(head, fruit)
        area, near_tail = areaAroundSnake(state)
        features["head-area"] = area
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