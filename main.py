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
    cprint("3. Determine Area of Lightning Bolt Image", "green", "on_black")
    cprint("4. Determine Area of Dart Board Image", "green", "on_black")
    cprint("5. Probability of Scoring 10 or More on Dart Board", "green", "on_black")
    cprint("6. Determine Area of Each Color in an Image", "green", "on_black")
    cprint("7. Time Until Outcome When Sampling Colors in an Image", "green", "on_black")
    cprint("8. Average Time Until Outcome When Sampling Colors in an Image", "green", "on_black")
    cprint("Type 'quit' anytime to exit the program.", "red", "on_black")
    menu_num = quit(input(colored("Enter your choice: ", "blue", "on_black"))) # Get the user's choice
    while not menu_num.isnumeric() or int(menu_num) < 1 or int(menu_num) > 8:
        cprint("Please enter a valid choice.", "red", "on_black")
        menu_num = quit(input(colored("Enter your choice: ", "blue", "on_black"))) # Get the user's choice
    menu_num = int(menu_num)

def make_function(expr): # Create a vectorized function from a string expression
    def _f(x):
        local = {"x": x}
        return eval(expr, {"__builtins__": None, "math": math, "np": np}, local) # use math and numpy functions only
    return np.vectorize(_f)

def separate_coordinates(coordinate_list): # Separate x and y coordinates from a list of (x, y) tuples
    x_vals = []
    y_vals = []

    for coordinate in coordinate_list: # Iterate through each coordinate tuple
        x_vals.append(coordinate[0])
        y_vals.append(coordinate[1])

    return x_vals,y_vals # Return separate x and y lists

def plot_function(f_vec, x_min, x_max, y_min, y_max, under_coords, over_coords, two_lines, title): # Plot the function and sampled points
    xs = np.linspace(x_min, x_max, 500) # Generate x values
    ys = f_vec(xs) # Generate y values

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, color="black", label="y = f(x)") # Plot the function

    if two_lines: # If there is a second function to plot
        ys2 = two_lines(xs)
        plt.plot(xs, ys2, color="blue", label="y = f2(x)")

    if over_coords: # If there are points above the curve
        over_x, over_y = separate_coordinates(over_coords) # Separate x and y coordinates
        plt.scatter(over_x, over_y, color="red", s=1, label="Above curve") # Plot points above the curve red
    if under_coords: # If there are points below the curve
        under_x, under_y = separate_coordinates(under_coords) # Separate x and y coordinates
        plt.scatter(under_x, under_y, color="blue", s=1, label="Under curve") # Plot points below the curve blue

    plt.xlim(x_min, x_max) # Set x limits
    plt.ylim(y_min, y_max) # Set y limits
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show() # Show the plot

def integration_single(): # Single function integration using Monte Carlo
    expr = input(colored("Enter f(x) (default x**2): ", "blue", "on_black")) or "x**2" # Get the function expression from the user, default is graded criteria function (default by pressing enter without typing anything)
    f_vec = make_function(expr) # Create a vectorized function
    x_min = float(input(colored("x_min (default 0): ", "blue", "on_black")) or 0) # Get the x, y min and max from the user, default is within graded criteria
    x_max = float(input(colored("x_max (default 3): ", "blue", "on_black")) or 3)
    y_min = float(input(colored("y_min (default 0): ", "blue", "on_black")) or 0)
    y_max = float(input(colored("y_max (default 9): ", "blue", "on_black")) or 9)
    amount_samples = int(input(colored("Number of random samples (default 10000): ", "blue", "on_black")) or 10000) # Get the number of random samples from the user, default is 10000
    xs = np.random.uniform(x_min, x_max, amount_samples) # Generate random x samples
    ys = np.random.uniform(y_min, y_max, amount_samples) # Generate random y samples
    f_vals = f_vec(xs) # Evaluate the function at the random x samples
    count_under = np.sum(ys <= f_vals) # Count how many random points are under the curve
    area_box = (x_max - x_min) * (y_max - y_min) # Calculate the area of the bounding box
    estimate = (count_under / amount_samples) * area_box # Calculate the Monte Carlo estimate
    cprint(f"Monte Carlo Estimate: {estimate:.5f}", "green", "on_black")
    plot_function(f_vec, x_min, x_max, y_min, y_max, # Plot parameters
                  under_coords=[(x, y) for x, y, f_val in zip(xs, ys, f_vals) if y <= f_val], # For both x and y coordinates, check if the y coordinate is under the function value at that x coordinate, then plot if true
                  over_coords=[(x, y) for x, y, f_val in zip(xs, ys, f_vals) if y > f_val], # For both x and y coordinates, check if the y coordinate is over the function value at that x coordinate, then plot if true
                  two_lines=None, # No second function to plot
                  title="Monte Carlo Estimate of Area Under Curve") # Title

