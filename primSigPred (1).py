import time
import matplotlib.pyplot as plt
import numpy as np

# Function to load the grammar from a .txt file
def load_grammar(file):
    grammar = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if '->' not in line or not line:
                continue
            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs = [tuple(part.strip().split()) for part in rhs.split('|')]
            if lhs in grammar:
                grammar[lhs].extend(rhs)
            else:
                grammar[lhs] = rhs
    return grammar

# Function to calculate the FIRST set
def first_sets(grammar, symbol, first_cache, in_process=set()):
    if symbol in first_cache:
        return first_cache[symbol]
    if symbol in in_process:
        return set()

    in_process.add(symbol)
    result = set()
    
    if symbol not in grammar:  # If it's a terminal
        result.add(symbol)
    else:
        for production in grammar[symbol]:
            if not production:
                result.add('')
            else:
                for part in production:
                    part_first = first_sets(grammar, part, first_cache, in_process)
                    result.update(part_first - {''})
                    if '' not in part_first:
                        break
                else:
                    result.add('')

    in_process.remove(symbol)
    first_cache[symbol] = result
    return result

# Function to calculate the FOLLOW set
def follow_sets(grammar, symbol, first_cache, follow_cache, start_symbol):
    if symbol in follow_cache:
        return follow_cache[symbol]

    result = set()
    if symbol == start_symbol:
        result.add('$')

    follow_cache[symbol] = result

    for lhs, rhs_list in grammar.items():
        for production in rhs_list:
            for idx, produced_symbol in enumerate(production):
                if produced_symbol == symbol:
                    if idx + 1 < len(production):
                        next_symbol = production[idx + 1]
                        result.update(first_sets(grammar, next_symbol, first_cache) - {''})
                    if idx + 1 == len(production) or '' in first_cache.get(production[idx + 1], set()):
                        if lhs != symbol:
                            result.update(follow_sets(grammar, lhs, first_cache, follow_cache, start_symbol))

    follow_cache[symbol] = result
    return result

# Function to calculate the PREDICTIONS
def predictions(grammar, first_cache, follow_cache, start_symbol):
    predictions_result = {}
    for lhs, rhs_list in grammar.items():
        for production in rhs_list:
            prediction = set()
            for part in production:
                part_first = first_sets(grammar, part, first_cache)
                prediction.update(part_first - {''})
                if '' not in part_first:
                    break
            else:
                prediction.update(follow_sets(grammar, lhs, first_cache, follow_cache, start_symbol))
            predictions_result[(lhs, production)] = prediction
    return predictions_result

# Function to measure execution time for FIRST, FOLLOW, and PREDICTIONS
def measure_time(grammar):
    first_cache = {}
    follow_cache = {}
    start_symbol = list(grammar.keys())[0]

    # Measure FIRST sets
    start_time = time.perf_counter()
    for symbol in grammar:
        first_sets(grammar, symbol, first_cache)
    end_time = time.perf_counter()
    time_first = end_time - start_time

    # Measure FOLLOW sets
    start_time = time.perf_counter()
    for symbol in grammar:
        follow_sets(grammar, symbol, first_cache, follow_cache, start_symbol)
    end_time = time.perf_counter()
    time_follow = end_time - start_time

    # Measure PREDICTIONS
    start_time = time.perf_counter()
    predictions_result = predictions(grammar, first_cache, follow_cache, start_symbol)
    end_time = time.perf_counter()
    time_predictions = end_time - start_time

    return time_first, time_follow, time_predictions, predictions_result

# Function to plot execution time for FIRST using matplotlib
def plot_first(lengths, first_times):
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, first_times, marker='o', label='First Execution Time')
    plt.title('Execution Time of First Algorithm')
    plt.xlabel('String Length')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.legend()
    
    # Ajusta los límites de los ejes para mantener la misma escala
    plt.xlim(0, max(lengths) + 10)           # Ajusta el rango según las longitudes
    plt.ylim(0, max(prediction_times) * 1.1) # Ajusta el rango según los tiempos

    plt.savefig('first_execution_time.png')
    plt.close()

# Function to plot execution time for FOLLOW using matplotlib
def plot_follow(lengths, follow_times):
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, follow_times, marker='o', color='orange', label='Follow Execution Time')
    plt.title('Execution Time of Follow Algorithm')
    plt.xlabel('String Length')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.legend()
    
    # Ajusta los límites de los ejes para mantener la misma escala
    plt.xlim(0, max(lengths) + 10)         # Ajusta el rango según las longitudes
    plt.ylim(0, max(follow_times) * 1.1)   # Ajusta el rango según los tiempos
    
    plt.savefig('follow_execution_time.png')
    plt.close()


# Function to plot execution time for PREDICTIONS using matplotlib
def plot_predictions(lengths, prediction_times):
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, prediction_times, marker='o', color='green', label='Prediction Execution Time')
    plt.title('Execution Time of Prediction Algorithm')
    plt.xlabel('String Length')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.legend()
    
    # Ajusta los límites de los ejes para mantener la misma escala
    plt.xlim(0, max(lengths) + 10)           # Ajusta el rango según las longitudes
    plt.ylim(0, max(prediction_times) * 1.1) # Ajusta el rango según los tiempos
    
    plt.savefig('prediction_execution_time.png')
    plt.close()


# Load the grammar from the "gramatica.txt" file
grammar_file = 'gramatica.txt'
grammar = load_grammar(grammar_file)

# Define the string to evaluate
user_string = (
    "En un pequeño mundo, un gato feliz corre junto a un niño. Juntos, juegan con una pelota grande en el parque. "
    "La niña, que observa desde la casa bonita, también quiere unirse a la diversión. Ella juega con su perro y "
    "cuenta historias sobre un mundo mágico. Mientras tanto, el gato escucha atentamente, con sus ojos brillantes, "
)

# Generate a subset of strings automatically with increasing lengths
additional_strings = [user_string[:i] for i in range(5, len(user_string) + 1, 10)]  # Representative subset

# Measure execution times for the generated strings
first_times = []
follow_times = []
prediction_times = []

for string in additional_strings:
    time_first, time_follow, time_prediction, _ = measure_time(load_grammar(grammar_file))
    first_times.append(time_first)
    follow_times.append(time_follow)
    prediction_times.append(time_prediction)

# Plot the results
plot_first([len(string) for string in additional_strings], first_times)
plot_follow([len(string) for string in additional_strings], follow_times)
plot_predictions([len(string) for string in additional_strings], prediction_times)

# Print the results
print(f"Execution time for First: {first_times[0]:.6f} seconds for a string of length {len(user_string)}")
print(f"Execution time for Follow: {follow_times[0]:.6f} seconds for a string of length {len(user_string)}")
print(f"Execution time for Predictions: {prediction_times[0]:.6f} seconds for a string of length {len(user_string)}")
