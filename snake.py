import os
from random import randint

import pygame
import snake_problem
import learningGame
import learningAgents
import time
import pickle

BOARD_SIZE = 10

DIRECTIONS = {
    "UP": (0, 1),
    "RIGHT": (1, 0),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
}

DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']

snake, fruit = None, None


def init():
    """
    DON'T TOUCH THIS
    """
    global snake
    length = 3
    snake = [(1, length - j) for j in range(length)]

    place_fruit((3, 3))


def place_fruit(coord=None):
    """
    DON'T TOUCH THIS
    """
    global fruit
    if coord:
        fruit = coord
        return

    fruit = place_fruit_help(BOARD_SIZE)


def place_fruit_help(size, thisSnake=None):
    if thisSnake == None:
        thisSnake = snake
    while True:
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        if (x, y) not in thisSnake:
            return x, y


def illegal(next_head, size, curr_snake):
    return next_head[0] < 0 or next_head[0] >= size or next_head[1] < 0 or \
           next_head[1] >= size or next_head in curr_snake


def step(direction):
    """
    DON'T TOUCH THIS
    """
    old_head = snake[0]
    movement = DIRECTIONS[direction]
    new_head = (old_head[0] + movement[0], old_head[1] + movement[1])

    score = float(len(snake)) * 100 / (BOARD_SIZE ** 2)

    if illegal(new_head, BOARD_SIZE, snake):  # if move will result in loss
        return False

    snake.insert(0, new_head)

    if new_head == fruit:
        place_fruit()
    else:
        del snake[-1]  # delete the tail

    return score


def print_field():
    """
    DON'T TOUCH THIS
    """
    os.system('clear')
    print('=' * (BOARD_SIZE + 2))
    for y in range(BOARD_SIZE - 1, -1, -1):
        print('|', end='')
        for x in range(BOARD_SIZE):
            out = ' '
            if (x, y) in snake:
                out = 'X'
            elif (x, y) == fruit:
                out = 'O'
            print(out, end='')
        print('|')
    print('=' * (BOARD_SIZE + 2))


def start_display():
    pygame.init()
    s = pygame.display.set_mode((BOARD_SIZE * 10, BOARD_SIZE * 10))
    pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 0))
    headimage = pygame.Surface((10, 10))
    headimage.fill((0, 0, 255))
    return s, img, headimage, appleimage


def update_display(s, img, headimage, appleimage):
    s.fill((255, 255, 255))
    s.blit(headimage, (snake[0][0] * 10, (BOARD_SIZE - snake[0][1] - 1) * 10))
    for bit in snake[1:]:
        s.blit(img, (bit[0] * 10, (BOARD_SIZE - bit[1] - 1) * 10))
    s.blit(appleimage, (fruit[0] * 10, (BOARD_SIZE - fruit[1] - 1) * 10))
    pygame.display.flip()


def learn(learning_length):
    direction = 0
    state = snake_problem.SnakeState(snake, BOARD_SIZE, direction, fruit, 0)
    agent = learningAgents.ApproximateQAgent()
    game = learningGame.Game(agent, state, learning_length)
    game.learn()
    return game.agent


def learned_strategy(direction, depth, agent):
    problem = snake_problem.SnakeProblem(snake, fruit, BOARD_SIZE, direction, depth)
    actions = snake_problem.astar(problem, heuristic=snake_problem.learned_heuristic, agent=agent)
    if actions is None or len(actions) == 0:
        actions = [0]
    return actions


def search_strategy(direction, depth, agent=None):
    problem = snake_problem.SnakeProblem(snake, fruit, BOARD_SIZE, direction, depth)
    actions = snake_problem.astar(problem, heuristic=snake_problem.combined_heuristic)
    if actions is None or len(actions) == 0:
        actions = [0]
    return actions


def run(depth=3, strategy=search_strategy, learning_length=0, init_agent=None):
    init()

    agent = init_agent
    if learning_length > 0:
        agent = learn(learning_length)

    num_of_steps = 0
    score = 0
    actions = []

    direction = 0

    s, img, headimage, appleimage = start_display()

    while True:
        time_for_action = 0
        if len(actions) == 0:
            start = time.time()
            actions = strategy(direction, depth, agent)
            end = time.time()
            time_for_action = (end - start) * 1000
        waiting = int(max(0, 100 - time_for_action))
        pygame.time.wait(waiting)
        direction = actions[0]
        actions = actions[1:]
        num_of_steps += 1

        temp_score = step(DIRS[direction])
        if temp_score:
            score = temp_score
            if score == BOARD_SIZE ** 2 - 2 or num_of_steps > 30 * (BOARD_SIZE ** 2):
                pygame.quit()
                return score, num_of_steps, agent

        if not temp_score:
            pygame.quit()
            return score, num_of_steps, agent

        update_display(s, img, headimage, appleimage)


def saveQLearningAgent(learning_length):
    init()
    agent = learn(learning_length)
    with open('./learned heuristic size ' + str(learning_length), 'wb') as f:
        pickle.dump(agent.weights, f)


def loadQLearningAgent(filename):
    with open(filename, 'rb') as f:
        weights = pickle.load(f)
        agent = learningAgents.ApproximateQAgent()
        agent.weights = weights
        return agent


def QLearningTester():
    runs = 25
    for depth in {3, 4}:
        score, run_steps, agent = run(depth=depth, strategy=learned_strategy, learning_length=500)
        print("You're Dead" + "\nScore: " + str(score) + "%\nSteps: " + str(run_steps))
        print("Done learning!")
        scores = []
        steps = []
        times = []
        for i in range(runs):
            start = time.time()
            score, run_steps, agent = run(depth=depth, strategy=learned_strategy, learning_length=0, init_agent=agent)
            end = time.time()
            run_time = end - start
            scores.append(score)
            steps.append(run_steps)
            times.append(run_time)
            print("You're Dead (run " + str(i + 1) + " out of " + str(runs) + ")\nScore: " + str(score) + "%\nSteps: " + \
                  str(run_steps) + "\nTime: " + str(run_time))
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("\tdepth is - " + str(depth))
        print("\tOut of " + str(runs) + " runs - Avg. Score: " + str(float(sum(scores)) / runs) + "!")
        print("\tOne run had " + str(float(sum(steps)) / runs) + " steps in average!")
        print("\tOne run took " + str(float(sum(times)) / runs) + " seconds in average!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == '__main__':
    # start = time.time()
    # saveQLearningAgent(50)
    # end = time.time()
    # print(end-start)
    loadedAgent = loadQLearningAgent('learned heuristic size 800')
    run(depth=3, strategy=learned_strategy, init_agent=loadedAgent)
