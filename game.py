import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Conway\'s Game of Life')

clock = pygame.time.Clock()

def initialize_grid():
    return np.random.randint(2, size=(GRID_WIDTH, GRID_HEIGHT))

def draw_grid(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = WHITE if grid[x, y] == 1 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_lines():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def update_grid(grid):
    new_grid = np.copy(grid)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            total = (grid[(x-1)%GRID_WIDTH, (y-1)%GRID_HEIGHT] + grid[(x-1)%GRID_WIDTH, y] + grid[(x-1)%GRID_WIDTH, (y+1)%GRID_HEIGHT] +
                     grid[x, (y-1)%GRID_HEIGHT] + grid[x, (y+1)%GRID_HEIGHT] +
                     grid[(x+1)%GRID_WIDTH, (y-1)%GRID_HEIGHT] + grid[(x+1)%GRID_WIDTH, y] + grid[(x+1)%GRID_WIDTH, (y+1)%GRID_HEIGHT])
            
            if grid[x, y] == 1 and (total < 2 or total > 3):
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and total == 3:
                new_grid[x, y] = 1
    return new_grid

def main():
    grid = initialize_grid()
    running = True
    pause = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_r:
                    grid = initialize_grid()

        screen.fill(BLACK)
        draw_lines()
        draw_grid(grid)
        
        if not pause:
            grid = update_grid(grid)
        
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
