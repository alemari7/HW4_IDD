import os
import json
from bs4 import BeautifulSoup
import shutil

# Percorsi delle cartelle
INPUT_FOLDER = "sources/json"  # Cartella contenente i file JSON con le tabelle
OUTPUT_FOLDER = "JSON_CLAIMS"  # Cartella per salvare i file di output

# Funzione per caricare il mapping da file JSON
def load_mapping(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Funzione per svuotare e ricreare una cartella
def reset_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

# Funzione per gestire le tabelle di tipo 1
def process_table_type1(html_content, paper_id, table_index, output_folder):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")

        if not table:
            print("[AVVISO] Nessuna tabella trovata.")
            return

        # Estrai intestazioni
        headers = [header.text.strip() for header in table.find("tr").find_all("th")]
        rows = table.find_all("tr")[1:]  # Ignora la riga delle intestazioni

        claims = []
        count = 0

        for row in rows:
            # Estrai celle
            cells = row.find_all("th") + row.find_all("td")
            if not cells:
                continue

            # Specifiche della claim
            specifications = "{" + ",".join(
                f"|{headers[i]}, {cells[i].text.strip()}|"
                for i in range(len(headers)) if i < len(cells)
            ) + "}"

            # Estrai misura e risultato
            for col_index, cell in enumerate(cells):
                if col_index == len(headers) - 1:  # Assume che l'ultima colonna sia la misura
                    measure = headers[col_index]
                    outcome = cell.text.strip()

                    if outcome:
                        claims.append({f'Claim {count}': f'|{specifications}, {measure}, {outcome}|'})
                        count += 1

        if claims:
            # Salva le claims in un file JSON
            output_filename = f"{paper_id}_{table_index}_claims.json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w") as out_f:
                json.dump(claims, out_f, indent=4)

            print(f"[INFO] Salvato: {output_filename}")

    except Exception as e:
        print(f"[ERRORE] Errore nel processamento della tabella: {e}")

# Funzione per gestire le tabelle di tipo 2
def process_table_type2(input_file, key, value, table_index, output_folder):
    SPEC_NAME = "SPEC_NAME"
    METRIC_NAME = "METRIC_NAME"
    count = 0

    try:
        html_content = value.get("table", "")
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")

        if not table:
            print(f"[AVVISO] Nessuna tabella trovata in {input_file}, chiave {key}.")
            return

        # Estrai intestazioni
        header_row = table.find("tr")
        headers = [header.text.strip() for header in header_row.find_all(["th", "td"])]

        rows = table.find_all("tr")[1:]
        data = []

        # Processa le righe della tabella
        for row in rows:
            cells = row.find_all("th") + row.find_all("td")
            model_name = cells[0].text.strip()

            # Estrai i valori delle celle
            for col_index, cell in enumerate(cells[1:], start=1):
                value = cell.text.strip()
                if value:
                    # Crea la claim
                    data.append({
                        f'Claim {count}': f"|{{|{headers[0]}, {model_name}|, |{SPEC_NAME}, {headers[col_index]}|}}, {METRIC_NAME} , {value}|"
                    })
                    count += 1

        if data:
            # Salva le claims in un file JSON
            output_filename = f"{os.path.splitext(input_file)[0]}_{table_index}_claims.json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"[INFO] Salvato: {output_filename}")

    except Exception as e:
        print(f"[ERRORE] Errore nel processamento della tabella in {input_file}, chiave {key}: {e}")

# Funzione principale per processare i file JSON
def process_json_files(input_folder, output_folder, output_mapping):
    # Itera su tutti i file nella cartella
    for input_file in os.listdir(input_folder):
        if input_file.endswith(".json"):
            # Ottieni il nome del file senza estensione
            file_name = input_file[:-5]
            input_path = os.path.join(input_folder, input_file)
            paper_id = os.path.splitext(input_file)[0]

            with open(input_path, "r") as f:
                content = json.load(f)

            # Processa ogni "table" presente
            table_index = 1
            for key, value in content.items():
                # Ottieni il valore di mapping per la chiave corrente (file_name + key)
                mapping_value = output_mapping.get(f"{file_name}_{key}")
                print(f"Chiave: {file_name}_{key}, Valore di mapping: {mapping_value}")

                # Processa la tabella in base al valore di mapping
                if mapping_value == 1 and "table" in value:
                    process_table_type1(value["table"], paper_id, table_index, output_folder)
                    table_index += 1

                elif mapping_value == 2 and "table" in value:
                    process_table_type2(input_file, key, value, table_index, output_folder)
                    table_index += 1

                else:
                    print(f"[INFO] Saltata la chiave {key} poiché il valore di mapping è non gestito.")

if __name__ == "__main__":
    output_mapping = load_mapping("output_mapping.json")
    reset_folder(OUTPUT_FOLDER)
    process_json_files(INPUT_FOLDER, OUTPUT_FOLDER, output_mapping)
