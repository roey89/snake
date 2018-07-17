import os
import time
from random import randint

import pygame

import snake_problem

BOARD_SIZE = 10

DIRECTIONS = {
    "UP": (0, 1),
    "RIGHT": (1, 0),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
}

snake, fruit = None, None


def init():
    """
    DON'T TOUCH THIS
    """
    global snake
    length = 3
    snake = [(1, length - j) for j in range(length)]

    place_fruit()


def place_fruit(coord=None):
    """
    DON'T TOUCH THIS
    """
    global fruit
    if coord:
        fruit = coord
        return

    while True:
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)
        if (x, y) not in snake:
            fruit = x, y
            return


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
        print("You're Dead\nScore: " + str(score) + "%")
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


def test():
    global fruit
    init()
    assert step('UP')

    assert snake == [(0, 3), (0, 2), (0, 1)]

    fruit = (0, 4)
    assert step('UP')

    assert snake == [(0, 4), (0, 3), (0, 2), (0, 1)]
    assert fruit != (0, 4)

    assert not step('DOWN'), 'Kdyz nacouvam do sebe, umru!'


DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']


def run():
    init()

    direction = 0

    pygame.init()
    s = pygame.display.set_mode((BOARD_SIZE * 10, BOARD_SIZE * 10))
    pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 0))
    headimage = pygame.Surface((10, 10))
    headimage.fill((0, 0, 255))
    clock = pygame.time.Clock()

    pygame.time.set_timer(1, 100)

    score = 0
    actions = []
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            pygame.quit()
        else:
            if len(actions) == 0:
                # direction = 0
                actions = search_strategy(direction)
            direction = actions[0]
            actions = actions[1:]
        # elif e.type == MOUSEBUTTONDOWN:
        #     if e.button == 3:
        #         direction = (direction+1) % 4
        #     elif e.button == 1:
        #         direction = (direction+3) % 4

        temp_score = step(DIRS[direction])
        if temp_score:
            score = temp_score

        if not temp_score:
            pygame.quit()
            return score

        s.fill((255, 255, 255))
        s.blit(headimage, (snake[0][0] * 10, (BOARD_SIZE - snake[0][1] - 1) * 10))
        for bit in snake[1:]:
            s.blit(img, (bit[0] * 10, (BOARD_SIZE - bit[1] - 1) * 10))
        s.blit(appleimage, (fruit[0] * 10, (BOARD_SIZE - fruit[1] - 1) * 10))
        pygame.display.flip()


def search_strategy(direction):
    problem = snake_problem.SnakeProblem(snake, fruit, BOARD_SIZE, direction, BOARD_SIZE ** 3 + 100)
    actions = snake_problem.astar(problem, heuristic=snake_problem.distance_heuristic)
    if actions is None or len(actions) == 0:
        actions = [0]
    return actions


def strategy(direction):
    head = snake[0]
    xDistance = fruit[0] - head[0]
    yDistance = fruit[1] - head[1]
    movement = DIRECTIONS[DIRS[direction]]
    bad_directions = forbidden_directions(direction)
    move = None
    if not not_forward(direction):
        if xDistance != 0:
            if movement[0] != 0:
                if movement[0] * xDistance > 0:
                    move = direction
                else:
                    move = (direction + 1) % 4
            else:
                if movement[1] * xDistance > 0:
                    move = (direction + 1) % 4
                else:
                    move = (direction + 3) % 4
        else:
            if movement[1] != 0:
                if movement[1] * yDistance > 0:
                    move = direction
                else:
                    move = (direction + 3) % 4
            else:
                if movement[0] * yDistance > 0:
                    move = (direction + 3) % 4
                else:
                    move = (direction + 1) % 4
    if move is None:
        return (direction + 1) % 4

    return move


def forbidden_directions(direction):
    movements = [DIRECTIONS[DIRS[(direction + 2) % 4]]]
    for i in (0, 1, 3):
        old_head = snake[0]
        movement = DIRECTIONS[DIRS[(direction + i) % 4]]
        new_head = (old_head[0] + movement[0], old_head[1] + movement[1])
        if illegal(new_head, BOARD_SIZE, snake):
            movements.append(i)
    return movements


def not_forward(direction):
    return 0 in forbidden_directions(direction)


if __name__ == '__main__':
    start = time.time()
    runs = 25
    scores = []
    for i in range(runs):
        scores.append(run())
    end = time.time()
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("\tOut of " + str(runs) + " runs - Avg. Score: " + str(float(sum(scores)) / runs) + "!")
    print("\tOne run took " + str(int(end - start) / runs) + " seconds in average!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
