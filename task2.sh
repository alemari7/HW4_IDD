#!/bin/bash

# Esegui il primo script Python
# GENERA UN DIZIONARIO CHE ASSOCIA METRICHE A VALORI e SPEFICICHE A VALORI
python3 distribution/dict_generator.py
# Verifica se il primo script è stato eseguito correttamente
if [ $? -eq 0 ]; then
    echo "dict_generator.py completato con successo"
else
    echo "Errore nell'esecuzione di dict_generator.py"
    exit 1
fi

# Esegui il secondo script Python
# ESEGUE IL PROFILING DELLE DISTRIBUZIONI SULLA BASE DEL DIZIONARIO GENERATO
# esegue anche il profiling allineato per la task 3
python3 distribution/profiling.py
if [ $? -eq 0 ]; then
    echo "profiling.py completato con successo"
else
    echo "Errore nell'esecuzione di profiling.py"
    exit 1
fi
