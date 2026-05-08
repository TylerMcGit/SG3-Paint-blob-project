"""
Language: Python 3
Developed in PyCharm, and tested on Thonny.

Authors:
    Tyler Mcfarland
    Jacob Schaefer
    Caleb Hackmann
    Jory Ehman
    Hunter Sindelar
...

CS 4500 - SG3: Paint Blobs
Date of Submission: 05/08/2026

Purpose:
    This program simulates random paint blobs dropping onto a
    square canvas. Each drop lands on a random square and gets
    a random color (red, green, blue). Only the latest blob on
    each square is visible.
 
    Stats are printed when all squares are first painted, and
    again after MaxT total drops.

Data Structures:
    Canvas.grid    - 2D list of lists; each cell stores a list of color values (blob history for that square).
    Canvas.history - List of (row, col, color) tuples recording every blob drop in order.
    NumPy 2D arrays are used for rendering the grid with matplotlib.

Packages:
    random     - Generates random grid positions and blob colors.
    matplotlib - Renders the canvas grid, animation, and comparison graphs.
    numpy      - Creates 2D arrays for matplotlib's imshow display.

External Files: None

Outside Resources:
    https://www.geeksforgeeks.org/python/matplotlib-pyplot-ion-in-python/
        - Used for interactive plotting with plt.ion() and plt.ioff() in the animate method.
    https://www.geeksforgeeks.org/python/matplotlib-tutorial/
        - General matplotlib usage for plotting and displaying graphs.
    https://docs.python.org/3/library/random.html
        - Reference for random.randint() and random.choice() usage.
    https://docs.python.org/3/tutorial/datastructures.html
        - Reference for Python list operations and comprehensions.

Revision Information:
    Mon Apr 27 - Start of Project
    Mon Apr 29 - Ver 0.1
    Thu Apr 30 - Ver 0.2
    Fri May 1 - Ver 0.3
    Sat May 2 - Ver 0.4
    Thu May 7 - Ver 1.0
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

INTRO_N    = 10   # grid dimension for the intro simulation
INTRO_MAXT = 300  # number of blobs for the intro simulation


def displayStartupInfo():
    # Prints the project summary and author information to the console.
    # Parameters: None
    # Returns: None
    print("""
        SG3: Paint Blobs
        Project Authors: Caleb Hackmann, Jory Ehman, Tyler Mcfarland, Hunter Sindelar,  Jacob Schaefe
 
Summary:
    This program simulates random paint blobs dropping onto a
    square canvas. Each drop lands on a random square and gets
    a random color (red, green, blue). Only the latest blob on
    each square is visible.
 
    Stats are printed when all squares are first painted, and
    again after MaxT total drops.
