import time
import matplotlib.pyplot as plt
import os

# Function to load grammar from a .txt file
def load_grammar(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    grammar = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if '->' not in line or not line:
                continue
            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs = [tuple(part.strip().split()) for part in rhs.split('|')]
            grammar.setdefault(lhs, []).extend(rhs)
    return grammar

# Function to compute FIRST sets
def compute_firsts(grammar, symbol, first_cache, processing=set()):
    if symbol in first_cache:
        return first_cache[symbol]
    if symbol in processing:
        return set()  # Prevent infinite loops

    processing.add(symbol)
    result = set()
    
    if symbol not in grammar:  # Terminal symbol
        result.add(symbol)
    else:
        for production in grammar[symbol]:
            for part in production:
                part_firsts = compute_firsts(grammar, part, first_cache, processing)
                result.update(part_firsts - {''})
                if '' not in part_firsts:
                    break
            else:
                result.add('')

    processing.remove(symbol)
    first_cache[symbol] = result
    return result

# Function to compute FOLLOW sets
def compute_follows(grammar, symbol, first_cache, follow_cache, start_symbol):
    if symbol in follow_cache:
        return follow_cache[symbol]

    result = set()
    if symbol == start_symbol:
        result.add('$')  # Add end-of-input marker

    follow_cache[symbol] = result

    for lhs, rhs_list in grammar.items():
        for production in rhs_list:
            for idx, prod_symbol in enumerate(production):
                if prod_symbol == symbol:
                    if idx + 1 < len(production):
                        next_symbol = production[idx + 1]
                        result.update(compute_firsts(grammar, next_symbol, first_cache) - {''})
                    if idx + 1 == len(production) or '' in first_cache.get(production[idx + 1], set()):
                        if lhs != symbol:
                            result.update(compute_follows(grammar, lhs, first_cache, follow_cache, start_symbol))

    follow_cache[symbol] = result
    return result

# Function to compute PREDICTIONS
def compute_predictions(grammar, first_cache, follow_cache, start_symbol):
    predictions = {}
    for lhs, rhs_list in grammar.items():
        for production in rhs_list:
            prediction = set()
            for part in production:
                part_firsts = compute_firsts(grammar, part, first_cache)
                prediction.update(part_firsts - {''})
                if '' not in part_firsts:
                    break
            else:
                prediction.update(compute_follows(grammar, lhs, first_cache, follow_cache, start_symbol))
            predictions[(lhs, production)] = prediction
    return predictions

# Function to measure execution times
def measure_times(grammar):
    first_cache = {}
    follow_cache = {}
    start_symbol = next(iter(grammar.keys()))

    # Measure FIRST times
    start = time.perf_counter()
    for symbol in grammar:
        compute_firsts(grammar, symbol, first_cache)
    first_time = time.perf_counter() - start

    # Measure FOLLOW times
    start = time.perf_counter()
    for symbol in grammar:
        compute_follows(grammar, symbol, first_cache, follow_cache, start_symbol)
    follow_time = time.perf_counter() - start

    # Measure PREDICTION times
    start = time.perf_counter()
    predictions = compute_predictions(grammar, first_cache, follow_cache, start_symbol)
    prediction_time = time.perf_counter() - start

    return first_time, follow_time, prediction_time, predictions

# Function to plot execution times (improved visualization)
def plot_execution_times(lengths, first_times, follow_times, prediction_times):
    plt.figure(figsize=(12, 7))
    
    # Plotting the times
    plt.plot(lengths, first_times, 'o-', label='Firsts', color='#1f77b4', markersize=6, linewidth=2)
    plt.plot(lengths, follow_times, 's-', label='Follows', color='#2ca02c', markersize=6, linewidth=2)
    plt.plot(lengths, prediction_times, '^-', label='Predictions', color='#d62728', markersize=6, linewidth=2)
    
    # Adding titles and labels
    plt.title('Execution Times for Grammar Calculations', fontsize=18, fontweight='bold')
    plt.xlabel('String Length (number of symbols)', fontsize=14)
    plt.ylabel('Time (seconds)', fontsize=14)
    
    # Adjusting Y-axis range
    min_y = min(min(first_times), min(follow_times), min(prediction_times)) * 0.9
    max_y = max(max(first_times), max(follow_times), max(prediction_times)) * 1.1
    plt.ylim(min_y, max_y)
    
    # Configuring grid, legend, and style
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='upper left')
    
    # Adding a background style
    plt.gca().set_facecolor('#f7f7f7')
    
    # Improving margins
    plt.tight_layout()
    
    # Save and display the plot
    plt.savefig('execution_times_improved.png', dpi=300)
    plt.show()

# Main entry point
if __name__ == "__main__":
    grammar_file = 'gramatica.txt'  # Ensure the .txt file exists in the same directory
    grammar = load_grammar(grammar_file)

    # Generate test strings and measure times
    string_lengths = range(5, 101, 10)
    first_times, follow_times, prediction_times = [], [], []

    for length in string_lengths:
        times = measure_times(grammar)
        first_times.append(times[0])
        follow_times.append(times[1])
        prediction_times.append(times[2])

    # Call the function to plot execution times
    plot_execution_times(
        list(string_lengths),
        first_times,
        follow_times,
        prediction_times
    )
