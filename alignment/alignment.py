import json
import re
import os
from collections import defaultdict

# Cartella contenente i file JSON
input_folder = 'JSON_CLAIMS'
output_file = 'alignment/aligned_output.json'

def normalize_name(name):
    """Normalizza i nomi per l'allineamento, gestendo variazioni come underscore e maiuscole."""
    return re.sub(r'[\s_]+', ' ', name.strip().lower())

def find_generic_name(name, name_aliases):
    """Trova o crea un nome generico per un attributo dato, unificando variazioni simili."""
    for generic_name, aliases in name_aliases.items():
        if name in aliases:
            return generic_name
    # Se non esiste ancora un alias, usalo come nuovo nome generico
    name_aliases[name].add(name)
    return name

def process_claims(data, paper_id, name_aliases):
    aligned_names = {}
    aligned_values = {}

    for claim_id, claim_data in enumerate(data):
        for key, value in claim_data.items():
            # Estrazione delle specifiche
            matches = re.findall(r'\|([^|]+), ([^|]+)\|', value)
            spec_id=1
            for match in matches:
                raw_name, raw_value = match
                normalized_name = normalize_name(raw_name)
                generic_name = find_generic_name(normalized_name, name_aliases)  # Trova o unifica il nome generico

                paper_id = paper_id.replace("_claims", "")
                spec_id = f"{paper_id}_{claim_id}_{spec_id}"
                spec_id += 1

                # Allineamento nomi
                if generic_name not in aligned_names:
                    aligned_names[generic_name] = []
                aligned_names[generic_name].append(spec_id)

                # Allineamento valori
                if raw_value not in aligned_values:
                    aligned_values[raw_value] = []
                aligned_values[raw_value].append(spec_id)

    return {
        "aligned_names": aligned_names,
        "aligned_values": aligned_values
    }

# Mappatura delle alias per i nomi
name_aliases = defaultdict(set)

# Elaborazione di tutti i file JSON nella cartella
aligned_names = {}
aligned_values = {}

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        input_path = os.path.join(input_folder, filename)
        paper_id = os.path.splitext(filename)[0]

        with open(input_path, 'r') as file:
            data = json.load(file)
            result = process_claims(data, paper_id, name_aliases)

            # Unione dei risultati
            for key, value in result["aligned_names"].items():
                if key not in aligned_names:
                    aligned_names[key] = []
                aligned_names[key].extend(value)

            for key, value in result["aligned_values"].items():
                if key not in aligned_values:
                    aligned_values[key] = []
                aligned_values[key].extend(value)

# Salvataggio del file JSON risultante
final_output = {
    "aligned_names": aligned_names,
    "aligned_values": aligned_values
}

with open(output_file, 'w') as file:
    json.dump(final_output, file, indent=4)

print(f"Elaborazione completata. File salvato come {output_file}.")
