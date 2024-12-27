import os
import json
from bs4 import BeautifulSoup
import shutil

# Percorsi delle cartelle
input_folder = "sources/json"  # Cartella contenente i file JSON con le tabelle
output_folder = "output_test"  # Cartella per salvare i file di output
os.makedirs(output_folder, exist_ok=True)

# Carica il file di mapping
with open("output_mapping.json", "r") as f:
    output_mapping = json.load(f)

# Svuota e ricrea la cartella di output
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Elimina la cartella e il suo contenuto
os.makedirs(output_folder, exist_ok=True)  # Ricrea la cartella vuota

# Funzione per estrarre il claim dalla tabella
def extract_claims_from_table(input_file, key, value, table_index):
    count = 0
    try:
        html_content = value["table"]
        caption = value["caption"]

        # Analizza l'HTML
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")

        # Controlla se la tabella è valida
        if not table:
            print(f"[AVVISO] Nessuna tabella trovata in {input_file}, chiave {key}.")
            return table_index

        # Estrai intestazioni
        header_row = table.find("tr")  # Prima riga della tabella
        headers = header_row.find_all(["th", "td"])  # Cerca sia <th> che <td> nella riga delle intestazioni
        header_keys = [header.text.strip() for header in headers]

        # Estrai le righe della tabella
        rows = table.find_all("tr")[1:]  # Ignora la riga delle intestazioni

        data = []
        
        # Processa le righe della tabella
        for row_index, row in enumerate(rows):
            cells = row.find_all("th") + row.find_all("td")  # Combina <th> e <td>
            
            # Controlla che la riga abbia abbastanza celle per la corrispondenza
            if len(cells) < len(header_keys):
                print(f"[AVVISO] La riga {row_index + 1} in {input_file}, chiave {key}, ha meno celle rispetto alle intestazioni.")
                continue  # Salta la riga se non ha abbastanza celle
            
            metric_name = cells[0].text.strip()  # Prima colonna: nome della metrica

            # Estrai i valori per ogni specifica dalla riga
            for col_index, cell in enumerate(cells[1:], start=1):  # Salta la prima colonna (nome della metrica)
                if col_index >= len(header_keys):
                    break  # Salta se l'indice supera il numero di intestazioni
                spec_name = header_keys[col_index]  # Nome della specifica (es. Score, Error, ecc.)
                spec_value = cell.text.strip()  # Valore della specifica

                if spec_value:  # Solo celle non vuote
                    claim = {
                        f"Claim {count}": f"|{{|{spec_name}, {spec_value}|}}, {metric_name}, {spec_value}|"
                    }
                    count += 1
                    data.append(claim)

        # Salva il risultato in un file JSON
        output_filename = f"{os.path.splitext(input_file)[0]}_{table_index}_claims.json"
        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[INFO] Salvato: {output_filename}")
        table_index += 1

    except Exception as e:
        print(f"[ERRORE] Errore nel processamento della tabella in {input_file}, chiave {key}: {e}")
        return table_index

    return table_index

# Processa tutti i file JSON nella cartella di input
# Effettua una distinzione di processamento in base alla classificazione sulle tabelle
for input_file in os.listdir(input_folder):
    if input_file.endswith(".json"):
        file_name = input_file[:-5]
        input_path = os.path.join(input_folder, input_file)

        # Leggi il contenuto del file JSON
        with open(input_path, "r") as f:
            content = json.load(f)

        # Processa ogni "table" presente
        table_index = 1
        for key, value in content.items():
            # MAPPING CHECK - Estrai il valore associato alla chiave
            mapping_value = output_mapping.get(file_name + '_' + key, None)  # Cerca il valore nel file output_mapping.json
            if mapping_value == 3 and "table" in value:
                # Esegui la funzione di estrazione claims
                table_index = extract_claims_from_table(input_file, key, value, table_index)
            else:
                # Saltare la chiave se il valore di mapping non è 0
                print(f"[INFO] Saltata la chiave {key} poiché il valore di mapping non è 0.")
