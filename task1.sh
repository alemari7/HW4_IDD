#!/bin/bash

# Esegui il primo script Python
python3 claim_extractor.py
# Verifica se il primo script è stato eseguito correttamente
if [ $? -eq 0 ]; then
    echo "claim_extractor.py completato con successo"
else
    echo "Errore nell'esecuzione di claim_extractor.py"
    exit 1
fi


# Aggiungi altri script secondo necessità
