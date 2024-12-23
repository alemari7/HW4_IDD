import os
import json
from bs4 import BeautifulSoup
import shutil

# Percorsi delle cartelle
input_folder = "sources/json"  # Cartella contenente i file JSON con le tabelle
output_folder = "JSON_CLAIMS"  # Cartella per salvare i file di output

# Svuota e ricrea la cartella di output
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Elimina la cartella e il suo contenuto
os.makedirs(output_folder, exist_ok=True)  # Ricrea la cartella vuota

# Funzione per estrarre claims da una tabella HTML
def extract_claims_from_table(html_content, table_id, paper_id):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")

    if not table:
        return []

    headers = [header.text.strip() for header in table.find("tr").find_all("th")]
    rows = table.find_all("tr")[1:]  # Ignora la riga delle intestazioni

    claims = []

    for row_index, row in enumerate(rows):
        cells = row.find_all("th") + row.find_all("td")
        if not cells:
            continue

        specifications = {str(i): {"name": headers[i], "value": cells[i].text.strip()} for i in range(len(headers)) if i < len(cells)}

        # Identifica la misura ("Measure") e l'outcome per ogni riga
        for col_index, cell in enumerate(cells):
            if col_index == len(headers) - 1:  # Assume che l'ultima colonna sia la misura
                measure = headers[col_index]
                outcome = cell.text.strip()

                if outcome:
                    claim = {
                        "specifications": specifications,
                        "Measure": measure,
                        "Outcome": outcome
                    }
                    claims.append(claim)

    return claims

# Processa tutti i file JSON nella cartella di input
for input_file in os.listdir(input_folder):
    if input_file.endswith(".json"):
        input_path = os.path.join(input_folder, input_file)
        paper_id = os.path.splitext(input_file)[0]

        with open(input_path, "r") as f:
            content = json.load(f)

        table_index = 1
        for key, value in content.items():
            if "table" in value:
                try:
                    html_content = value["table"]
                    claims = extract_claims_from_table(html_content, table_index, paper_id)

                    if claims:
                        output_filename = f"{paper_id}_{table_index}_claims.json"
                        output_path = os.path.join(output_folder, output_filename)

                        with open(output_path, "w") as out_f:
                            json.dump(claims, out_f, indent=4)

                        print(f"[INFO] Salvato: {output_filename}")

                    table_index += 1

                except Exception as e:
                    print(f"[ERRORE] Errore nel processamento della tabella in {input_file}, chiave {key}: {e}")
                    continue