""")

class Canvas:
    def __init__(self, n, maxt):
        # Initializes a Canvas with an n x n grid and a maximum of maxt blob drops.
        # Parameters:
        #   n    - grid dimension (n x n)
        #   maxt - total number of blobs to drop
        # Returns: None
        self.n = n
        self.maxt = maxt
        self.grid = [[[] for _ in range(n)] for _ in range(n)]
        self.history = []
        self.fill_t = None

    def generate(self):
        # Drops maxt random blobs onto the grid. Each gets a random position
        # and color (1=red, 2=green, 3=blue). Records when all squares are first covered.
        # Parameters: None
        # Returns: None
        colors = [1, 2, 3]
        for t in range(1, self.maxt + 1):
            r, c = random.randint(0, self.n - 1), random.randint(0, self.n - 1)
            color = random.choice(colors)

            self.grid[r][c].append(color)
            self.history.append((r, c, color))

            # Check if canvas has been filled
            if self.fill_t is None:
                if all(len(sq) > 0 for row in self.grid for sq in row):
                    self.fill_t = t

    def display(self):
        # Displays the final canvas state as a colored grid using matplotlib.
        # Parameters: None
        # Returns: None
        final_view = np.zeros((self.n, self.n))

        # Grab the last color from each square
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c]:
                    final_view[r][c] = self.grid[r][c][-1]

        # plot
        fig, ax = plt.subplots()
        cmap = ListedColormap(['white', 'red', 'green', 'blue'])
        ax.imshow(final_view, cmap=cmap, vmin=0, vmax=3, extent=[0, self.n, 0, self.n])
        ax.set_title(f"Final Canvas State\nTotal Blobs: {self.maxt}")
        ax.set_xticks(range(self.n + 1))
        ax.set_yticks(range(self.n + 1))
        ax.grid(True)

        plt.show()

    def animate(self):
        # Animates the blob-dropping process using matplotlib interactive mode.
        # Pauses when the canvas is first fully covered.
        # Parameters: None
        # Returns: None
        display_grid = np.zeros((self.n, self.n))
        plt.ion()  # Interactive mode (ref: geeksforgeeks.org/python/matplotlib-pyplot-ion-in-python/)
        fig, ax = plt.subplots()

        cmap = ListedColormap(['white', 'red', 'green', 'blue'])
        im = ax.imshow(display_grid, cmap=cmap, vmin=0, vmax=3, extent=[0, self.n, 0, self.n])

        # This block adjusts the refresh rate of the display window based on the length of the simulation.
        # It will dramatically reduce the simulation time for large maxT values and makes it stable
        update_freq = 1 if self.maxt <= 500 else self.maxt // 100
        for t, (r, c, color) in enumerate(self.history, 1):
            display_grid[r][c] = color

            if t % update_freq == 0 or t == self.fill_t or t == self.maxt:
                im.set_data(display_grid)
                ax.set_title(f"Blobs: {t}/{self.maxt}")
                plt.pause(0.02)

            if t == self.fill_t:
                print(f"Canvas filled at {t} seconds.")
                plt.pause(2)

        plt.ioff()
        plt.show()

    def get_stats(self):
        # Calculates the min, max, and average blob count across all grid squares.
        # Parameters: None
        # Returns: tuple (min_count, max_count, avg_count)
        # List of blob count for every square
        counts = [len(self.grid[r][c]) for r in range(self.n) for c in range(self.n)]

        low = min(counts)
        high = max(counts)
        avg = sum(counts) / len(counts)

        return (low, high, avg)  # Returns as a tuple

# ====================================================================================================================

def user_prompt():
    # Prompts user for N and MaxT, validates both.
    # Parameters: None
    # Returns: tuple (N, MaxT) as integers
    print("You will enter two integers to configure the simulation:")
    print("the grid size dimension (N) and the number of paint blobs (MaxT).")
    print("-" * 65)

    N = input("Enter the grid size dimension for the simulation. It must be an integer between 2 and 100, inclusive: ")
    N = valid_entry(N, 2, 100)

    T = input("Enter MaxT (number of blobs). It must be an integer between 4 and 1,000,000, inclusive: ")
    T = valid_entry(T, 4, 1000000)

    return int(N), int(T)

def valid_entry(X, lower_range, upper_range):
    # Validates that X is a whole number within [lower_range, upper_range].
    # Re-prompts until valid input is given.
    # Parameters:
    #   X           - initial input value to validate
    #   lower_range - minimum acceptable value
    #   upper_range - maximum acceptable value
    # Returns: validated number as a float (whole number)
    check = False
    while not check:
        try:
            X = float(X)
            if not X.is_integer():
                X = input("   Input is not a valid integer, please enter a valid integer: ")
                continue
        except ValueError:
            print("   Input is not a number, please input a valid number.")
            X = input()
            continue

        if int(X) < lower_range or int(X) > upper_range:
            print(f"   ERROR: number must be between {lower_range} and {upper_range}. Please re-enter.")
            X = input()
        else:
            check = True
    return X


def increment_N(start_n, maxt, step):
    # Runs 10 simulations, incrementing N by step each time while holding MaxT constant.
    # Parameters:
    #   start_n - starting grid size
    #   maxt    - constant MaxT for all simulations
    #   step    - amount to increment N each simulation
    # Returns: list of (n, (min, max, avg)) tuples
    results = [] # Data for graphing later
    current_n = start_n

    print(f"\n--- Running 10 Simulations: Incrementing N by {step} ---")
    for i in range(1, 11):
        sim = Canvas(current_n, maxt)
        sim.generate()

        # Stores the sim's N value and corresponding low, high, and avg
        results.append((current_n, sim.get_stats()))

        print(f"    Simulation {i}/10: N = {current_n}")
        current_n += step

    return results


def increment_maxt(n, start_maxt, step):
    # Runs 10 simulations, incrementing MaxT by step each time while holding N constant.
    # Parameters:
    #   n          - constant grid size for all simulations
    #   start_maxt - starting MaxT value
    #   step       - amount to increment MaxT each simulation
    # Returns: list of (maxt, (min, max, avg)) tuples
    results = [] # Data for graphing later
    current_maxt = start_maxt

    print(f"\n--- Running 10 Simulations: Incrementing MaxT by {step} ---")
    for i in range(1, 11):
        sim = Canvas(n, current_maxt)
        sim.generate()

        # Stores the sim's maxT value and corresponding low, high, and avg
        results.append((current_maxt, sim.get_stats()))

        print(f"    Simulation {i}/10: MaxT = {current_maxt}")
        current_maxt += step

    return results

def choose_mode():
    # Prompts the user to choose between holding N or MaxT constant.
    # Parameters: None
    # Returns: 1 (hold MaxT, vary N) or 2 (hold N, vary MaxT)
    print("\n" + "=" * 65)
    print("MULTI-SIMULATION COMPARISON")
    print("=" * 65)
    print("Choose one of the following options:")
    print("  1. Hold MaxT constant and change N")
    print("  2. Hold N constant and change MaxT")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("   ERROR: Please enter either 1 or 2.")


def get_increment(label):
    # Prompts user for an increment value that must be 1, 10, 100, or 1000.
    # Parameters:
    #   label - string describing what is being incremented (e.g. 'Nincrement')
    # Returns: validated increment as an int
    valid = {1, 10, 100, 1000}
    while True:
        raw = input(f"Enter {label} (must be 1, 10, 100, or 1000): ").strip()
        try:
            val = int(float(raw))
            if val in valid:
                return val
            print(f"   ERROR: {label} must be exactly 1, 10, 100, or 1000.")
        except ValueError:
            print("   ERROR: Please enter a valid integer.")


def graph_N_results(results, maxt):
    # Displays a line graph of min/max/avg blob counts vs grid size N.
    # Parameters:
    #   results - list of (n, (min, max, avg)) tuples from increment_N()
    #   maxt    - the constant MaxT value used across all simulations
    # Returns: None
    ns    = [r[0] for r in results]
    lows  = [r[1][0] for r in results]
    highs = [r[1][1] for r in results]
    avgs  = [r[1][2] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(ns, lows,  'v--', color='blue',  label='Lowest Blobs',  markersize=8)
    plt.plot(ns, avgs,  's-',  color='green', label='Average Blobs', markersize=8)
    plt.plot(ns, highs, '^--', color='red',   label='Highest Blobs', markersize=8)

    plt.xlabel("Grid Size (N)", fontsize=12)
    plt.ylabel("Number of Blobs on a Square", fontsize=12)
    plt.title(f"Blob Distribution vs Grid Size\n(MaxT = {maxt}, 10 simulations)", fontsize=13)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graph_T_results(results, n):
    # Displays a line graph of min/max/avg blob counts vs MaxT.
    # Parameters:
    #   results - list of (maxt, (min, max, avg)) tuples from increment_maxt()
    #   n       - the constant grid size used across all simulations
    # Returns: None
    ts    = [r[0] for r in results]
    lows  = [r[1][0] for r in results]
    highs = [r[1][1] for r in results]
    avgs  = [r[1][2] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(ts, lows,  'v--', color='blue',  label='Lowest Blobs',  markersize=8)
    plt.plot(ts, avgs,  's-',  color='green', label='Average Blobs', markersize=8)
    plt.plot(ts, highs, '^--', color='red',   label='Highest Blobs', markersize=8)

    plt.xlabel("Total Paint Blobs (MaxT)", fontsize=12)
    plt.ylabel("Number of Blobs on a Square", fontsize=12)
    plt.title(f"Blob Distribution vs Total Blobs Dropped\n(Grid Size = {n}x{n}, 10 simulations)", fontsize=13)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def run_multi_simulation(prev_n, prev_maxt):
    # Runs the multi-simulation comparison: prompts for mode, gathers inputs,
    # runs 10 simulations, and displays a graph.
    # Parameters:
    #   prev_n    - N value from the previous simulation
    #   prev_maxt - MaxT value from the previous simulation
    # Returns: None
    mode = choose_mode()

    if mode == 1:
        # Hold MaxT constant, vary N
        print("\n--- Option 1: Hold MaxT Constant, Change N ---")
        raw_n = input("Enter starting N (integer, 2 to 100): ")
        start_n = int(valid_entry(raw_n, 2, 100))

        n_increment = get_increment("Nincrement")

        raw_t = input("Enter MaxT to hold constant (integer, 4 to 1,000,000): ")
        maxt = int(valid_entry(raw_t, 4, 1000000))

        results = increment_N(start_n, maxt, n_increment)
        graph_N_results(results, maxt)

    else:
        # Hold N constant, vary MaxT
        print("\n--- Option 2: Hold N Constant, Change MaxT ---")
        raw_t = input("Enter starting MaxT (integer, 4 to 1,000,000): ")
        start_maxt = int(valid_entry(raw_t, 4, 1000000))

        t_increment = get_increment("Tincrement")

        raw_n = input("Enter N to hold constant (integer, 2 to 100): ")
        n = int(valid_entry(raw_n, 2, 100))

        results = increment_maxt(n, start_maxt, t_increment)
        graph_T_results(results, n)

    input("\nAll simulations complete. Press ENTER to finish the program.")


def main():
    # Entry point. Runs the intro simulation, a user-configured simulation,
    # and the multi-simulation comparison.
    # Uses globals: INTRO_N, INTRO_MAXT
    # Parameters: None
    # Returns: None
    displayStartupInfo()

    # Initialize 10x10 canvas and set MaxT=300 for the intro simulation
    intro_canvas = Canvas(INTRO_N, INTRO_MAXT)
    intro_canvas.generate()
    intro_canvas.animate()

    # New canvas from user prompted values
    N, maxT = user_prompt()

    canvas = Canvas(N, maxT)
    canvas.generate()
    canvas.animate()

    #Multi-simulation comparison (replaces the hardcoded increment_N test)
    run_multi_simulation(N, maxT)


if __name__ == "__main__":
    main()