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
        html_content = value["table"]
        caption = value["caption"]

        # Analizza l'HTML
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")

        # Controlla se la tabella è valida
        if not table:
            print(f"[AVVISO] Nessuna tabella trovata in {input_file}, chiave {key}.")
            return table_index

        # Estrai intestazioni e righe della tabella
        rows = table.find_all("tr")  # Estrai tutte le righe della tabella

        if len(rows) < 3:  # Assicurati che ci siano almeno 3 righe (intestazione + valori)
            print(f"[AVVISO] La tabella in {input_file}, chiave {key}, non ha abbastanza righe.")
            return table_index

        # La prima riga è l'intestazione (nomi delle specifiche)
        header_row = rows[1]
        header_cells = header_row.find_all("th") + header_row.find_all("td")  # Intestazione può contenere sia <th> che <td>
        header_keys = [cell.text.strip() for cell in header_cells]

        # La seconda riga è la riga dei valori
        value_row = rows[2]
        value_cells = value_row.find_all("th") + value_row.find_all("td")

        # Verifica che la seconda riga abbia lo stesso numero di celle della prima riga
        if len(value_cells) != len(header_keys):
            print(f"[AVVISO] Il numero di celle nella seconda riga non corrisponde alle intestazioni in {input_file}, chiave {key}.")
            # Gestisci la discrepanza tra celle della seconda riga e intestazioni
            if len(value_cells) < len(header_keys):
                # Aggiungi celle vuote se ci sono meno celle
                value_cells.extend([''] * (len(header_keys) - len(value_cells)))
            else:
                # Se ci sono più celle, prendi solo quelle necessarie
                value_cells = value_cells[:len(header_keys)]

        # Estrai le metriche e i dati dalla tabella
        data = []
        for row_index in range(3, len(rows)):  # Inizia dalla quarta riga in poi (dopo l'intestazione e i valori)
            row = rows[row_index]
            cells = row.find_all("th") + row.find_all("td")
            if len(cells) < 1:
                continue

            metric_name = cells[0].text.strip()  # La prima colonna è il nome della metrica

            # Estrai i valori per ogni specifica (prima riga come intestazione, seconda riga come valore)
            for col_index, spec_value_cell in enumerate(value_cells[1:], start=1):  # Salta la prima cella (nome della metrica)
                spec_name = header_keys[col_index]  # Nome della specifica (es. Score, Error, ecc.)
                spec_value = cells[col_index].text.strip()  # Valore della specifica

                if spec_value:  # Solo celle non vuote
                    claim = {
                        f"Claim {count}": f"|{{|{spec_name}, {spec_value}|}}, {metric_name}, {spec_value}|"
                    }
                    count += 1
                    # Salva i claim nella lista dei dati
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
                # Saltare la chiave se il valore di mapping non è 3
                print(f"[INFO] Saltata la chiave {key} poiché il valore di mapping non è 3.")
