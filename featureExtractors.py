# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Snake game states"

from snake import DIRECTIONS, illegal
from snake_problem import manhattan_distance
import util


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
    for direction in DIRECTIONS.values():
        if illegal((head[0] + direction[0], head[1] + direction[1]), boardSize, snake):
            blocked += 1
    return blocked


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
        boardSize = snake.BOARD_SIZE  # TODO: maybe we need to change this to a state attribute

        features = util.Counter()
        features["bias"] = 1.0

        # Tried to order by importance
        if not illegal(head, boardSize, snake):
            features["legal-move"] = 1.0
            if fruit == (head(0), head(1)):
                features["eats-fruit"] = 1.0
        features["head-fruit-distance"] = manhattan_distance(head, fruit)
        features["head-tail-distance"] = manhattan_distance(head, tail)
        features["#-of-blocked-directions"] = blockedDirections(snake, boardSize)
        if features["#-of-blocked-directions"] == 4:
            features["is-totally=blocked"] = 1.0
        features["snake-size"] = len(snake)
        features["#-of-turns"] = numberOfTurns(snake)

        features.divideAll(10.0)
        return features
