import os
import json

# Funzione per determinare se un dettaglio può essere una metrica
def is_potential_metric(detail):
    # Considera una colonna come metrica se contiene un nome plausibile seguito da un valore
    parts = detail.split(",", 1)
    return len(parts) == 2 and parts[0].strip() and parts[1].strip()

# Funzione per convertire un claim nel nuovo formato
def convert_claims_format(input_data):
    converted = []
    for index, claim in enumerate(input_data):
        key = f"Claim {index}"
        if key in claim:
            # Analizza il campo stringa nel formato specificato
            details = claim[key].strip("|{}").split("|,|")
            specifications = {}
            measure = ""
            outcome = "N/A"
            
            # Analizziamo tutte le specifiche, tranne gli ultimi dettagli
            for spec_index, detail in enumerate(details[:-1]):  # Escludiamo l'ultimo dettaglio per ora
                parts = detail.split(",", 1)
                if len(parts) == 2:
                    name, value = map(str.strip, parts)
                    specifications[str(spec_index)] = {"name": name, "value": value}
            
            # Estraiamo la metrica e l'outcome dall'ultimo dettaglio
            last_detail = details[-1]
            if ',' in last_detail:
                measure, outcome = map(str.strip, last_detail.split(",", 1))
            
            # Aggiungi il risultato al formato specifico
            converted.append({
                str(index): {
                    "specifications": specifications,
                    "Measure": measure,
                    "Outcome": outcome
                }
            })
    return converted

# Funzione per convertire tutti i file JSON in una directory
def process_json_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, f"converted_{file_name}")
            
            # Leggi il file JSON originale
            with open(input_path, 'r') as file:
                input_data = json.load(file)
            
            # Converte i dati
            converted_data = convert_claims_format(input_data)
            
            # Scrivi il nuovo file JSON
            with open(output_path, 'w') as file:
                json.dump(converted_data, file, indent=4)

# Directory di input e output
input_directory = "JSON_CLAIMS"  # Sostituisci con il percorso della tua cartella
output_directory = "JSON_CLAIMS_CONVERTED"  # Cartella dove salvare i file convertiti

# Esegui la conversione
process_json_files(input_directory, output_directory)
