import os
import json


# Funzione per convertire un claim nel nuovo formato
def convert_claims_format(input_data):
    converted = []
    for index, claim in enumerate(input_data):
        key = f"Claim {index}"
        if key in claim:
            # Analizza il campo stringa nel formato specificato
            raw_data = claim[key].strip("|")
            specifications = {}
            measure = ""
            outcome = "N/A"
            
            # Trova la parte tra { e }, e quella successiva
            if "{|" in raw_data and "|}" in raw_data:
                spec_part, metric_part = raw_data.split("|},", 1)
                spec_part = spec_part.strip("{|").split("|,|")
                
                # Analizza le specifiche
                for spec_index, detail in enumerate(spec_part):
                    if "," in detail:
                        name, value = map(str.strip, detail.split(",", 1))
                        specifications[str(spec_index)] = {"name": name, "value": value}
                
                # Analizza la metrica e l'outcome
                if "," in metric_part:
                    measure, outcome = map(str.strip, metric_part.split(",", 1))
            
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
            output_path = os.path.join(output_dir, f"{file_name}")
            
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
