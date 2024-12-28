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

# Funzione per estrarre i claim dalla tabella
def extract_claims_from_table(input_file, key, value, table_index):
    count = 0
    try:
        html_content = value.get("table")
        caption = value.get("caption", "")

        # Analizza l'HTML
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")

        # Controlla se la tabella è valida
        if not table:
            print(f"[AVVISO] Nessuna tabella trovata in {input_file}, chiave {key}.")
            return table_index

        # Estrai righe della tabella
        rows = table.find_all("tr")  # Estrai tutte le righe della tabella

        if len(rows) < 3:  # Assicurati che ci siano almeno intestazione e righe di dati
            print(f"[AVVISO] La tabella in {input_file}, chiave {key}, non ha abbastanza righe.")
            return table_index

        # Estrai intestazioni dalla seconda riga
        header_row = rows[1]
        header_cells = header_row.find_all(["th", "td"])
        header_keys = [cell.text.strip() for cell in header_cells]

        # Processa righe dei dati
        data = []
        for row_index, row in enumerate(rows[2:], start=3):  # Dalla terza riga in poi
            cells = row.find_all(["th", "td"])
            if len(cells) != len(header_keys):
                print(f"[AVVISO] Numero di celle diverso dalle intestazioni in {input_file}, riga {row_index}.")
                continue

            metric_name = cells[0].text.strip()  # La prima cella è il nome della metrica
            for col_index, cell in enumerate(cells[1:], start=1):  # Salta la prima cella
                spec_name = header_keys[col_index]  # Nome della specifica
                spec_value = cell.text.strip()  # Valore della specifica

                if spec_value:  # Solo celle non vuote
                    claim = {
                        f"Claim {count}": f"|{{|{spec_name}, {spec_value}|}}, {metric_name}, {spec_value}|"
                    }
                    data.append(claim)
                    count += 1

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
for input_file in os.listdir(input_folder):
    if input_file.endswith(".json"):
        file_name = input_file[:-5]
        input_path = os.path.join(input_folder, input_file)

        # Leggi il contenuto del file JSON
        with open(input_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        # Processa ogni "table" presente
        table_index = 1
        for key, value in content.items():
            # MAPPING CHECK - Estrai il valore associato alla chiave
            mapping_value = output_mapping.get(f"{file_name}_{key}", None)  # Cerca il valore nel file output_mapping.json
            if mapping_value == 3 and "table" in value:
                # Esegui la funzione di estrazione claims
                table_index = extract_claims_from_table(input_file, key, value, table_index)
            else:
                print(f"[INFO] Saltata la chiave {key} poiché il valore di mapping non è 3.")
