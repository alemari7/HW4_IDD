#!/bin/bash

# Esegui il primo script Python
python3 distribution/dict_generator.py
# Verifica se il primo script è stato eseguito correttamente
if [ $? -eq 0 ]; then
    echo "dict_generator.py completato con successo"
else
    echo "Errore nell'esecuzione di dict_generator.py"
    exit 1
fi

# Esegui il secondo script Python
python3 distribution/profiling.py
if [ $? -eq 0 ]; then
    echo "profiling.py completato con successo"
else
    echo "Errore nell'esecuzione di profiling.py"
    exit 1
fi

# Aggiungi altri script secondo necessità
