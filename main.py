# import libraries
import math
import numpy as np
import matplotlib.pyplot as plt
from termcolor import *
import time
import sys
import random
from PIL import Image, ImageDraw

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
    cprint("3. Sampling Pixels in an Image", "green", "on_black")
    cprint("4. Determine Area of Lightning Bolt Image", "green", "on_black")
    cprint("5. Determine Area of Dart Board Image", "green", "on_black")
    cprint("6. Probability of Scoring 10 or More on Dart Board", "green", "on_black")
    cprint("Type 'quit' anytime to exit the program.", "red", "on_black")
    menu_num = quit(input(colored("Enter your choice: ", "blue", "on_black"))) # Get the user's choice
    while not menu_num.isnumeric() or int(menu_num) < 1 or int(menu_num) > 6:
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

def plot_function(f_vec, x_min, x_max, y_min, y_max, under_coords, over_coords, two_lines, title="Monte Carlo Estimate of Area Under Curve"):
    xs = np.linspace(x_min, x_max, 500)
    ys = f_vec(xs)

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, color="black", label="y = f(x)")
    if two_lines:
        ys2 = two_lines(xs)
        plt.plot(xs, ys2, color="green", label="y = g(x)")

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
                  over_coords=[(x, y) for x, y, f_val in zip(xs, ys, f_vals) if y > f_val],
                  two_lines=None,
                  title="Monte Carlo Estimate of Area Under Curve")

def integration_double():
    expr1 = input(colored("Enter f1(x) (e.g. '10' or 'x**2'): ", "blue", "on_black"))
    expr2 = input(colored("Enter f2(x) (e.g. '5' or 'x'): ", "blue", "on_black"))
    f1_vec = make_function(expr1)
    f2_vec = make_function(expr2)
    x_min = float(input(colored("x_min (default 0): ", "blue", "on_black")) or 0)
    x_max = float(input(colored("x_max (default 20): ", "blue", "on_black")) or 20)
    y_min = float(input(colored("y_min (default 0): ", "blue", "on_black")) or 0)
    y_max = float(input(colored("y_max (default 20): ", "blue", "on_black")) or 20)
    amount_samples = int(input(colored("Number of random samples (default 10000): ", "blue", "on_black")) or 10000)
    xs = np.random.uniform(x_min, x_max, amount_samples)
    ys = np.random.uniform(y_min, y_max, amount_samples)
    f1_vals = f1_vec(xs)
    f2_vals = f2_vec(xs)
    count_under = np.sum((ys <= f1_vals) & (ys >= f2_vals))
    area_box = (x_max - x_min) * (y_max - y_min)
    estimate = (count_under / amount_samples) * area_box
    cprint(f"Monte Carlo Estimate: {estimate:.5f}", "green", "on_black")
    plot_function(f1_vec, x_min, x_max, y_min, y_max,
                  under_coords=[(x, y) for x, y, f1_val, f2_val in zip(xs, ys, f1_vals, f2_vals) if y <= f1_val and y >= f2_val],
                  over_coords=[(x, y) for x, y, f1_val, f2_val in zip(xs, ys, f1_vals, f2_vals) if not (y <= f1_val and y >= f2_val)],
                  two_lines=f2_vec,
                  title="Monte Carlo Estimate of Area Between Two Curves")

def image_pixel_sampling_by_color(path, replace_color):
    num_samples = 5000
    img = Image.open(path)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size
    color_counts = {}
    pixels_used = []
    for i in range(num_samples):
        rand_x = random.randint(0, width - 1)
        rand_y = random.randint(0, height - 1)
        color = pixels[rand_x, rand_y]
        # color is an (R, G, B) tuple
        color_counts[color] = color_counts.get(color, 0) + 1
        pixels_used.append((rand_x, rand_y))
    if replace_color:
        draw = ImageDraw.Draw(img)
        for (x, y) in pixels_used:
            draw.point((x, y), fill=(255, 0, 0))  # Replace sampled pixels with red
        img.show()
    return color_counts

def image_pixel_sampling_coordinates(path, replace_color):
    num_samples = 5000
    img = Image.open(path)
    width, height = img.size
    pixels_used = []
    for i in range(num_samples):
        rand_x = random.randint(0, width - 1)
        rand_y = random.randint(0, height - 1)
        pixels_used.append((rand_x, rand_y))
    if replace_color:
        draw = ImageDraw.Draw(img)
        for (x, y) in pixels_used:
            draw.point((x, y), fill=(255, 0, 0))  # Replace sampled pixels with red
        img.show()
    return pixels_used

def plot_color_distribution(color_counts, top_n=12): # For debugging
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    top = sorted_colors[:top_n]
    labels = ["#%02x%02x%02x" % c for c, _ in top]
    counts = [cnt for _, cnt in top]
    bar_colors = [(c[0] / 255, c[1] / 255, c[2] / 255) for c, _ in top]

    plt.figure(figsize=(max(8, len(labels) * 0.4), 5))
    x = np.arange(len(labels))
    plt.bar(x, counts, color=bar_colors, edgecolor='black', linewidth=0.8)
    plt.xticks(x, labels, rotation=90)
    plt.title(f"Top {len(labels)} sampled colors")
    plt.ylabel("Sample count")
    plt.tight_layout()
    plt.show()

def determine_area(image, target_color, total_pixels, whitelist_colors):
    if whitelist_colors:
        target_pixels = image.get(target_color, 0)
        area_percentage = (target_pixels / total_pixels) * 100
    else:
        target_pixels = sum(count for color, count in image.items() if color != target_color)
        area_percentage = (target_pixels / total_pixels) * 100

    return area_percentage

def within_circle(x, y, center_x, center_y, radius):
    within = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
    return within

welcome()
menu()
while True:
    if menu_num == 1:
        integration_single()
    elif menu_num == 2:
        integration_double()
    elif menu_num == 3:
        path = input(colored(f"Enter the image file path: ", "blue", "on_black"))
        color_distribution = image_pixel_sampling_by_color(path, True)
        plot_color_distribution(color_distribution)
        for color, count in sorted(color_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"Color {color}: {count} samples")
    elif menu_num == 4:
        bolt_percentage = determine_area(image_pixel_sampling_by_color("Student Resources/2.0 Lightning Bolt/bolt.png", True), (255, 255, 54), 5000, True)
        cprint(f"Estimated area of lightning bolt: {bolt_percentage:.2f}%", "green", "on_black")
    elif menu_num == 5:
        target_percentage = determine_area(image_pixel_sampling_by_color("Student Resources/3.0 Dart Board/3.1.png", True), (255, 255, 255), 5000, False)
        cprint(f"Estimated area of dart board (non-background): {target_percentage:.2f}%", "green", "on_black")
    elif menu_num == 6:
        # blue = 59 163 234 or # 3BA3EA
        # red = 237 49 25 or # ED3119
        # orange = 247 188 43 or # F7BC2B
        target_image = Image.open("Student Resources/3.0 Dart Board/3.1.png")
        r3 = target_image.size[0] / 2 / 5 * 3
        center_x, center_y = target_image.size[0] / 2, target_image.size[1] / 2
        within_r3 = sum(1 for x, y in image_pixel_sampling_coordinates("Student Resources/3.0 Dart Board/3.1.png", True) if within_circle(x, y, center_x, center_y, r3))
        cprint(f"Estimated probability of scoring 10 or more: {(within_r3 / 5000) * 100:.2f}%", "green", "on_black")

    menu()
