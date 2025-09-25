# import libraries
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from termcolor import *
import time
import sys

# Initialize variables
menu_num = None

def welcome(): # Welcome message
    cprint(f" _    _        _", "white", "on_black")
    time.sleep(0.1)
    cprint(f"| |  | |      | |", "white", "on_black")
    time.sleep(0.1)
    cprint(f"| |  | |  ___ | |  ___   ___   _ __ ___    ___", "white", "on_black")
    time.sleep(0.1)
    cprint(f"| |/\| | / _ \| | / __| / _ \ | '_ ` _ \  / _ \'", "white", "on_black")
    time.sleep(0.1)
    cprint(f"\  /\  /|  __/| || (__ | (_) || | | | | ||  __/", "white", "on_black")
    time.sleep(0.1)
    cprint(f" \/  \/  \___||_| \___| \___/ |_| |_| |_| \___|", "white", "on_black")
    time.sleep(0.25)
    cprint("Year 9 Mathematics Investigation 2 - Sampling and Distributions", "green", "on_black")
    time.sleep(0.25)
    cprint("By Henry Sun", "green", "on_black")
    time.sleep(0.25)
    cprint("If you decide to quit the program at any point, type quit!", "green", "on_black")
    time.sleep(0.25)
    cprint("If you want to view the menu again, type menu!", "green", "on_black")

def quit(text): # Quit function
    if text.lower() == "quit" or text.lower() == "exit": # If the user types quit or exit, the program will terminate
        cprint("NOOOOoOOOoooooooo why do u want to terminate me??????😟😭😭", "green", "on_black")
        time.sleep(0.5)
        cprint("I just want to be helpful!!!!", "green", "on_black")
        time.sleep(0.5)
        cprint("But you decide to---", "green", "on_black")
        time.sleep(0.5)
        cprint("You have terminated the program.", "red", "on_black")
        sys.exit() # Terminate the program
    else:
        return text # If the user does not type quit, the program will continue

def menu(): # Menu system
    global menu_num
    print()
    cprint("Please select an option:", "green", "on_black")
    cprint("1. Approximating Integration using Monte Carlo Estimate", "green", "on_black")
    cprint("2. Approximating Integration between two functions using Monte Carlo Estimate", "green", "on_black")
    menu_num = quit(input(colored("Enter your choice: ", "blue", "on_black"))) # Get the user's choice
    while not menu_num.isnumeric() or int(menu_num) < 1 or int(menu_num) > 2:
        cprint("Please enter a valid choice.", "red", "on_black")
        menu_num = quit(input(colored("Enter your choice: ", "blue", "on_black"))) # Get the user's choice
    menu_num = int(menu_num)

def make_function(expr):
    def _f(x):
        local = {"x": x}
        return eval(expr, {"__builtins__": None, "math": math, "np": np}, local)
    return np.vectorize(_f)

def separate_coordinates(coordinate_list):
    x_vals = []
    y_vals = []

    for coordinate in coordinate_list:
        x_vals.append(coordinate[0])
        y_vals.append(coordinate[1])

    return x_vals,y_vals

def plot_function(f_vec, x_min, x_max, y_min, y_max, under_coords, over_coords, title="Monte Carlo Estimate of Area Under Curve"):
    xs = np.linspace(x_min, x_max, 500)
    ys = f_vec(xs)

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, color="black", label="y = f(x)")

    if over_coords:
        over_x, over_y = separate_coordinates(over_coords)
        plt.scatter(over_x, over_y, color="red", s=1, label="Above curve")
    if under_coords:
        under_x, under_y = separate_coordinates(under_coords)
        plt.scatter(under_x, under_y, color="blue", s=1, label="Under curve")

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

def integration_single():
    expr = input(colored("Enter f(x) (e.g. '10' or 'x**2'): ", "blue", "on_black"))
    f_vec = make_function(expr)
    x_min = float(input(colored("x_min (default 0): ", "blue", "on_black")) or 0)
    x_max = float(input(colored("x_max (default 20): ", "blue", "on_black")) or 20)
    y_min = float(input(colored("y_min (default 0): ", "blue", "on_black")) or 0)
    y_max = float(input(colored("y_max (default 20): ", "blue", "on_black")) or 20)
    amount_samples = int(input(colored("Number of random samples (default 10000): ", "blue", "on_black")) or 10000)
    xs = np.random.uniform(x_min, x_max, amount_samples)
    ys = np.random.uniform(y_min, y_max, amount_samples)
    f_vals = f_vec(xs)
    count_under = np.sum(ys <= f_vals)
    area_box = (x_max - x_min) * (y_max - y_min)
    estimate = (count_under / amount_samples) * area_box
    cprint(f"Monte Carlo Estimate: {estimate:.5f}", "green", "on_black")
    plot_function(f_vec, x_min, x_max, y_min, y_max,
                  under_coords=[(x, y) for x, y, f_val in zip(xs, ys, f_vals) if y <= f_val],
                  over_coords=[(x, y) for x, y, f_val in zip(xs, ys, f_vals) if y > f_val])

def integration_double():
    pass

# Main loop
welcome()

menu()
while True:
    if menu_num == 1:
        integration_single()
    elif menu_num == 2:
        integration_double()
    menu()