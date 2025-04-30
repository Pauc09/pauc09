import time
import matplotlib.pyplot as plt
import os
import multiprocessing as mp
import numpy as np


# Function to load the grammar from a .txt file
def cargar_gramatica(archivo):
    gramatica = {}
    with open(archivo, 'r') as file:
        for linea in file:
            linea = linea.strip()
            if '->' not in linea or not linea:
                continue
            lhs, rhs = linea.split('->')
            lhs = lhs.strip()
            rhs = [tuple(part.strip().split()) for part in rhs.split('|')]
            if lhs in gramatica:
                gramatica[lhs].extend(rhs)
            else:
                gramatica[lhs] = rhs
    return gramatica

# Function to implement the CYK algorithm
def cyk_algorithm(grammar, input_string):
    n = len(input_string)
    table = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for lhs, rhs in grammar.items():
            for production in rhs:
                if len(production) == 1 and production[0] == input_string[i]:
                    table[i][i].add(lhs)

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for lhs, rhs in grammar.items():
                    for production in rhs:
                        if len(production) == 2:
                            B, C = production
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)

    return 'S' in table[0][n - 1]

# Function to measure execution time for the entire program
def medir_tiempo_total(grammar, cadena_usuario):
    start_time = time.perf_counter()
    
    # Generate a subset of strings automatically with increasing lengths
    cadenas_adicionales = [cadena_usuario[:i] for i in range(5, len(cadena_usuario) + 1, 10)]  # Representative subset
    
    # Measure execution times for the generated strings
    tiempos_y_longitudes = []
    for cadena in cadenas_adicionales:
        tiempo = medir_tiempo_una_cadena((grammar, cadena))
        tiempos_y_longitudes.append(tiempo)
        
    end_time = time.perf_counter()
    tiempo_total = end_time - start_time
    
    # Separate times and lengths for plotting
    tiempos_ejecucion, longitudes_cadenas = zip(*tiempos_y_longitudes)

    # Plot the results
    graficar_tiempos(longitudes_cadenas, tiempos_ejecucion)

    return tiempo_total

# Function to measure execution time for a single string
def medir_tiempo_una_cadena(args):
    grammar, cadena = args
    start_time = time.perf_counter()
    cyk_algorithm(grammar, cadena)
    end_time = time.perf_counter()
    tiempo = end_time - start_time
    longitud = len(cadena)
    return tiempo, longitud

# Function to plot execution times using matplotlib
def graficar_tiempos(longitudes, tiempos):
    plt.plot(longitudes, tiempos, marker='o')
    plt.title('Execution Time of CYK Algorithm')
    plt.xlabel('String Length')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    
    # Ajusta los límites de los ejes para mantener la misma escala
    plt.xlim(0, max(longitudes) + 10)  # Ajusta el rango según las longitudes
    plt.ylim(0, max(tiempos) * 1.1)    # Ajusta el rango según los tiempos
    
    plt.savefig(os.path.join(os.path.dirname(__file__), 'execution_time.png'))
    plt.close()

# Load the grammar from the "gramatica.txt" file
archivo_gramatica = 'gramatica.txt'
grammar = cargar_gramatica(archivo_gramatica)

# Define the string to evaluate
cadena_usuario = (
    "En un pequeño mundo, un gato feliz corre junto a un niño. Juntos, juegan con una pelota grande en el parque. "
    "La niña, que observa desde la casa bonita, también quiere unirse a la diversión. Ella juega con su perro y "
    "cuenta historias sobre un mundo mágico. Mientras tanto, el gato escucha atentamente, con sus ojos brillantes, "
)

# Measure total execution time and string length
tiempo_total = medir_tiempo_total(grammar, cadena_usuario)
longitud_cadena_usuario = len(cadena_usuario)

# Print the results
print(f"Total Execution Time: {tiempo_total:.6f} seconds")
print(f"String Length: {longitud_cadena_usuario} characters")

