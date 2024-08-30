# Cellular Automata Simulation

This project is a simulation of cellular automata, including classic and variant rulesets such as Conway's Game of Life, HighLife, and Day & Night. The simulation is implemented using Pygame for visualization and NumPy for grid manipulation.

## Features

![Simulation Screenshot](https://github.com/user-attachments/assets/a18f030a-8768-4f47-bc3c-12b3c19dbb7a)

- **Grid Initialization**: Randomly generates an initial grid of live and dead cells.
- **Rule Variants**: Supports Conway's Game of Life, HighLife, and Day & Night rulesets.
- **Interactive Tools**: Add or erase cells with a brush tool, adjust brush size, and toggle grid lines.
- **Statistics**: Displays live cell count, percentage of alive cells, and other statistics.
- **Save and Load**: Save and load grid states to/from JSON files and images.
- **Visualization**: Save grid states as images and visualize live cells over time.

## Installation

To run this simulation, ensure you have Python 3 installed. You also need to install the required libraries. You can install them using pip:

```bash
pip install pygame numpy matplotlib
```

## Usage

1. **Run the Simulation**: Execute the script with Python:

   ```bash
   python main.py
   ```

2. **Controls**:
   - `SPACE`: Pause/Resume the simulation.
   - `R`: Reset the grid to a random state.
   - `UP`/`DOWN`: Increase/Decrease simulation speed.
   - `G`: Toggle grid lines on/off.
   - `S`: Save the current grid to a JSON file.
   - `L`: Load a saved grid from a JSON file.
   - `I`: Save the current grid as an image.
   - `O`: Load a grid from an image.
   - `H`: Toggle help tooltip on/off.
   - `LEFT`/`RIGHT`: Decrease/Increase brush size.
   - **Left Click**: Add cells with the brush tool.
   - **Right Click**: Erase cells with the brush tool.

3. **Menu**:
   - On startup, you will be prompted to select a game mode:
     - `1`: Conway's Game of Life (B3/S23)
     - `2`: HighLife (B36/S23)
     - `3`: Day & Night (B3678/S34678)

## Configuration

The simulation reads configuration settings from `config.json`. If the file does not exist, it will be created with default settings. You can adjust parameters such as screen width, height, cell size, colors, font size, and speed.

## Acknowledgements

- [Pygame](https://www.pygame.org/) for game development and rendering.
- [NumPy](https://numpy.org/) for numerical computations.
- [Matplotlib](https://matplotlib.org/) for plotting live cell statistics.
