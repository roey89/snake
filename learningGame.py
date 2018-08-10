from util import *
from util import raiseNotDefined
import time
import traceback
import snake


class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agent, startState, gameLength=1000):
        self.agent = agent
        self.gameLength = gameLength
        self.currentState = startState
        self.gameOver = False
        self.moveHistory = []
        self.totalAgentTime = 0

    def learn(self):
        numMoves = 0
        while numMoves < self.gameLength:
            numMoves += self.run(self.currentState)

    def run(self, currentState):
        numMoves = 0

        while not self.gameOver:
            # if numMoves % 1000 == 999:
            #     print("Done learning " + str(100 * (numMoves+1) / self.gameLength) + "%")
            action = self.agent.getAction(currentState)
            if not action is None:
                self.moveHistory.append(action)
                newState = currentState.do_move(action)
                if newState.fruit == newState.snake[0]:
                    self.agent.update(currentState, action, newState, newState.board_size)
                    newState.fruit = snake.place_fruit_help(newState.board_size, newState.snake)
                elif newState.dead_end():
                    self.agent.update(currentState, action, newState, -newState.board_size)
                else:
                    self.agent.update(currentState, action, newState, 0)
                currentState = newState
                numMoves += 1
                if numMoves == self.gameLength or self.currentState.illegal_state():
                    self.gameOver = True
            else:
                self.gameOver = True

        self.gameOver = False
        return numMoves
