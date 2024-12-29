import json
import csv
import os
from collections import Counter

INPUT_SPEC = 'Distribution/specifiche.json'  # Percorso del tuo file JSON
INPUT_METRIC = 'Distribution/metriche.json'  # Percorso del tuo file JSON
OUTPUT = 'NAME_PROFILING.csv'                # Nome del file CSV di output

# Funzione per caricare il JSON da un file esterno
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Funzione per salvare la distribuzione in un file CSV (in modalità append)
def save_distribution_to_csv(distribution, output_filename, headers):
    with open(output_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Scrivi le intestazioni
        # Scrivi le righe della distribuzione
        for name, count in distribution.items():
            writer.writerow([name, count])
        writer.writerow([])  # Riga vuota separatrice

# Funzione per calcolare e salvare la distribuzione delle specifiche
def spec_distribution(input_filename, output_filename):
    data = load_json(input_filename)
    first_elements = [list(item.keys())[0] for item in data.values()]
    distribution = Counter(first_elements)
    save_distribution_to_csv(distribution, output_filename, ['Specification', 'Frequency'])
    print(f"La distribuzione delle specifiche è stata salvata in {output_filename}")

# Funzione per calcolare e salvare la distribuzione delle metriche
def metric_distribution(input_filename, output_filename):
    data = load_json(input_filename)
    first_elements = [list(item.keys())[0] for item in data.values()]
    distribution = Counter(first_elements)
    save_distribution_to_csv(distribution, output_filename, ['Metric', 'Frequency'])
    print(f"La distribuzione delle metriche è stata salvata in {output_filename}")

# Funzione per calcolare le medie delle metriche e salvarle nel file CSV
def metric_averages(input_filename, output_filename):
    data = load_json(input_filename)
    metrics = {}

    # Raccogli i valori per ciascuna metrica
    for entry in data.values():
        for metric, value in entry.items():
            try:
                value = float(value)  # Converte il valore in float
                if metric not in metrics:
                    metrics[metric] = []
                metrics[metric].append(value)
            except ValueError:
                continue  # Ignora se il valore non è un numero

    # Calcola la media per ciascuna metrica
    averages = {metric: sum(values) / len(values) for metric, values in metrics.items()}
    save_distribution_to_csv(averages, output_filename, ['Metric', 'Average'])
    print(f"Le medie delle metriche sono state salvate in {output_filename}")

# Rimuove il file esistente (se presente) per ricrearlo da zero
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

# Esegui le distribuzioni
spec_distribution(INPUT_SPEC, OUTPUT)
metric_distribution(INPUT_METRIC, OUTPUT)
metric_averages(INPUT_METRIC, OUTPUT)
