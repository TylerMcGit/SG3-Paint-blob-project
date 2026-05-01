"""
Authors:
Caleb Hackmann
Jory Ehman
...

CS 4500 - SG3: Paint Blobs
Date of Submission: 05/06/2026
Developed in PyCharm, and tested on Thonny.

Purpose:
Data Structures:
Packages:
Outside Resources:
Revision Information:
"""

import os
import random
import matplotlib.pyplot as plt
from datetime import datetime

INTRO_N    = 10   # grid dimension for the intro simulation
INTRO_MAXT = 300  # number of blobs for the intro simulation


def displayStartupInfo():
    # Prints SG3 project explanation to the screen.
    print("""
        SG3: Paint Blobs
        Project Authors: Caleb Hackmann, Jory Ehman,
 
Summary:
    This program simulates random paint blobs dropping onto a
    square canvas. Each drop lands on a random square and gets
    a random color (red, green, blue). Only the latest blob on
    each square is visible.
 
    Stats are printed when all squares are first painted, and
    again after MaxT total drops.
""")


def make_canvas(n):
    # Returns an N x N 2D list of empty lists (all squares start blank).
    return [[[] for _ in range(n)] for _ in range(n)]


def valid_entry(X, lower_range, upper_range):
    # Validates that X is a whole number integer within [lower_range, upper_range].
    # Re-prompts until valid. Returns the validated integer.
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


def user_interaction():
    # Prompts user for N and MaxT, validates both, and returns them as ints.
    print("You will enter two integers to configure the simulation:")
    print("the grid size dimension (N) and the number of paint blobs (MaxT).")
    print("-" * 65)

    N = input("Enter the grid size dimension for the simulation. It must be an integer between 2 and 100, inclusive: ")
    N = valid_entry(N, 2, 100)

    T = input("Enter MaxT (number of blobs). It must be an integer between 4 and 1,000,000, inclusive: ")
    T = valid_entry(T, 4, 1000000)

    return int(N), int(T)


def main():
    displayStartupInfo()

    # Initialize 10x10 canvas and set MaxT=300 for the intro simulation
    canvas = make_canvas(INTRO_N)
    maxt   = INTRO_MAXT

    # Unique randomness is guaranteed by Python's random module seeding from system time
    # run_intro_simulation(canvas, maxt) -- teammate's Step 2 plugs in here

    N, MaxT = user_interaction()

    # Second simulation runs here -- teammate's steps plug in below


if __name__ == "__main__":
    main()