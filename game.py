import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
TEXT_BG_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Conway\'s Game of Life')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

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
    births = deaths = 0
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            total = (grid[(x-1)%GRID_WIDTH, (y-1)%GRID_HEIGHT] + grid[(x-1)%GRID_WIDTH, y] + grid[(x-1)%GRID_WIDTH, (y+1)%GRID_HEIGHT] +
                     grid[x, (y-1)%GRID_HEIGHT] + grid[x, (y+1)%GRID_HEIGHT] +
                     grid[(x+1)%GRID_WIDTH, (y-1)%GRID_HEIGHT] + grid[(x+1)%GRID_WIDTH, y] + grid[(x+1)%GRID_WIDTH, (y+1)%GRID_HEIGHT])
            
            if grid[x, y] == 1 and (total < 2 or total > 3):
                new_grid[x, y] = 0
                deaths += 1
            elif grid[x, y] == 0 and total == 3:
                new_grid[x, y] = 1
                births += 1
    return new_grid, births, deaths

def draw_statistics(grid, generation, births, deaths, avg_population):
    live_cells = np.sum(grid)
    total_cells = GRID_WIDTH * GRID_HEIGHT
    percentage_alive = (live_cells / total_cells) * 100
    
    live_cells_text = f"Live Cells: {live_cells}"
    percentage_text = f"Percentage Alive: {percentage_alive:.2f}%"
    generation_text = f"Generation: {generation}"
    births_text = f"Births: {births}"
    deaths_text = f"Deaths: {deaths}"
    avg_population_text = f"Avg Population: {avg_population:.2f}"
    
    live_cells_surface = font.render(live_cells_text, True, GREEN)
    percentage_surface = font.render(percentage_text, True, GREEN)
    generation_surface = font.render(generation_text, True, GREEN)
    births_surface = font.render(births_text, True, GREEN)
    deaths_surface = font.render(deaths_text, True, GREEN)
    avg_population_surface = font.render(avg_population_text, True, GREEN)
    
    live_cells_rect = live_cells_surface.get_rect(topleft=(10, HEIGHT - 180))
    percentage_rect = percentage_surface.get_rect(topleft=(10, HEIGHT - 150))
    generation_rect = generation_surface.get_rect(topleft=(10, HEIGHT - 120))
    births_rect = births_surface.get_rect(topleft=(10, HEIGHT - 90))
    deaths_rect = deaths_surface.get_rect(topleft=(10, HEIGHT - 60))
    avg_population_rect = avg_population_surface.get_rect(topleft=(10, HEIGHT - 30))
    
    pygame.draw.rect(screen, TEXT_BG_COLOR, live_cells_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, percentage_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, generation_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, births_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, deaths_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, avg_population_rect)
    
    screen.blit(live_cells_surface, live_cells_rect.topleft)
    screen.blit(percentage_surface, percentage_rect.topleft)
    screen.blit(generation_surface, generation_rect.topleft)
    screen.blit(births_surface, births_rect.topleft)
    screen.blit(deaths_surface, deaths_rect.topleft)
    screen.blit(avg_population_surface, avg_population_rect.topleft)

def main():
    grid = initialize_grid()
    running = True
    pause = False
    generation = 0
    total_population = np.sum(grid)
    speed = 10  # Initial speed
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_r:
                    grid = initialize_grid()
                    generation = 0
                    total_population = np.sum(grid)
                if event.key == pygame.K_UP:
                    speed += 1  # Increase speed
                if event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)  # Decrease speed but not below 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                grid[x, y] = 1 - grid[x, y]
                total_population = np.sum(grid)

        screen.fill(BLACK)
        draw_lines()
        draw_grid(grid)
        
        if not pause:
            grid, births, deaths = update_grid(grid)
            generation += 1
            total_population += np.sum(grid)
            avg_population = total_population / generation if generation != 0 else 0
        
        draw_statistics(grid, generation, births, deaths, avg_population)
        
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()