def integration_double(): # Double function integration using Monte Carlo
    expr1 = input(colored("Enter f1(x) (default 1/2*x+1): ", "blue", "on_black")) or "1/2*x+1" # Get the function expressions from the user, default is within graded criteria (default by pressing enter without typing anything)
    expr2 = input(colored("Enter f2(x) (default (x-2)**2+0.5): ", "blue", "on_black")) or "(x-2)**2+0.5" # Get the second function expression
    f1_vec = make_function(expr1) # Create vectorized functions
    f2_vec = make_function(expr2)
    x_min = float(input(colored("x_min (default 0): ", "blue", "on_black")) or 0) # Get the x, y min and max from the user, default is within graded criteria
    x_max = float(input(colored("x_max (default 4): ", "blue", "on_black")) or 4)
    y_min = float(input(colored("y_min (default 0): ", "blue", "on_black")) or 0)
    y_max = float(input(colored("y_max (default 4): ", "blue", "on_black")) or 4)
    amount_samples = int(input(colored("Number of random samples (default 10000): ", "blue", "on_black")) or 10000)
    xs = np.random.uniform(x_min, x_max, amount_samples) # Generate random x samples
    ys = np.random.uniform(y_min, y_max, amount_samples) # Generate random y samples
    f1_vals = f1_vec(xs) # Evaluate both functions at the random x samples
    f2_vals = f2_vec(xs)
    count_under = np.sum((ys <= f1_vals) & (ys >= f2_vals)) # Count how many random points are between the two curves
    area_box = (x_max - x_min) * (y_max - y_min) # Calculate the area of the bounding box
    estimate = (count_under / amount_samples) * area_box # Calculate the Monte Carlo estimate
    cprint(f"Monte Carlo Estimate: {estimate:.5f}", "green", "on_black") 
    plot_function(f1_vec, x_min, x_max, y_min, y_max, # Plot parameters
                  under_coords=[(x, y) for x, y, f1_val, f2_val in zip(xs, ys, f1_vals, f2_vals) if y <= f1_val and y >= f2_val], # For both x and y coordinates, check if the y coordinate is under the first function value and above the second function value at that x coordinate, then plot if true
                  over_coords=[(x, y) for x, y, f1_val, f2_val in zip(xs, ys, f1_vals, f2_vals) if not (y <= f1_val and y >= f2_val)], # For both x and y coordinates, check if the y coordinate is not under the first function value and above the second function value at that x coordinate, then plot if true
                  two_lines=f2_vec, # Second function to plot
                  title="Monte Carlo Estimate of Area Between Two Curves") # Title

def replace_sampled_pixels(img, pixels_used): # Replace sampled pixels in the image with red for visualization
    draw = ImageDraw.Draw(img)
    for (x, y) in pixels_used:
        draw.point((x, y), fill=(255, 0, 0))  # Replace sampled pixels with red
    img.show()

def image_pixel_sampling_by_color(path): # Sample pixels from an image and count colors
    num_samples = 5000 # Number of pixels to sample
    img = Image.open(path) # Open the image
    img = img.convert("RGB") # Ensure image is in RGB mode
    pixels = img.load() # Load pixel data
    width, height = img.size # Get image dimensions
    color_counts = {} # Dictionary to store amount of each color
    pixels_used = [] # List to store sampled pixel coordinates (for visualization, and to make sure when double counting a pixel it doesnt count it as red due to replacing it before before all samples are done)
    for i in range(num_samples): # Sample pixels
        rand_x = random.randint(0, width - 1)
        rand_y = random.randint(0, height - 1)
        color = pixels[rand_x, rand_y] # color is an (R, G, B) tuple
        color_counts[color] = color_counts.get(color, 0) + 1 # Increment the count for this color, if there is no count yet, set it to 0 first and add 1
        pixels_used.append((rand_x, rand_y)) # Store sampled pixel coordinates
    replace_sampled_pixels(img, pixels_used) # Visualize sampled pixels
    return color_counts # Return the colors and amounts for the colors

