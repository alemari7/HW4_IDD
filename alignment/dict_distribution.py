import json

def load_json(file_path):
    """Carica un file JSON e restituisce il contenuto."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """Salva un dizionario come file JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def find_key_by_value(synonyms_dict, value):
    """Trova la chiave nel dizionario dei sinonimi che contiene il valore dato."""
    for key, values in synonyms_dict.items():
        if value.lower() in (v.lower() for v in values):
            return key
    return None

def replace_values(json_data, synonyms_dict):
    """Sostituisci i valori nel JSON in base al dizionario dei sinonimi."""
    replaced_data = {}
    for entry_id, entry in json_data.items():
        replaced_entry = {}
        for key, value in entry.items():
            replacement_key = find_key_by_value(synonyms_dict, key)
            if replacement_key:
                replaced_entry[replacement_key] = value
            else:
                replaced_entry[key] = value
        replaced_data[entry_id] = replaced_entry
    return replaced_data

# Percorsi dei file
synonyms_file = "alignment/synonym_dict.json"  # File contenente il dizionario dei sinonimi
metric_json_file = "distribution/metriche.json"   # File contenente il JSON di input
spec_json_file = "distribution/specifiche.json"   # File contenente il JSON di input
output_metric_json_file = "alignment/aligned_metriche.json" # File per il JSON risultante
output_spec_json_file = "alignment/aligned_specifiche.json" # File per il JSON risultante

# DISTRIBUZIONE DELLE METRICHE
# Caricamento dei file
synonyms_dict = load_json(synonyms_file)
metric_json = load_json(metric_json_file)

# Sostituzione dei valori
output_metric_json = replace_values(metric_json, synonyms_dict)

# Salvataggio del risultato
save_json(output_metric_json, output_metric_json_file)

print(f"Il file JSON risultante delle metriche è stato salvato in: {output_metric_json_file}")

# DISTRIBUZIONE DELLE SPECIFICHE
# Caricamento dei file
spec_json = load_json(spec_json_file)

# Sostituzione dei valori
output_spec_json = replace_values(spec_json, synonyms_dict)

# Salvataggio del risultato
save_json(output_spec_json, output_spec_json_file)

print(f"Il file JSON risultante delle specifiche è stato salvato in: {output_spec_json_file}")