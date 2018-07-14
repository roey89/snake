"""
In search.py, you will implement generic search algorithms
"""

from util import Stack
from util import Queue
from util import PriorityQueue
import util


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


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a lstt of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = Stack()
    been_there = []
    fringe.push((problem.get_start_state(), []))
    while True:
        if fringe.isEmpty():
            return None
        current_board, actions = fringe.pop()
        if problem.is_goal_state(current_board):
            return actions
        if current_board not in been_there:

            successors = problem.get_successors(current_board)
            for item in successors:
                temp_lst = actions[:]
                temp_lst.append(item[1])
                fringe.push((item[0], temp_lst))
            been_there.append(current_board)


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = Queue()
    been_there = []
    fringe.push((problem.get_start_state(), []))
    while True:
        if fringe.isEmpty():
            return None
        current_board, actions = fringe.pop()
        if problem.is_goal_state(current_board):
            return actions
        if current_board not in been_there:

            successors = problem.get_successors(current_board)
            for item in successors:
                temp_lst = actions[:]
                temp_lst.append(item[1])
                fringe.push((item[0], temp_lst))
            been_there.append(current_board)


class Duo(list):
    def __init__(self, lst):
        self.lst = lst


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    fringe = PriorityQueue()
    been_there = []
    temp_item = Duo([problem.get_start_state(), []])
    fringe.push(temp_item, 0)

    while True:
        if fringe.isEmpty():
            return None
        current_board, actions = fringe.pop().lst
        if problem.is_goal_state(current_board):
            return actions
        if current_board not in been_there:

            successors = problem.get_successors(current_board)
            for item in successors:
                if item[0] not in been_there:

                    temp_lst = actions[:]
                    temp_lst.append(item[1])
                    temp_item = Duo([item[0], temp_lst])
                    fringe.push(temp_item, problem.get_cost_of_actions(temp_lst))
            been_there.append(current_board)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    fringe = PriorityQueue()
    been_there = []
    temp_item = Duo([problem.get_start_state(), []])
    fringe.push(temp_item, 0)
    while True:
        if fringe.isEmpty():
            return None
        current_board, actions = fringe.pop().lst
        if problem.is_goal_state(current_board):
            return actions
        if current_board not in been_there:
            for item in problem.get_successors(current_board):
                temp_actions = actions[:]
                temp_actions.append(item[1])
                temp_item = Duo([item[0], temp_actions])
                fringe.push(temp_item, problem.get_cost_of_actions(temp_actions) + heuristic(item[0], problem))
            been_there.append(current_board)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
