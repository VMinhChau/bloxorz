from functions import view_2d_solution
import pygame
import sys
from functions import convert_solution_map

screen_scale = 50
BLOCK_COLOR = '#b27466'
TILE_COLOR = '#e0d9e0'
TILE_FRAGILE = (255,153,51)
BUTTON_SPLIT_COLOR = (178,255,102)
EMPTY_SPACE = '#FFFFFF'
EMPTY = '#FFFFFF'
UGLY_PINK = (255, 0, 255)
BLACK = (0,0,0)
PINK_FOR_CIRCLE = (191, 52, 194)
GRAY = (33,33,33)
WHITE = '#FFFFFF'

def get_tile_color(tile_contents):
    tile_color = EMPTY
    if tile_contents == ".":
        tile_color = EMPTY_SPACE
    if tile_contents == "#":
        tile_color = TILE_COLOR
        
    if tile_contents == "=":
        tile_color = TILE_FRAGILE
    if tile_contents == "G":
        tile_color = '#8798a5'
    if tile_contents == "+":
        tile_color = BLOCK_COLOR
    return tile_color


def init(row, col):
    screen_width = screen_scale * col
    screen_height = screen_scale * row
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bloxorz Solver")
    icon = pygame.image.load("resources/block.png")
    pygame.display.set_icon(icon)
    # screen.fill(TILE_COLOR)
    return screen


def draw_grid(row, col, screen):
    for i in range(col):
        new_height = round(i * screen_scale)
        new_width = round(i * screen_scale)
        pygame.draw.line(screen, WHITE, (0, new_height), (col * screen_scale, new_height), 2)
        pygame.draw.line(screen, WHITE, (new_width, 0), (new_width, row * screen_scale), 2)


def draw_map(screen, s):
    for j, tile in enumerate(s):
        for i, tile_contents in enumerate(tile):
            rectangle = pygame.Rect(i * screen_scale, j * screen_scale, screen_scale, screen_scale)
            pygame.draw.rect(screen, get_tile_color(tile_contents), rectangle)
            if tile_contents == 'o':
                pygame.draw.circle(screen, GRAY, (i * screen_scale + int(screen_scale / 2),
                                                             j * screen_scale + int(screen_scale / 2)), 20, 8)
            if tile_contents == 'x':
                pygame.draw.line(screen, GRAY, (i * screen_scale + 5, j * screen_scale + 5),(
                                   (i+1) * screen_scale - 5, (j+1) * screen_scale - 5), 9)
                pygame.draw.line(screen, GRAY, (
                    (i + 1) * screen_scale - 5, j * screen_scale + 5), (
                    (i) * screen_scale + 5, (j + 1) * screen_scale - 5), 9)
            if tile_contents == '@':
                pygame.draw.circle(screen, GRAY, (i * screen_scale + screen_scale//2,
                                                       j * screen_scale + screen_scale//2), 22, 7,
                                                            True, False, True, False)


def game_loop(row, col, solution, screen):
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT:
                    if i < len(solution) - 1:
                        i += 1
                elif event.key == pygame.K_LEFT:
                    if i > 0:
                        i -= 1
        draw_map(screen, solution[i].game_map)
        draw_grid(row, col, screen)
        pygame.display.update()


def draw_pygame(solution, row, col):
    convert_solution_map(solution)
    screen = init(row, col)
    game_loop(row, col, solution, screen)


def draw_raw_solution(solution):
    cnt = 0
    for i in solution:
        print("Showing All", len(solution), "Steps")
        cnt += 1
        print("\nStep:", cnt)
        print()
        view_2d_solution(i)
        print("====================================")
    print("Success !!!")
