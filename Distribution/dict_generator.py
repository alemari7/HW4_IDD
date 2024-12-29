import os
import json
import re

# Directory contenente i file JSON
INPUT_DIR = "JSON_CLAIMS"
OUTPUT_DIR = "Distribution"

# Inizializzo i dizionari
specifiche_dict = {}
metriche_dict = {}

# Funzione per processare una singola "claim"
def process_claim(claim_key, claim_value):
    # Regex per estrarre il blocco all'interno di {| ... |}
    specifiche_match = re.search(r"\{\|(.+?)\|\}", claim_value)
    if specifiche_match:
        specifiche_blocco = specifiche_match.group(1)
        # Divido il blocco in coppie chiave-valore e costruisco un dizionario separato per ogni specifica
        specifiche = re.findall(r"([^,]+),([^|]+)", specifiche_blocco)
        for i, (k, v) in enumerate(specifiche, start=1):
            k = k.replace("|", "")
            specifiche_dict[f"{claim_key}_{i}"] = {k.strip(): v.strip()}

    # Regex per estrarre la metrica e il suo valore (fuori dalle graffe)
    metriche_match = re.search(r"\}\s*,\s*([^,]+)\s*,\s*([^|]+)\|", claim_value)
    if metriche_match:
        metrica, valore = metriche_match.groups()
        metriche_dict[claim_key] = {metrica.strip(): valore.strip()}

# Scorro tutti i file nella directory
count = 0
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(INPUT_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Carico il JSON
            # Itero su ogni elemento della lista
            for item in data:
                for claim_key, claim_value in item.items():
                    count += 1
                    process_claim(count, claim_value)


# Salvo i risultati in file JSON
with open(f"{OUTPUT_DIR}/specifiche.json", "w", encoding="utf-8") as spec_file:
    json.dump(specifiche_dict, spec_file, indent=4, ensure_ascii=False)

with open(f"{OUTPUT_DIR}/metriche.json", "w", encoding="utf-8") as metric_file:
    json.dump(metriche_dict, metric_file, indent=4, ensure_ascii=False)
