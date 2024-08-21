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
GRID_COLOR = (50, 50, 50)  # Dark grey grid lines
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
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

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

def draw_statistics(grid, generation, births, deaths, avg_population, speed):
    live_cells = np.sum(grid)
    total_cells = GRID_WIDTH * GRID_HEIGHT
    percentage_alive = (live_cells / total_cells) * 100
    
    live_cells_text = f"Live Cells: {live_cells}"
    percentage_text = f"Percentage Alive: {percentage_alive:.2f}%"
    generation_text = f"Generation: {generation}"
    births_text = f"Births: {births}"
    deaths_text = f"Deaths: {deaths}"
    avg_population_text = f"Avg Population: {avg_population:.2f}"
    fps_text = f"FPS: {int(clock.get_fps())}"
    speed_text = f"Speed: {speed}"
    
    live_cells_surface = font.render(live_cells_text, True, GREEN)
    percentage_surface = font.render(percentage_text, True, GREEN)
    generation_surface = font.render(generation_text, True, GREEN)
    births_surface = font.render(births_text, True, GREEN)
    deaths_surface = font.render(deaths_text, True, GREEN)
    avg_population_surface = font.render(avg_population_text, True, GREEN)
    fps_surface = font.render(fps_text, True, GREEN)
    speed_surface = font.render(speed_text, True, GREEN)
    
    live_cells_rect = live_cells_surface.get_rect(topleft=(10, HEIGHT - 240))
    percentage_rect = percentage_surface.get_rect(topleft=(10, HEIGHT - 210))
    generation_rect = generation_surface.get_rect(topleft=(10, HEIGHT - 180))
    births_rect = births_surface.get_rect(topleft=(10, HEIGHT - 150))
    deaths_rect = deaths_surface.get_rect(topleft=(10, HEIGHT - 120))
    avg_population_rect = avg_population_surface.get_rect(topleft=(10, HEIGHT - 90))
    fps_rect = fps_surface.get_rect(topleft=(10, HEIGHT - 60))
    speed_rect = speed_surface.get_rect(topleft=(10, HEIGHT - 30))
    
    pygame.draw.rect(screen, TEXT_BG_COLOR, live_cells_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, percentage_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, generation_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, births_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, deaths_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, avg_population_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, fps_rect)
    pygame.draw.rect(screen, TEXT_BG_COLOR, speed_rect)
    
    screen.blit(live_cells_surface, live_cells_rect.topleft)
    screen.blit(percentage_surface, percentage_rect.topleft)
    screen.blit(generation_surface, generation_rect.topleft)
    screen.blit(births_surface, births_rect.topleft)
    screen.blit(deaths_surface, deaths_rect.topleft)
    screen.blit(avg_population_surface, avg_population_rect.topleft)
    screen.blit(fps_surface, fps_rect.topleft)
    screen.blit(speed_surface, speed_rect.topleft)

def main():
    grid = initialize_grid()
    running = True
    pause = False
    show_grid_lines = True  # Toggle for grid lines
    generation = 0
    total_population = np.sum(grid)
    speed = 10  # Initial speed
    dragging = False  # Add a flag to track dragging state
    erase_dragging = False  # Add a flag to track erasing state
    
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
                if event.key == pygame.K_g:
                    show_grid_lines = not show_grid_lines  # Toggle grid lines
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True  # Start dragging
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    grid[x, y] = 1 - grid[x, y]
                    total_population = np.sum(grid)
                if event.button == 3:  # Right mouse button
                    erase_dragging = True  # Start erasing
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    grid[x, y] = 0  # Erase cell
                    total_population = np.sum(grid)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False  # Stop dragging
                if event.button == 3:  # Right mouse button
                    erase_dragging = False  # Stop erasing
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                if dragging:
                    grid[x, y] = 1  # Make cell alive while dragging
                if erase_dragging:
                    grid[x, y] = 0  # Erase cell while dragging
                total_population = np.sum(grid)

        screen.fill(BLACK)
        draw_grid(grid)
        if show_grid_lines:
            draw_lines()  # Draw lines only if show_grid_lines is True
        
        if not pause:
            grid, births, deaths = update_grid(grid)
            generation += 1
            total_population += np.sum(grid)
            avg_population = total_population / generation if generation != 0 else 0
        
        draw_statistics(grid, generation, births, deaths, avg_population, speed)
        
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()