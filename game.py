import pygame
import numpy as np
import matplotlib.pyplot as plt
import json
import os

pygame.init()

# Default configuration
default_config = {
    "WIDTH": 800,
    "HEIGHT": 600,
    "CELL_SIZE": 10,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GREEN": (0, 255, 0),
    "GRID_COLOR": (50, 50, 50),
    "TEXT_BG_COLOR": (50, 50, 50),
    "FONT_SIZE": 36,
    "SPEED": 10
}

def load_config(filename="config.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            config = json.load(f)
    else:
        with open(filename, "w") as f:
            json.dump(default_config, f, indent=4)
        config = default_config
    return config

config = load_config()

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
CELL_SIZE = config["CELL_SIZE"]
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = config["WHITE"]
BLACK = config["BLACK"]
GREEN = config["GREEN"]
GRID_COLOR = config["GRID_COLOR"]
TEXT_BG_COLOR = config["TEXT_BG_COLOR"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, config["FONT_SIZE"])

def initialize_grid():
    return np.random.randint(2, size=(GRID_WIDTH, GRID_HEIGHT))

def initialize_age_grid():
    return np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

def save_grid(grid, filename="saved_grid.json"):
    with open(filename, "w") as f:
        json.dump(grid.tolist(), f)

def load_grid(filename="saved_grid.json"):
    with open(filename, "r") as f:
        grid = np.array(json.load(f))
    return grid

def save_grid_as_image(grid, filename="saved_grid.png"):
    image_surface = pygame.Surface((WIDTH, HEIGHT))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = WHITE if grid[x, y] == 1 else BLACK
            pygame.draw.rect(image_surface, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.image.save(image_surface, filename)

def load_grid_from_image(filename="saved_grid.png"):
    image_surface = pygame.image.load(filename)
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = image_surface.get_at((x * CELL_SIZE, y * CELL_SIZE))
            grid[x, y] = 1 if color == WHITE else 0
    return grid

def draw_grid(grid, age_grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] == 1:
                age = age_grid[x, y]
                color = (0, min(255, age * 10), 0)  # Green color with intensity based on age
            else:
                color = BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_lines():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def update_grid(grid, age_grid):
    padded_grid = np.pad(grid, pad_width=1, mode='wrap')
    neighbor_sum = (
        padded_grid[:-2, :-2] + padded_grid[:-2, 1:-1] + padded_grid[:-2, 2:] +
        padded_grid[1:-1, :-2] + padded_grid[1:-1, 2:] +
        padded_grid[2:, :-2] + padded_grid[2:, 1:-1] + padded_grid[2:, 2:]
    )
    births = (grid == 0) & (neighbor_sum == 3)
    deaths = (grid == 1) & ((neighbor_sum < 2) | (neighbor_sum > 3))
    new_grid = np.copy(grid)
    new_grid[births] = 1
    new_grid[deaths] = 0
    age_grid[births] = 1
    age_grid[deaths] = 0
    age_grid[new_grid == 1] += 1
    return new_grid, age_grid, np.sum(births), np.sum(deaths)

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
    age_grid = initialize_age_grid()
    running = True
    pause = False
    show_grid_lines = True
    generation = 0
    total_population = np.sum(grid)
    speed = config["SPEED"]
    dragging = False
    erase_dragging = False
    live_cells_history = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_r:
                    grid = initialize_grid()
                    age_grid = initialize_age_grid()
                    generation = 0
                    total_population = np.sum(grid)
                    live_cells_history = []
                if event.key == pygame.K_UP:
                    speed += 1
                if event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)
                if event.key == pygame.K_g:
                    show_grid_lines = not show_grid_lines
                if event.key == pygame.K_s:
                    save_grid(grid)
                if event.key == pygame.K_l:
                    grid = load_grid()
                if event.key == pygame.K_i:
                    save_grid_as_image(grid)
                if event.key == pygame.K_o:
                    grid = load_grid_from_image()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    grid[x, y] = 1 - grid[x, y]
                    total_population = np.sum(grid)
                if event.button == 3:
                    erase_dragging = True
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    grid[x, y] = 0
                    total_population = np.sum(grid)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                if event.button == 3:
                    erase_dragging = False
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                if dragging:
                    grid[x, y] = 1
                if erase_dragging:
                    grid[x, y] = 0
                total_population = np.sum(grid)

        screen.fill(BLACK)
        draw_grid(grid, age_grid)
        if show_grid_lines:
            draw_lines()
        
        if not pause:
            grid, age_grid, births, deaths = update_grid(grid, age_grid)
            generation += 1
            total_population += np.sum(grid)
            avg_population = total_population / generation if generation != 0 else 0
            live_cells_history.append(np.sum(grid))

        draw_statistics(grid, generation, births, deaths, avg_population, speed)
        
        pygame.display.flip()
        clock.tick(speed)

    plt.figure(figsize=(10, 5))
    plt.plot(live_cells_history, label='Live Cells Over Time', color='green')
    plt.xlabel('Generation')
    plt.ylabel('Live Cells')
    plt.title('Live Cells Over Time')
    plt.legend()
    plt.show()

    pygame.quit()

if __name__ == "__main__":
    main()