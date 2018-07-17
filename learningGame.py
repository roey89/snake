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

    def run(self):
        numMoves = 0

        while not self.gameOver:
            action = self.agent.getAction(self.currentState)
            self.moveHistory.append(action)
            newState = self.currentState.do_move(action)
            if newState.fruit == newState.snake[0]:
                self.agent.update(self.currentState, action, newState, newState.board_size)
                newState.fruit = snake.place_fruit_help(newState.board_size, newState.snake)
            else:
                self.agent.update(self.currentState, action, newState, 0)
            self.currentState = newState
            numMoves += 1
            if numMoves == self.gameLength or self.currentState.illegal_state():
                self.gameOver = True
