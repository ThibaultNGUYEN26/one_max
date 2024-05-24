import random
import time
from tkinter import Tk, Frame, StringVar, Label, Canvas, Entry, Button, messagebox

# Parameters
population_size = 50
mutation_rate = 0.05  # Increased mutation rate to introduce more variability
generations = 50
colors = ["red", "blue", "yellow", "green", "black", "white"]
color_to_number = {"red": 0, "blue": 1, "yellow": 2, "green": 3, "black": 4, "white": 5}
number_to_color = {v: k for k, v in color_to_number.items()}

# Initialize population with random values between 0 and 5
def initialize_population(size, length):
    return [[random.randint(0, 5) for _ in range(length)] for _ in range(size)]

# Fitness function: count the number of genes matching the target value
def fitness(chromosome, target_value):
    return sum(1 for gene in chromosome if gene == target_value)

# Selection: tournament selection
def select_parents(population, target_value):
    tournament_size = 5  # Increased tournament size for better selection pressure
    parents = []
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        parents.append(max(tournament, key=lambda x: fitness(x, target_value)))
    return parents

# Crossover: single-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation: change gene to a random value between 0 and 5 with a certain probability
def mutate(chromosome, rate):
    return [random.randint(0, 5) if random.random() < rate else gene for gene in chromosome]

# Function to display an individual on the canvas
def display_individual(canvas, individual, generation, fitness_value):
    canvas.delete("all")
    canvas.create_text(10, 10, anchor="nw", text=f"Generation: {generation}", font=("Futura", 14))
    canvas.create_text(10, 40, anchor="nw", text=f"Fitness: {fitness_value}", font=("Futura", 14))
    square_size = 30
    padding = 5
    canvas_width = one_max_canvas.winfo_width()
    canvas_height = one_max_canvas.winfo_height()
    total_width = len(individual) * (square_size + padding) - padding
    start_x = (canvas_width - total_width) // 2
    start_y = (canvas_height - square_size) // 2  # Center vertically
    for index, gene in enumerate(individual):
        color = number_to_color[gene]
        canvas.create_rectangle(
            start_x + index * (square_size + padding), start_y,
            start_x + index * (square_size + padding) + square_size, start_y + square_size,
            fill=color, outline="black"
        )
    canvas.update()

# Function to display the best solution found on the canvas
def display_best_solution(canvas, best_individual, best_fitness, generation):
    canvas.delete("all")
    canvas.create_text(10, 10, anchor="nw", text=f"Best Solution Found in Generation {generation}", font=("Futura", 14))
    canvas.create_text(10, 40, anchor="nw", text=f"Fitness: {best_fitness}", font=("Futura", 14))
    square_size = 30
    padding = 5
    canvas_width = one_max_canvas.winfo_width()
    canvas_height = one_max_canvas.winfo_height()
    total_width = len(best_individual) * (square_size + padding) - padding
    start_x = (canvas_width - total_width) // 2
    start_y = (canvas_height - square_size) // 2  # Center vertically
    for index, gene in enumerate(best_individual):
        color = number_to_color[gene]
        canvas.create_rectangle(
            start_x + index * (square_size + padding), start_y,
            start_x + index * (square_size + padding) + square_size, start_y + square_size,
            fill=color, outline="black"
        )
    canvas.update()

# Genetic algorithm
def genetic_algorithm(population_size, chromosome_length, mutation_rate, generations, target_value):
    population = initialize_population(population_size, chromosome_length)
    best_individual = None
    best_fitness = -1
    best_generation = 0
    
    for generation in range(generations):
        print(f"Generation {generation}:")
        for individual in population:
            fitness_value = fitness(individual, target_value)
            print(f"Individual: {individual}, Fitness: {fitness_value}")
            display_individual(one_max_canvas, individual, generation, fitness_value)
            time.sleep(0.02)

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, target_value)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))
        
        population = new_population

        current_best_individual = max(population, key=lambda x: fitness(x, target_value))
        current_best_fitness = fitness(current_best_individual, target_value)
        print(f"Best Fitness in Generation {generation}: {current_best_fitness}")

        if current_best_fitness > best_fitness:
            best_individual = current_best_individual
            best_fitness = current_best_fitness
            best_generation = generation

        if best_fitness == chromosome_length:
            print("Optimal solution found!")
            break

    return best_individual, best_fitness, best_generation

