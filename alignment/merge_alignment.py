import json
import re
from collections import defaultdict

# Input e output file
input_file = 'alignment/aligned_output.json'
output_file = 'merged_fields_output.json'
synonym_file = 'alignment/synonym_dict.json'  # Il dizionario dei sinonimi

# Funzione per normalizzare il nome
def normalize_name(name):
    """Normalizza i nomi per identificare campi simili, unificando varianti come plurali, underscore, spazi e maiuscole."""
    normalized = re.sub(r'[\s_]+', '', name.strip().lower())  # Rimuove gli underscore e gli spazi
    normalized = re.sub(r's$', '', normalized)                # Rimuove plurali semplici
    return normalized

# Funzione per caricare il dizionario dei sinonimi
def load_synonym_dict(synonym_file):
    """Carica il dizionario dei sinonimi da un file JSON."""
    with open(synonym_file, 'r') as file:
        synonym_dict = json.load(file)
    return synonym_dict

# Funzione per trovare i sinonimi di un campo
def find_synonyms(field, synonym_dict):
    """Restituisce una lista di sinonimi di un campo, considerando anche se stesso."""
    for key, synonyms in synonym_dict.items():
        if field in synonyms:
            return set(synonyms)
    return {field}  # Se non troviamo sinonimi, restituiamo il campo stesso

# Funzione per unificare i campi simili
def merge_similar_fields(input_data, synonym_dict):
    """Unifica campi simili in un unico campo, usando anche il dizionario dei sinonimi."""
    aligned_names = input_data.get("aligned_names", {})
    aligned_values = input_data.get("aligned_values", {})

    field_mappings = defaultdict(list)
    reverse_mapping = {}

    # Identificare campi simili e unirli, considerando anche i sinonimi
    for field in aligned_names:
        normalized_field = normalize_name(field)

        # Trova i sinonimi per questo campo
        synonyms = find_synonyms(field, synonym_dict)

        # Unifica il campo con il suo rappresentante di sinonimi
        representative = min(synonyms)  # Usa il termine alfabeticamente più piccolo come rappresentante
        if representative not in reverse_mapping:
            reverse_mapping[representative] = field

        # Aggiungi i termini nel mapping dei campi unificati
        field_mappings[representative].extend(aligned_names[field])

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

# Carica il dizionario dei sinonimi
synonym_dict = load_synonym_dict(synonym_file)

# Creare il file con i campi unificati
merged_output = merge_similar_fields(input_data, synonym_dict)

# Scrivere il file di output
with open(output_file, 'w') as file:
    json.dump(merged_output, file, indent=4)

print(f"File con campi unificati salvato come {output_file}.")
