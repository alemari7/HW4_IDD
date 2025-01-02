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
            
            for spec_index, detail in enumerate(details):
                parts = detail.split(",", 1)
                if len(parts) == 2:
                    name, value = map(str.strip, parts)
                    specifications[str(spec_index)] = {"name": name, "value": value}
                else:
                    continue
            
            # Determina la metrica e l'outcome
            if details:
                # Prova con l'ultima colonna come metrica
                last_detail = details[-1]
                if is_potential_metric(last_detail):
                    last_detail_parts = last_detail.split(",", 1)
                    measure = last_detail_parts[0].strip()
                    outcome = last_detail_parts[1].strip()
                else:
                    # Cerca una colonna plausibile come metrica
                    for detail in details:
                        if is_potential_metric(detail):
                            metric_parts = detail.split(",", 1)
                            measure = metric_parts[0].strip()
                            outcome = metric_parts[1].strip()
                            break

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
