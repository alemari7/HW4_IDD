import json
import csv
import os
from collections import Counter

INPUT_SPEC = 'Distribution/specifiche.json'  # Percorso del tuo file JSON
INPUT_METRIC = 'Distribution/metriche.json'  # Percorso del tuo file JSON
OUTPUT = 'distribution.csv'  # Nome del file CSV di output

# Funzione principale per calcolare e salvare la distribuzione
def spec_distribution(input_filename, output_filename):
    # Funzione per caricare il JSON da un file esterno
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Funzione per salvare la distribuzione in un file CSV (in modalità append)
    def save_distribution_to_csv(distribution, output_filename):
        # Apre il file in modalità append ('a') dopo averlo creato
        with open(output_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Specification', 'Frequency'])  # Intestazioni
            # Scrive solo le righe della distribuzione, non le intestazioni
            for name, count in distribution.items():
                writer.writerow([name, count])
            writer.writerow([])

    
    # Carica il JSON dal file di input
    data = load_json(input_filename)

    # Estrazione dei primi elementi
    first_elements = [list(item.keys())[0] for item in data.values()]

    # Conteggio delle occorrenze
    distribution = Counter(first_elements)

    # Salva la distribuzione nel file CSV
    save_distribution_to_csv(distribution, output_filename)

    print(f"La distribuzione delle specifiche è stata salvata in {output_filename}")

# Funzione principale per calcolare e salvare la distribuzione
def metric_distribution(input_filename, output_filename):
    # Funzione per caricare il JSON da un file esterno
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Funzione per salvare la distribuzione in un file CSV (in modalità append)
    def save_distribution_to_csv(distribution, output_filename):
        # Apre il file in modalità append ('a') dopo averlo creato
        with open(output_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Metric', 'Frequency'])  # Intestazioni
            # Scrive solo le righe della distribuzione, non le intestazioni
            for name, count in distribution.items():
                writer.writerow([name, count])
            writer.writerow([])

    
    # Carica il JSON dal file di input
    data = load_json(input_filename)

    # Estrazione dei primi elementi
    first_elements = [list(item.keys())[0] for item in data.values()]

    # Conteggio delle occorrenze
    distribution = Counter(first_elements)

    # Salva la distribuzione nel file CSV
    save_distribution_to_csv(distribution, output_filename)

    print(f"La distribuzione delle metriche è stata salvata in {output_filename}")

# Funzione che calcola le medie delle metriche e le salva nel file CSV
def process_and_save_averages(input_filename, output_filename):
    # Funzione per caricare il JSON da un file esterno
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Funzione per salvare la distribuzione in un file CSV (in modalità append)
    def save_distribution_to_csv(distribution):
        # Apre il file in modalità append ('a') dopo averlo creato
        with open(output_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Metric', 'Average'])  # Intestazioni
            # Scrive solo le righe della distribuzione
            for name, avg in distribution.items():
                writer.writerow([name, avg])
            writer.writerow([])  # Riga vuota separatrice

    # Funzione per calcolare la media per ciascuna metrica
    def calculate_average_per_metric():
        # Carica il JSON dal file
        data = load_json(input_filename)
        
        # Dizionario per mantenere i valori per ciascuna metrica
        metrics = {}
        
        # Itera attraverso il dizionario JSON e raccoglie i valori per ogni metrica
        for entry in data.values():
            for metric, value in entry.items():
                try:
                    # Converte il valore in float e aggiungilo alla lista delle metriche
                    value = float(value)
                    
                    if metric not in metrics:
                        metrics[metric] = []
                    metrics[metric].append(value)
                except ValueError:
                    # Se il valore non è un numero, lo ignora
                    continue
        
        # Calcola la media per ciascuna metrica
        averages = {}
        for metric, values in metrics.items():
            averages[metric] = sum(values) / len(values)
        
        return averages

    # Calcola le medie per ciascuna metrica
    averages = calculate_average_per_metric()

    # Salva la distribuzione nel file CSV esistente (append)
    save_distribution_to_csv(averages)

    print(f"Le medie delle metriche sono state salvate in {output_filename}")


# Rimuove il file esistente (se presente) per ricrearlo da zero
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

spec_distribution(INPUT_SPEC, OUTPUT)
metric_distribution(INPUT_METRIC, OUTPUT)
process_and_save_averages(INPUT_METRIC, OUTPUT)