def image_pixel_sampling_coordinates(path): # Sample pixel coordinates from an image
    num_samples = 5000 # Number of pixels to sample
    img = Image.open(path) # Open the image
    width, height = img.size # Get image dimensions
    pixels_used = [] # List to store sampled pixel coordinates
    for i in range(num_samples): # Sample pixels
        rand_x = random.randint(0, width - 1) 
        rand_y = random.randint(0, height - 1)
        pixels_used.append((rand_x, rand_y)) # Store sampled pixel coordinates
    replace_sampled_pixels(img, pixels_used) # Visualize sampled pixels
    return pixels_used # Return the sampled pixel coordinates

def determine_area(image_color_data, target_color, total_pixels, whitelist_colors): # Determine area percentage of target color in sampled image data
    if whitelist_colors: # If only counting target color
        target_pixels = image_color_data.get(target_color, 0) # Get the count of target color pixels, default to 0 if not found
        area_percentage = (target_pixels / total_pixels) * 100 # Calculate area percentage
    elif not whitelist_colors: # If counting all colors except target color
        target_pixels = sum(count for color, count in image_color_data.items() if color != target_color) # Sum counts of all colors except target color
        area_percentage = (target_pixels / total_pixels) * 100 # Calculate area percentage
    return area_percentage # Return the area percentage

def within_circle(x, y, center_x, center_y, radius): # Check if a point is within a circle
    within = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2 # Calculate if the point is within the circle using the circle equation using squared distances
    return within # Return the result

def time_until_outcome(image_path, target_color): # Time until a specific color pixel is found in an image
    img = Image.open(image_path).convert('RGB') # Open and convert the image to RGB
    w, h = img.size
    pix = img.load() # Load pixel data
    results = [] # List to store time counts
    for i in range(20000): # Perform 20000 trials
        count = 0
        while True:
            count += 1
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            if pix[x, y] == target_color:
                results.append(count)
                break
    with open("time_until_outcome_results.txt", "w") as f: # Save results to a text file
        for result in results:
            f.write(f"{result}\n")
    return results

