#!/bin/bash

# Esegui il primo script Python
python3 alignment/alignment.py
# Verifica se il primo script è stato eseguito correttamente
if [ $? -eq 0 ]; then
    echo "alignment.py completato con successo"
else
    echo "Errore nell'esecuzione di alignment.py"
    exit 1
fi

# Esegui il secondo script Python
python3 alignment/merge_alignment.py
if [ $? -eq 0 ]; then
    echo "merge_profiling.py completato con successo"
else
    echo "Errore nell'esecuzione di merge_profiling.py"
    exit 1
fi

# Aggiungi altri script secondo necessità
