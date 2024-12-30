import json
import re
from collections import defaultdict

# Input e output file
input_file = 'aligned_output.json'
output_file = 'merged_fields_output.json'

def normalize_name(name):
    """Normalizza i nomi per identificare campi simili, unificando varianti come plurali, underscore, spazi e maiuscole."""
    # Rimuovi gli underscore e gli spazi e converte tutto a minuscolo
    normalized = re.sub(r'[\s_]+', '', name.strip().lower())  # Rimuove gli underscore e gli spazi
    normalized = re.sub(r's$', '', normalized)  # Rimuove plurali semplici
    return normalized

def merge_similar_fields(input_data):
    """Unifica campi simili in un unico campo."""
    aligned_names = input_data.get("aligned_names", {})
    aligned_values = input_data.get("aligned_values", {})

    field_mappings = defaultdict(list)
    reverse_mapping = {}

    # Identificare campi simili e unirli
    for field in aligned_names:
        normalized_field = normalize_name(field)

        # Se il campo normalizzato esiste già, uniamolo, altrimenti creiamo un nuovo mapping
        if normalized_field in reverse_mapping:
            merged_field = reverse_mapping[normalized_field]
        else:
            merged_field = field
            reverse_mapping[normalized_field] = merged_field

        field_mappings[merged_field].extend(aligned_names[field])

    # Creare una nuova struttura per i campi unificati
    merged_aligned_names = {field: list(set(ids)) for field, ids in field_mappings.items()}

    # Creare una mappa per i valori corrispondenti
    merged_aligned_values = defaultdict(list)
    for value, ids in aligned_values.items():
        for id in ids:
            # La logica di unione si basa sul confronto tra l'ID e il campo normalizzato
            for normalized_field, merged_field in reverse_mapping.items():
                if normalize_name(id.split('_')[2]) == normalized_field:
                    merged_aligned_values[merged_field].extend(ids)

    merged_aligned_values = {field: list(set(ids)) for field, ids in merged_aligned_values.items()}

    # Il file risultante
    merged_output = {
        "merged_aligned_names": merged_aligned_names,
        "merged_aligned_values": merged_aligned_values
    }

    return merged_output

# Leggere il file di input
with open(input_file, 'r') as file:
    input_data = json.load(file)

# Creare il file con i campi unificati
merged_output = merge_similar_fields(input_data)

# Scrivere il file di output
with open(output_file, 'w') as file:
    json.dump(merged_output, file, indent=4)

print(f"File con campi unificati salvato come {output_file}.")