welcome() # Display welcome message
menu() # Display menu
while True: # Main program loop
    if menu_num == 1: # Execute the selected option
        integration_single() 
    elif menu_num == 2:
        integration_double()
    elif menu_num == 3:
        bolt_percentage = determine_area(image_pixel_sampling_by_color("Student Resources/2.0 Lightning Bolt/bolt.png"), (255, 255, 54), 5000, True) # Calculate area percentage of lightning bolt color using whitelist
        cprint(f"Estimated area of lightning bolt: {bolt_percentage:.2f}%", "green", "on_black") # Display the result
    elif menu_num == 4:
        target_percentage = determine_area(image_pixel_sampling_by_color("Student Resources/3.0 Dart Board/3.1.png"), (255, 255, 255), 5000, False) # Calculate area percentage of non-background color using blacklist
        cprint(f"Estimated area of dart board (non-background): {target_percentage:.2f}%", "green", "on_black")
    elif menu_num == 5:
        target_image = Image.open("Student Resources/3.0 Dart Board/3.1.png") # Open the dart board image
        r3 = target_image.size[0] / 2 / 5 * 3 # Calculate radius for scoring 10 or more (3/5 of the dart board radius), each ring's thickness is 1/5 of the radius
        center_x, center_y = target_image.size[0] / 2, target_image.size[1] / 2 # Calculate center of the dart board
        within_r3 = sum(1 for x, y in image_pixel_sampling_coordinates("Student Resources/3.0 Dart Board/3.1.png") if within_circle(x, y, center_x, center_y, r3)) # Count how many sampled pixels are within the radius for scoring 10 or more
        cprint(f"Estimated probability of scoring 10 or more: {(within_r3 / 5000) * 100:.2f}%", "green", "on_black") # Display the result
    elif menu_num == 6:
        target_colors = [(59, 163, 234), (247, 188, 43), (138, 219, 138), (238, 193, 165), (237, 49, 25), (0, 0, 0)] # Define target colors to analyze
        target_colors_words = ["Blue", "Gold", "Green", "Peach", "Red", "Black (Text)"] # Corresponding color names
        img = Image.open("Student Resources/3.0 Dart Board/3.3.png")
        determine_area_each_color_counts = image_pixel_sampling_by_color("Student Resources/3.0 Dart Board/3.3.png") # Sample the image and get color counts
        total_sampled_pixels = sum(determine_area_each_color_counts.values()) # Calculate total sampled pixels
        total_pixels = img.width * img.height # Calculate total pixels in the image
        for color, color_word in zip(target_colors, target_colors_words): # Loop through each target color and its name
            area_percentage = determine_area(determine_area_each_color_counts, color, total_sampled_pixels, True) # Calculate area percentage for the target color using whitelist
            cprint(f"Estimated area of color {color_word}: {area_percentage:.2f}%, or {area_percentage / 100 * total_pixels:.2f} pixels", "green", "on_black") # Display the result
        cprint("Estimated area of background (not counted colors): {:.2f}%".format(100 - sum(determine_area(determine_area_each_color_counts, color, total_sampled_pixels, True) for color in target_colors)) + " or {:.2f} pixels".format((100 - sum(determine_area(determine_area_each_color_counts, color, total_sampled_pixels, True) for color in target_colors)) / 100 * total_pixels), "green", "on_black")
    elif menu_num == 7:
        time_count = time_until_outcome("Student Resources/4.0 Distributions/0.5_2.png", (255, 0, 0)) # Get time until outcome data
        max_trial = max(time_count)
        # bins from 0.5 to max_trial+0.5 to centre integer bins
        bins = [i - 0.5 for i in range(1, max_trial + 2)]
        plt.figure(figsize=(8, 6))
        counts, edges, patches = plt.hist(time_count, bins=bins, color='blue', edgecolor='black')
        xticks = list(range(1, max_trial + 1))
        plt.xticks(xticks)
        for count, left_edge, patch in zip(counts, edges[:-1], patches):
            center = left_edge + 0.5
            plt.text(center, count + max(counts) * 0.01, f'{int(count)}', ha='center', va='bottom', fontsize=8)
        plt.xlabel('Number of Trials Needed to Find (255, 0, 0)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Trials Needed')
        plt.grid(axis='y', alpha=0.75)
        plt.show()
    elif menu_num == 8:
        time_count = time_until_outcome("Student Resources/4.0 Distributions/0.5_2.png", (255, 0, 0)) # Get time until outcome data
        averages = []
        for i in range(0, len(time_count), 20): # Calculate averages of groups of 20 time counts for normal distribution
            group = time_count[i:i+20] # Get the current group of 20
            if len(group) == 0:
                continue
            group_average = sum(group) / len(group) # Calculate the average of the group
            averages.append(group_average) # Store the average
        # Use bins of width 0.1 so bars represent one decimal place increments
        # Plotting histogram
        min_avg = min(averages)
        max_avg = max(averages)
        # Create bin edges spaced by 0.1 and center bars on one-decimal values
        bins = np.arange(math.floor(min_avg*10)/10 - 0.05, math.ceil(max_avg*10)/10 + 0.15, 0.1)
        plt.hist(averages, bins=bins, edgecolor='black')
        # set x-ticks at one-decimal increments
        xticks = np.round(np.arange(math.floor(min_avg*10)/10, math.ceil(max_avg*10)/10 + 0.1, 0.1), 1)
        plt.xticks(xticks)
        plt.title("Distribution of Averages (Groups of 20)")
        plt.xlabel("Average Value")
        plt.ylabel("Frequency")
        plt.grid(axis='y', alpha=0.75)
        plt.show()
    menu() # Display menu again after completing the selected option
