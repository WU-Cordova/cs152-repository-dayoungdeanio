import os
import time
import random
import copy
from projects.project2.kbhit import KBHit

# Constants
ROWS = 15
COLS = 15
LIVE_CELL = '\U0001F9A0'  # 🦠 Emoji for bacteria
DEAD_CELL = '-'  # Empty cell representation

def create_grid(rows, cols, random_seed=False):
    """Creates a 2D grid initialized with random bacteria or empty cells."""
    grid = [[LIVE_CELL if random_seed and random.random() < 0.5 else DEAD_CELL for _ in range(cols)] for _ in range(rows)]
    return grid

def display_grid(grid):
    """Prints the grid in a readable format."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears the console
    for row in grid:
        print(' '.join(row))
    print('\nPress Q to Quit, M for Manual Mode, A for Auto Mode')

def count_neighbors(grid, x, y):
    """Counts the number of live neighbors for a given cell."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == LIVE_CELL:
            count += 1
    return count

def next_generation(grid):
    """Computes the next generation of the grid."""
    new_grid = copy.deepcopy(grid)
    for i in range(ROWS):
        for j in range(COLS):
            neighbors = count_neighbors(grid, i, j)
            if grid[i][j] == LIVE_CELL:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = DEAD_CELL  # Dies
            else:
                if neighbors == 3:
                    new_grid[i][j] = LIVE_CELL  # Born
    return new_grid

def has_stabilized(history, new_grid):
    """Checks if the grid has stabilized by comparing with history."""
    return any(prev_grid == new_grid for prev_grid in history)

def game_loop():
    """Runs the Game of Life simulation with automatic and manual modes."""
    kb = KBHit()
    grid = create_grid(ROWS, COLS, random_seed=True)
    history = []
    manual_mode = False
    
    while True:
        display_grid(grid)
        history.append(copy.deepcopy(grid))
        if len(history) > 5:
            history.pop(0)  # Keep only last 5 states
        
        if has_stabilized(history, grid):
            print("Simulation has stabilized. Press any key to restart or Q to quit.")
            break
        
        grid = next_generation(grid)
        
        if manual_mode:
            while True:
                if kb.kbhit():
                    key = kb.getch().lower()
                    if key == 'q':
                        return
                    elif key == 'a':
                        manual_mode = False
                        break
                    elif key == 'm' or key == 's':
                        break  # Step forward
        else:
            time.sleep(1)
            if kb.kbhit():
                key = kb.getch().lower()
                if key == 'q':
                    return
                elif key == 'm':
                    manual_mode = True

game_loop()
