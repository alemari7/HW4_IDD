import os
import json
from bs4 import BeautifulSoup
import shutil
import re

# Percorsi delle cartelle
input_folder = "sources/json"  # Cartella contenente i file JSON con le tabelle
output_folder = "testing/output_test"  # Cartella per salvare i file di output

# Carica il file di mapping
with open("classification_mapping.json", "r") as f:
    output_mapping = json.load(f)

# Svuota e ricrea la cartella di output
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Elimina la cartella e il suo contenuto
os.makedirs(output_folder, exist_ok=True)  # Ricrea la cartella vuota

def extract_keys_with_numeric_values(input_list):
    # Espressione regolare per identificare valori numerici (inclusi numeri decimali, numeri tra parentesi e in notazione scientifica)
    pattern = r"^[\d,\.]+(?:\s?\([\d,\.]+\))?|^[\d,\.]+e[-+]?\d+"

    # Lista per memorizzare le chiavi associate a valori numerici
    keys = []

    # Itera sulla lista di dizionari
    for item in input_list:
        for key, value in item.items():
            # Verifica se il valore è numerico o segue il pattern
            if isinstance(value, str) and re.match(pattern, value):
                keys.append(key)

    return keys


# Funzione per estrarre claims da una tabella HTML
def func1(html_content, table_id, paper_id):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    count = 0

    if not table:
        return []

    headers = [header.text.strip() for header in table.find("tr").find_all("th")]
    rows = table.find_all("tr")[1:]  # Ignora la riga delle intestazioni

    claims = []
    keys = []

    for row_index, row in enumerate(rows):
        cells = row.find_all("th") + row.find_all("td")
        if not cells:
            continue

        specificationsRaw = []

        # Ciclo attraverso gli indici delle intestazioni (headers)
        for i in range(len(headers)):
            # Controlla che l'indice sia valido anche per le celle (cells)
            if i < len(cells):
                specificationsRaw.append({headers[i]: cells[i].text.strip()})

        # Estrai le chiavi associate ai valori numerici

        if (keys == []):
            keys = extract_keys_with_numeric_values(specificationsRaw)


        # Costruisci la stringa di specifiche senza le chiavi estratte, ma con i valori delle specifiche
        specifications = "{"
        for spec in specificationsRaw:
            for key, value in spec.items():
                if key not in keys:
                    specifications += f"|{key}, {value}|,"
        specifications = specifications[:-1] + "}"

        if specifications == "}":
            specifications = "{"
            for spec in specificationsRaw:
                for key, value in spec.items():
                    specifications += f"|{key}, {value}|,"
            specifications = specifications[:-1] + "}"
            keys = []

        for col_index, cell in enumerate(cells):
            if col_index == len(headers) - 1 or (headers[col_index] in keys):  # Assume che l'ultima colonna sia la misura
                measure = headers[col_index]
                outcome = cell.text.strip()

                if outcome:
                    claim = {f'Claim {count}': f'|{specifications}, {measure}, {outcome}|'}
                    count += 1
                    claims.append(claim)

    return claims

# Processa tutti i file JSON nella cartella di input
for input_file in os.listdir(input_folder):
    if input_file.endswith(".json"):
        file_name = input_file[:-5]
        input_path = os.path.join(input_folder, input_file)
        paper_id = os.path.splitext(input_file)[0]

        with open(input_path, "r") as f:
            content = json.load(f)

        table_index = 1
        for key, value in content.items():
            # MAPPING CHECK - Estrai il valore associato alla chiave
            mapping_value = output_mapping.get(file_name + '_' + key, None)  # Cerca il valore nel file output_mapping.json
            #print(f"Chiave: {file_name + '_' + key}, Valore di mapping: {mapping_value}")
            
                        # Esegui il codice solo se il valore di mapping è "1"
            if mapping_value == 1 and "table" in value:
                # Chiamata alla funzione func1 che gestisce l'elaborazione
                try:
                    html_content = value["table"]
                    claims = func1(html_content, table_index, paper_id)

                    if claims:
                        output_filename = f"{paper_id}_{table_index}_claims.json"
                        output_path = os.path.join(output_folder, output_filename)

                        with open(output_path, "w") as out_f:
                            json.dump(claims, out_f, indent=4)

                        print(f"[INFO] Salvato: {output_filename}")

                except Exception as e:
                    print(f"[ERRORE] Errore nel processamento della tabella in {input_file}, chiave {key}: {e}")
                    continue
            else:
                # Saltare la chiave se il valore di mapping non è gestit0
                #print(f"[INFO] Saltata la chiave {key} poiché il valore di mapping è non gestito.")
                None

            table_index += 1  
