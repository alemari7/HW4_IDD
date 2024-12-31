from sentence_transformers import SentenceTransformer, util
import json
import re

input_filename = 'alignment/aligned_output'
output_filename = 'alignment/synonym_dict.json'


def group_synonyms(input_array):
    # Normalizzazione dei termini per evitare che "data set" e "dataset" vengano trattati come separati
    input_array = [re.sub(r'\s+', ' ', term.strip().lower()) for term in input_array]

    # Calcolare gli embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Puoi usare anche modelli più adatti per sinonimi, tipo 'paraphrase-MiniLM-L6-v2'
    embeddings = model.encode(input_array)

    # Calcolo della matrice di similarità
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    # Clusterizzazione in base alla similarità (es. soglia più bassa)
    threshold = 0.45  # Abbassando la soglia rispetto a prima
    clusters = []
    visited = set()

    for i in range(len(input_array)):
        if i not in visited:
            cluster = [i]
            for j in range(i + 1, len(input_array)):
                if j not in visited and similarity_matrix[i][j] > threshold:
                    cluster.append(j)
                    visited.add(j)
            clusters.append(cluster)
            visited.update(cluster)

    # Creazione del dizionario di sinonimi
    synonym_dict = {}
    for cluster in clusters:
        # Trova il rappresentante per ogni cluster
        representative = input_array[cluster[0]]
        if representative not in synonym_dict:
            synonym_dict[representative] = [input_array[i] for i in cluster]
        else:
            synonym_dict[representative].extend([input_array[i] for i in cluster])

    # Gestione dei duplicati: ogni termine deve essere presente in un solo gruppo
    final_dict = {}
    used_terms = set()  # Per tenere traccia dei termini già assegnati
    added_terms = set()  # Per evitare di aggiungere un gruppo più di una volta

    for key, values in synonym_dict.items():
        # Rimuoviamo i duplicati all'interno del cluster
        values = list(set(values))
        
        # Ordina per frequenza per determinare quale gruppo rappresenta meglio i termini
        sorted_values = sorted(values, key=lambda v: values.count(v), reverse=True)

        # Aggiungi solo se il gruppo non è già stato aggiunto
        for value in sorted_values:
            if value not in used_terms:
                final_dict[value] = sorted_values
                used_terms.update(sorted_values)
                break

    # Aggiungi gli elementi che non sono in nessun cluster
    for term in input_array:
        if term not in used_terms:
            final_dict[term] = [term]

    return final_dict

# Supponiamo che il JSON sia in un file chiamato 'aligned_output.json'
with open(f'{input_filename}.json', 'r') as file:
    data = json.load(file)

# Estrai le chiavi di "aligned_names" ed escludi quelle numeriche
aligned_names_keys = [key for key in data.get("aligned_names", {}).keys() if not key.isdigit()]
print("Chiavi di aligned_names (non numeriche):", aligned_names_keys)

# Raggruppa le chiavi in sinonimi
synonym_dict = group_synonyms(aligned_names_keys)

# Salva il dizionario in un file JSON
with open(output_filename, 'w') as outfile:
    json.dump(synonym_dict, outfile, indent=4)

print("Dizionario di sinonimi:")
print(json.dumps(synonym_dict, indent=4))
