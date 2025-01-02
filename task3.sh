#!/bin/bash

# Esegui il primo script Python
# CODICE PER L'ALLINEAMENTO DEI DATI
python3 alignment/alignment.py
# Verifica se il primo script è stato eseguito correttamente
if [ $? -eq 0 ]; then
    echo "alignment.py completato con successo"
else
    echo "Errore nell'esecuzione di alignment.py"
    exit 1
fi

# Esegui il secondo script Python
# GENERA IL DIZIONARIO DEI SINONIMI
python3 alignment/synonym_dict_generator.py
if [ $? -eq 0 ]; then
    echo "synonym_dict_generator completato con successo"
else
    echo "Errore nell'esecuzione di synonym_dict_generator"
    exit 1
fi

# Esegui il terzo script Python
# ESEGUE IL MERGE DEI DATI DI ALLINEAMENTO
python3 alignment/merge_alignment.py
if [ $? -eq 0 ]; then
    echo "merge_profiling.py completato con successo"
else
    echo "Errore nell'esecuzione di merge_profiling.py"
    exit 1
fi

# Esegui il quarto script Python
# GENERA LA DISTRIBUZIONE DEI DATI SU DATI ALLINEATI
python3 alignment/dict_distribution.py
if [ $? -eq 0 ]; then
    echo "dict_distribution completato con successo"
else
    echo "Errore nell'esecuzione di dict_distribution"
    exit 1
fi

# Esegui il quinto script Python
# ESEGUE IL PROFILING DEI DATI ALLINEATI e non
python3 distribution/profiling.py
if [ $? -eq 0 ]; then
    echo "profiling completato con successo"
else
    echo "Errore nell'esecuzione di profiling"
    exit 1
fi