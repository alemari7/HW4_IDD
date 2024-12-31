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

            # Ottieni il nome del file senza l'estensione
            file_name_without_extension = os.path.splitext(filename)[0]
            
            # Leggi il contenuto del file JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)

                    # Estrai gli ID dalla struttura JSON
                    for item_id in data.keys():
                        # Concatena il nome del file con l'ID
                        new_key = f"{file_name_without_extension}_{item_id}"

                        # Aggiungi la chiave concatenata al dizionario con valore di default
                        if new_key not in id_mapping:
                            id_mapping[new_key] = 0  # Valore di default

            except Exception as e:
                print(f"Errore nella lettura del file {filename}: {e}")

    # Ordina id_mapping per chiave in ordine alfabetico
    id_mapping_sorted = dict(sorted(id_mapping.items()))

    # Scrivi il mapping in un file JSON di output
    try:
        with open(output_file, 'w', encoding='utf-8') as output_json:
            json.dump(id_mapping_sorted, output_json, ensure_ascii=False, indent=4)
        print(f"File di output creato con successo: {output_file}")
    except Exception as e:
        print(f"Errore nella scrittura del file di output: {e}")

# Specifica il percorso della cartella e il file di output
input_folder = "sources/json"  # Cambia con il percorso della tua cartella
output_file = "output_mapping.json"   # Nome del file di output

# Esegui la funzione
process_json_folder(input_folder, output_file)
