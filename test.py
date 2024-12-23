import os
import json
from bs4 import BeautifulSoup

# Percorsi delle cartelle
input_folder = "sources/json"  # Cartella contenente i file JSON con le tabelle
output_folder = "output"  # Cartella per salvare i file di output
os.makedirs(output_folder, exist_ok=True)

SPEC_NAME = "SPEC_NAME"
METRIC_NAME = "METRIC_NAME"

# Processa tutti i file JSON nella cartella di input
for input_file in os.listdir(input_folder):
    if input_file.endswith(".json"):
        input_path = os.path.join(input_folder, input_file)

        # Leggi il contenuto del file JSON
        with open(input_path, "r") as f:
            content = json.load(f)

        # Processa ogni "table" presente
        table_index = 1
        for key, value in content.items():
            if "table" in value:
                try:
                    html_content = value["table"]

                    # Analizza l'HTML
                    data = []
                    soup = BeautifulSoup(html_content, "html.parser")
                    table = soup.find("table")

                    # Controlla se la tabella è valida
                    if not table:
                        print(f"[AVVISO] Nessuna tabella trovata in {input_file}, chiave {key}.")
                        continue

                    # Estrarre intestazioni e righe
                    headers = table.find("tr").find_all("th")
                    header_keys = [header.text.strip() for header in headers]

                    rows = table.find_all("tr")[1:]  # Ignora la riga delle intestazioni

                    # Processa le righe della tabella
                    for row_index, row in enumerate(rows):
                        cells = row.find_all("th") + row.find_all("td")
                        model_name = cells[0].text.strip()

                        for col_index, cell in enumerate(cells[1:], start=1):
                            value = cell.text.strip()
                            if value:  # Solo celle non vuote
                                claim = {
                                    str(row_index * len(cells) + col_index - 1): f"|{{|{header_keys[0]}, {model_name}|, |{SPEC_NAME}, {header_keys[col_index]}|}}, {METRIC_NAME} , {value}|"
                                }
                                data.append(claim)

                    # Salva il risultato in un file JSON
                    output_filename = f"{os.path.splitext(input_file)[0]}_{table_index}_claims.json"
                    output_path = os.path.join(output_folder, output_filename)

                    with open(output_path, "w") as f:
                        json.dump(data, f, indent=4)

                    print(f"[INFO] Salvato: {output_filename}")
                    table_index += 1

                except Exception as e:
                    print(f"[ERRORE] Errore nel processamento della tabella in {input_file}, chiave {key}: {e}")
                    continue
