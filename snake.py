import pygame
from pygame.locals import *
from random import randint
import os, sys
import search
import blokus_problems
import copy

ARRAY_SIZE = 60

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
    length = 10
    snake = [(1, length - i) for i in range(length)]

    place_fruit((ARRAY_SIZE // 2, ARRAY_SIZE // 2))


def place_fruit(coord=None):
    """
    DON'T TOUCH THIS
    """
    global fruit
    if coord:
        fruit = coord
        return

    while True:
        x = randint(0, ARRAY_SIZE - 1)
        y = randint(0, ARRAY_SIZE - 1)
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

    if illegal(new_head, ARRAY_SIZE, snake):  # if move will result in loss
        return False

    if new_head == fruit:
        place_fruit()
    else:
        del snake[-1]  # delete the tail

    snake.insert(0, new_head)
    return True


def print_field():
    """
    DON'T TOUCH THIS
    """
    os.system('clear')
    print('=' * (ARRAY_SIZE + 2))
    for y in range(ARRAY_SIZE - 1, -1, -1):
        print('|', end='')
        for x in range(ARRAY_SIZE):
            out = ' '
            if (x, y) in snake:
                out = 'X'
            elif (x, y) == fruit:
                out = 'O'
            print(out, end='')
        print('|')
    print('=' * (ARRAY_SIZE + 2))


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
    s = pygame.display.set_mode((ARRAY_SIZE * 10, ARRAY_SIZE * 10))
    # pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 0))
    clock = pygame.time.Clock()

    pygame.time.set_timer(1, 100)

    while True:
        e = pygame.event.wait()
        if e.type == QUIT:
            pygame.quit()
        else:
            direction = search_strategy(direction)
            print(DIRS[direction])
        # elif e.type == MOUSEBUTTONDOWN:
        #     if e.button == 3:
        #         direction = (direction+1) % 4
        #     elif e.button == 1:
        #         direction = (direction+3) % 4

        if not step(DIRS[direction]):
            pygame.quit()
            sys.exit(1)

        s.fill((255, 255, 255))
        for bit in snake:
            s.blit(img, (bit[0] * 10, (ARRAY_SIZE - bit[1] - 1) * 10))
        s.blit(appleimage, (fruit[0] * 10, (ARRAY_SIZE - fruit[1] - 1) * 10))
        pygame.display.flip()


def search_strategy(direction):
    problem = blokus_problems.SnakeProblem(copy.deepcopy(snake), fruit, ARRAY_SIZE, direction, 2*ARRAY_SIZE)
    actions = search.astar(problem, heuristic=blokus_problems.distance_heuristic)
    new_direction = (direction + actions[0]) % 4
    return new_direction


def strategy(direction):
    head = snake[0]
    xDistance = fruit[0] - head[0]
    yDistance = fruit[1] - head[1]
    movement = DIRECTIONS[DIRS[direction]]
    bad_directions = forbidden_directions(direction)
    if not not_forward(direction):
        if xDistance != 0:
            if movement[0] != 0:
                if movement[0] * xDistance > 0:
                    return direction
                else:
                    return (direction + 1) % 4
            else:
                if movement[1] * xDistance > 0:
                    return (direction + 1) % 4
                else:
                    return (direction + 3) % 4
        else:
            if movement[1] != 0:
                if movement[1] * yDistance > 0:
                    return direction
                else:
                    return (direction + 3) % 4
            else:
                if movement[0] * yDistance > 0:
                    return (direction + 3) % 4
                else:
                    return (direction + 1) % 4
    else:
        return (direction + 1) % 4


def forbidden_directions(direction):
    movements = [DIRECTIONS[DIRS[(direction + 2) % 4]]]
    for i in (0, 1, 3):
        old_head = snake[0]
        movement = DIRECTIONS[DIRS[(direction + i) % 4]]
        new_head = (old_head[0] + movement[0], old_head[1] + movement[1])
        if illegal(new_head, ARRAY_SIZE, snake):
            movements.append(i)
    return movements


def not_forward(direction):
    return 0 in forbidden_directions(direction)


run()
