import json
import csv
import os
from collections import Counter

INPUT_SPEC = 'distribution/specifiche.json'  # Percorso del tuo file JSON
INPUT_METRIC = 'distribution/metriche.json'  # Percorso del tuo file JSON
OUTPUT = 'NAME_PROFILING.csv'                # Nome del file CSV di output

# versione allineata
INPUT_SPEC_ALIGNED = 'alignment/aligned_specifiche.json'  # Percorso del tuo file JSON
INPUT_METRIC_ALIGNED = 'alignment/aligned_metriche.json'  # Percorso del tuo file JSON
OUTPUT_ALIGNED = 'alignment/NAME_PROFILING_ALIGNED.csv'   # Nome del file CSV di output

# Funzione per caricare il JSON da un file esterno
def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} non trovato")
        exit(1)

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

# Funzione per calcolare e salvare la distribuzione sui valori
def values_distribution(input_filename, output_filename):
    data = load_json(input_filename)
    values = [list(item.values())[0] for item in data.values()]
    distribution = Counter(values)
    save_distribution_to_csv(distribution, output_filename, ['Value', 'Frequency'])
    print(f"La distribuzione dei valori è stata salvata in {output_filename}")

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
values_distribution(INPUT_SPEC, OUTPUT)
metric_averages(INPUT_METRIC, OUTPUT)

# Esegui le distribuzioni allineate
spec_distribution(INPUT_SPEC_ALIGNED, OUTPUT_ALIGNED)
metric_distribution(INPUT_METRIC_ALIGNED, OUTPUT_ALIGNED)
values_distribution(INPUT_SPEC_ALIGNED, OUTPUT_ALIGNED)
metric_averages(INPUT_METRIC_ALIGNED, OUTPUT_ALIGNED)