def exit_win(*args):
    exit()

# Update the parameters based on user input and rerun the algorithm
def update_parameters():
    global chromosome_length, generations
    if not chromosome_length_var.get().isdigit() or not (1 <= int(chromosome_length_var.get()) <= 20):
        messagebox.showerror("Invalid Input", "Please enter a valid number for chromosome length (1-20).")
        return
    if not generations_var.get().isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid number for generations.")
        return
    chromosome_length = int(chromosome_length_var.get())
    generations = int(generations_var.get())
    target_value = color_to_number[color_goal.get()]
    best_solution, best_fitness, best_generation = genetic_algorithm(population_size, chromosome_length, mutation_rate, generations, target_value)
    print("Best solution:", best_solution)
    print("Best fitness:", best_fitness)
    display_best_solution(one_max_canvas, best_solution, best_fitness, best_generation)

# Creation of the window
root = Tk()
root.title("One Max Problem")
root.geometry("800x600")
root.resizable(False, False)

# Creation of a frame for visuals parameters
param_frame = Frame(root, bg="gray")
param_frame.place(relx=0.0125, rely=0.0167, relwidth=0.975, relheight=0.475)

# Variable to store the selected color
color_goal = StringVar()
color_goal.set("red")

# Function to handle color selection
def select_color(color):
    color_goal.set(color)
    print(color)
    update_selected_color_display()

# Function to update the display of the selected color
def update_selected_color_display():
    selected_color_display.config(bg=color_goal.get())

choosing_square = Label(param_frame, text="Result color:", font=("Futura", 10))
choosing_square.place(relx=0.0125, rely=0.035)

# Create color squares
square_size = 30
padding = 10
for index, color in enumerate(colors):
    canvas = Canvas(param_frame, width=square_size, height=square_size, bg=color, highlightthickness=1, highlightbackground="black")
    canvas.place(x=50 + (square_size + padding) * index + padding, rely=0.15)
    canvas.bind("<Button-1>", lambda event, c=color: select_color(c))

# Display the currently selected color
selected_color_display = Canvas(param_frame, width=square_size * 1.25, height=square_size * 1.25, bg=color_goal.get(), highlightthickness=1, highlightbackground="black")
selected_color_display.place(x=10, rely=0.135)

# Entry field for chromosome length
chromosome_length_var = StringVar()
chromosome_length_var.set("10")  # Default value
chromosome_length_label = Label(param_frame, text="Chromosome Length (1-20):", font=("Futura", 10))
chromosome_length_label.place(relx=0.0125, rely=0.35)
chromosome_length_entry = Entry(param_frame, textvariable=chromosome_length_var)
chromosome_length_entry.place(relx=0.3, rely=0.35)

# Entry field for number of generations
generations_var = StringVar()
generations_var.set("50")  # Default value
generations_label = Label(param_frame, text="Number of Generations:", font=("Futura", 10))
generations_label.place(relx=0.0125, rely=0.45)
generations_entry = Entry(param_frame, textvariable=generations_var)
generations_entry.place(relx=0.3, rely=0.45)

# Button to update the parameters and run the algorithm
update_button = Button(param_frame, text="Run Algorithm", command=update_parameters)
update_button.place(relx=0.0125, rely=0.55)

# Creation of a frame for the visual of the problem
one_max_frame = Frame(root, bg="gray")
one_max_frame.place(relx=0.0125, rely=0.51, relwidth=0.975, relheight=0.475)

# Canvas to display the individuals
one_max_canvas = Canvas(one_max_frame, bg="white")
one_max_canvas.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

root.bind('<Escape>', exit_win)

root.mainloop()
