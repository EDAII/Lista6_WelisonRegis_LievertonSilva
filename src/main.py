import constants
import pygame
import time
import random
from threading import Thread
import os

print("""
 _        _    ____ ___ ____  ___ _   _ _____ ___          _   ___  
| |      / \  | __ )_ _|  _ \|_ _| \ | |_   _/ _ \  __   _/ | / _ \ 
| |     / _ \ |  _ \| || |_) || ||  \| | | || | | | \ \ / / || | | |
| |___ / ___ \| |_) | ||  _ < | || |\  | | || |_| |  \ V /| || |_| |
|_____/_/   \_\____/___|_| \_\___|_| \_| |_| \___/    \_/ |_(_)___/ 

""")

while True:
    GRID_WIDTH = int(input('Digite a largura do labirinto (1-50): '))
    GRID_HEIGHT = int(input('Digite a altura do labirinto (1-30): '))
    print('\n')

    if GRID_WIDTH >= 1 and GRID_WIDTH <= 50 and GRID_HEIGHT >= 1 and GRID_HEIGHT <= 30:
        break

os.system('cls' if os.name == 'nt' else 'clear')

print('COMANDOS:')
print('> ↑ (seta para cima): aumenta a velocidade da animação')
print('> ↓ (seta para baixo): diminui a velocidade da animação')


pygame.init()
pygame.display.set_caption("Labirinto v1.0")
screen = pygame.display.set_mode(((GRID_WIDTH+1)*20, (GRID_HEIGHT+1)*20))
clock = pygame.time.Clock()


grid = []
visited = []
stack = []
solution = {}


def generate_grid(x, y):
    for i in range(1, GRID_HEIGHT):
        y = y + constants.CELL_WIDTH
        x = 20
        for j in range(1, GRID_WIDTH):
            grid.append((x, y))
            x = x + constants.CELL_WIDTH

def start_point(x, y):
    pygame.draw.rect(screen, constants.GREEN, (x+2, y+2, 16, 16), 0)
    pygame.display.update()
    

def end_point(x, y):
    pygame.draw.rect(screen, constants.RED, (x+2, y+2, 16, 16), 0)
    pygame.display.update()

def solution_line(x, y, x1, y1):
    pygame.draw.line(screen, constants.RED, (x+10.5, y+10.5), (x1+10.5, y1+10.5), 3)
    pygame.display.update()

def expand_down(x, y):
    pygame.draw.rect(screen, constants.GREY, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def expand_up(x, y):
    pygame.draw.rect(screen, constants.GREY, (x + 1, y - constants.CELL_WIDTH + 1, 19, 39), 0)
    pygame.display.update()


def expand_left(x, y):
    pygame.draw.rect(screen, constants.GREY, (x - constants.CELL_WIDTH + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def expand_right(x, y):
    pygame.draw.rect(screen, constants.GREY, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, constants.GREY, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(screen, constants.BLUE, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


def solution_cell(x, y):
    pygame.draw.rect(screen, constants.BLUE, (x+8, y+8, 5, 5), 0)
    pygame.display.update()


def make_maze(x, y):
    single_cell(x, y)
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        time.sleep(velocity)
        cell = []

        if (x, y + constants.CELL_WIDTH) not in visited and (x, y + constants.CELL_WIDTH) in grid:
            cell.append("down")

        if (x, y - constants.CELL_WIDTH) not in visited and (x, y - constants.CELL_WIDTH) in grid:
            cell.append("up")

        if (x + constants.CELL_WIDTH, y) not in visited and (x + constants.CELL_WIDTH, y) in grid:
            cell.append("right")

        if (x - constants.CELL_WIDTH, y) not in visited and (x - constants.CELL_WIDTH, y) in grid:
            cell.append("left")

        if len(cell) > 0:
            cell_chosen = (random.choice(cell))

            if cell_chosen == "right":
                expand_right(x, y)
                solution[(x + constants.CELL_WIDTH, y)] = x, y
                x = x + constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "left":
                expand_left(x, y)
                solution[(x - constants.CELL_WIDTH, y)] = x, y
                x = x - constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                expand_down(x, y)
                solution[(x, y + constants.CELL_WIDTH)] = x, y
                y = y + constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                expand_up(x, y)
                solution[(x, y - constants.CELL_WIDTH)] = x, y
                y = y - constants.CELL_WIDTH
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()
            single_cell(x, y)
            time.sleep(velocity)
            backtracking_cell(x, y)


def solve_maze(x, y):
    solution_cell(x, y)
    x1, y1 = GRID_WIDTH*20, GRID_HEIGHT*20
    while (x1, y1) != (20, 20):
        x1, y1 = solution[x, y]

        solution_cell(x1, y1)        
        solution_line(x, y, x1, y1)

        x, y = x1, y1

        time.sleep(velocity)

velocity = 0.1

def pygame_monitor():
    running = True
    global velocity

    while running:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if velocity <= 0.3:
                        velocity += 0.01
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if velocity >= 0.02:
                        velocity -= 0.01


def main():
    x, y = 20, 20
    generate_grid(0, 0)
    make_maze(x, y)
    start_point(20, 20)
    end_point((GRID_WIDTH-1)*20, (GRID_HEIGHT-1)*20)
    solve_maze((GRID_WIDTH-1)*20, (GRID_HEIGHT-1)*20)

if __name__ == '__main__':
    t1 = Thread(target = pygame_monitor)
    t2 = Thread(target = main)

    t1.start()
    t2.start()

    t1.join()
    t2.join()