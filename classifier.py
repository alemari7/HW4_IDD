import os
import json

# Funzione per elaborare i file JSON e creare il file di output
def process_json_folder(input_folder, output_file):
    # Dizionario per mappare ID a valori di default
    id_mapping = {}

    # Itera su tutti i file nella cartella
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            
            # Leggi il contenuto del file JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)

                    # Estrai gli ID dalla struttura JSON
                    for item_id in data.keys():
                        if item_id not in id_mapping:
                            id_mapping[item_id] = 0  # Valore di default

            except Exception as e:
                print(f"Errore nella lettura del file {filename}: {e}")

    # Scrivi il mapping in un file JSON di output
    try:
        with open(output_file, 'w', encoding='utf-8') as output_json:
            json.dump(id_mapping, output_json, ensure_ascii=False, indent=4)
        print(f"File di output creato con successo: {output_file}")
    except Exception as e:
        print(f"Errore nella scrittura del file di output: {e}")

# Specifica il percorso della cartella e il file di output
input_folder = "sources/json"  # Cambia con il percorso della tua cartella
output_file = "output_mapping.json"   # Nome del file di output

# Esegui la funzione
process_json_folder(input_folder, output_file)
