import json
import csv
from collections import Counter

# Funzione principale per calcolare e salvare la distribuzione
def spec_distribution(input_filename, output_filename):
    # Funzione per caricare il JSON da un file esterno
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Funzione per salvare la distribuzione in un file CSV
    def save_distribution_to_csv(distribution, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Frequency'])  # Intestazioni
            for name, count in distribution.items():
                writer.writerow([name, count])

    # Carica il JSON dal file di input
    data = load_json(input_filename)

    # Estrazione dei primi elementi
    first_elements = [list(item.keys())[0] for item in data.values()]

    # Conteggio delle occorrenze
    distribution = Counter(first_elements)

    # Salva la distribuzione in un file CSV
    save_distribution_to_csv(distribution, output_filename)

    print(f"La distribuzione è stata salvata in {output_filename}")


input_filename = 'Distribution/specifiche.json'     # Percorso del tuo file JSON
output_filename = 'distribution.csv'                # Nome del file CSV di output
spec_distribution(input_filename, output_filename)
