import os
import json
from typing import Any, List, Tuple

def calculate_metrics(extracted_claims: List[str], ground_truth_claims: List[str]) -> Tuple[float, float, float]:
    """Calcola precisione, recall e F1-score per i claim estratti."""
    extracted_set = set(extracted_claims)
    ground_truth_set = set(ground_truth_claims)

    true_positives = len(extracted_set.intersection(ground_truth_set))
    false_positives = len(extracted_set - ground_truth_set)
    false_negatives = len(ground_truth_set - extracted_set)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def compare_folders(folder1: str, folder2: str):
    """Confronta i file JSON in due cartelle e calcola precisione, recall e F1-score."""
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    common_files = files1.intersection(files2)
    only_in_folder1 = files1 - files2
    only_in_folder2 = files2 - files1

    metrics = []

    for file_name in common_files:
        file1_path = os.path.join(folder1, file_name)
        file2_path = os.path.join(folder2, file_name)

        if file_name.endswith('.json'):
            try:
                with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
                    json1 = json.load(f1)
                    json2 = json.load(f2)

                    # Assumiamo che il contenuto sia una lista di claim
                    if isinstance(json1, list) and isinstance(json2, list):
                        extracted_claims = [str(claim) for claim in json1]
                        ground_truth_claims = [str(claim) for claim in json2]

                        precision, recall, f1_score = calculate_metrics(extracted_claims, ground_truth_claims)
                        metrics.append((precision, recall, f1_score))
                    else:
                        print(f"Formato non valido nei file: {file_name}. Devono contenere liste.")

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Errore nel leggere o analizzare il file {file_name}: {e}")

    if not metrics:
        raise ValueError("Non ci sono file JSON validi da confrontare nelle cartelle.")

    # Calcola metriche medie
    avg_precision = sum(m[0] for m in metrics) / len(metrics)
    avg_recall = sum(m[1] for m in metrics) / len(metrics)
    avg_f1_score = sum(m[2] for m in metrics) / len(metrics)

    return avg_precision, avg_recall, avg_f1_score, only_in_folder1, only_in_folder2

# Esempio di utilizzo
if __name__ == "__main__":
    folder1 = "GROUND_TRUTH"  # Sostituisci con il percorso della prima cartella
    folder2 = "JSON_CLAIMS"  # Sostituisci con il percorso della seconda cartella

    try:
        precision, recall, f1_score, missing_in_folder2, missing_in_folder1 = compare_folders(folder1, folder2)
        print(f"Precisione media: {precision:.2f}")
        print(f"Recall medio: {recall:.2f}")
        print(f"F1-Score medio: {f1_score:.2f}")
        if missing_in_folder1:
            print(f"File presenti solo in {folder2}: {missing_in_folder1}")
        if missing_in_folder2:
            print(f"File presenti solo in {folder1}: {missing_in_folder2}")
    except ValueError as e:
        print(f"Errore: {e}")
