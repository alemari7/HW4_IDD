import os
import json
from typing import List, Tuple
from difflib import SequenceMatcher

# Definizione della soglia globale
THRESHOLD = 0.9

def normalize_claim(claim: str) -> str:
    """Normalizza un claim rimuovendo spazi extra e standardizzando il formato."""
    return claim.strip().replace(" ", "").lower()

def calculate_similarity(claim1: str, claim2: str) -> float:
    """Calcola la similarità tra due stringhe usando SequenceMatcher."""
    return SequenceMatcher(None, claim1, claim2).ratio()

def calculate_metrics(extracted_claims: List[str], ground_truth_claims: List[str]) -> Tuple[float, float, float]:
    """Calcola precisione, recall e F1-score per i claim estratti considerando la soglia di similarità globale."""
    extracted_set = set(map(normalize_claim, extracted_claims))
    ground_truth_set = set(map(normalize_claim, ground_truth_claims))

    true_positives = 0
    matched_ground_truth = set()

    for extracted in extracted_set:
        for ground_truth in ground_truth_set:
            if ground_truth not in matched_ground_truth and calculate_similarity(extracted, ground_truth) >= THRESHOLD:
                true_positives += 1
                matched_ground_truth.add(ground_truth)
                break

    false_positives = len(extracted_set) - true_positives
    false_negatives = len(ground_truth_set) - len(matched_ground_truth)

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
    different_files = []

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
                        extracted_claims = [normalize_claim(str(claim)) for claim in json1]
                        ground_truth_claims = [normalize_claim(str(claim)) for claim in json2]

                        # Usa la variabile globale THRESHOLD
                        precision, recall, f1_score = calculate_metrics(extracted_claims, ground_truth_claims)
                        metrics.append((precision, recall, f1_score))

                        if precision < 1.0 or recall < 1.0:
                            different_files.append(file_name)
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

    return avg_precision, avg_recall, avg_f1_score, only_in_folder1, only_in_folder2, different_files

# Esempio di utilizzo
if __name__ == "__main__":
    folder1 = "GROUND_TRUTH"  # Sostituisci con il percorso della prima cartella
    folder2 = "JSON_CLAIMS"  # Sostituisci con il percorso della seconda cartella

    try:
        precision, recall, f1_score, missing_in_folder2, missing_in_folder1, different_files = compare_folders(folder1, folder2)
        print(f"Precisione media: {precision:.2f}")
        print(f"Recall medio: {recall:.2f}")
        print(f"F1-Score medio: {f1_score:.2f}")

        if missing_in_folder1:
            print(f"File presenti solo in {folder2}: {missing_in_folder1}")
        if missing_in_folder2:
            print(f"File presenti solo in {folder1}: {missing_in_folder2}")
    except ValueError as e:
        print(f"Errore: {e}")
