# Knowledge Extractor
The goal is to extract knowledge from a set of json files containing information related to tables contained in scientific papers. The extracted claims contain the name of the metric, its value and all the specifications (name and value). The claims are extracted from the HTML tables and integrated with data obtained from the context (references, captions and footnotes). Subsequently, profiling operations are performed to obtain the distribution of the metrics and specifications. Finally, an alignment of the terms is performed.

- `./sources`: Directory that contains all the input data that the code uses to extract knowledge. It contains all the papers in PDF format and for each paper an information extraction was performed producing the json files contained in the folder of the same name.

- `./sources/classifier.py`: Generates a default classification in which it associates each table id (paperID_TableID) with a default value (0). The user will classify the tables in order to process them in the most correct way

- `classification_mapping.json`: output of `./sources/classifier.py` . It is used to process the table based on its typology.

## Task 1: Claim Extraction
Task 1 focuses on extracting structured claims from tables in scientific papers. The extracted claims include metrics, their values, and associated specifications derived from tables and their context (e.g., captions, references, and footnotes). This task uses advanced natural language processing (NLP) techniques, including local and cloud-based language models, to achieve precise and reliable results.
- `./testing`: Contains all the testing code to test table types individually, the output is stored in `./testing/output_test`

- `./testing/LLM_testing`: Code used not only for testing that makes calls to the APIs of the implemented LLMs. It uses the Transformers and google.generativeai libraries to make calls to local LLMs (BERT-based models) and in the cloud to Gemini 1.5 respectively. It allows to extract additional information from the tables (captions and references) and to correctly process the tables by identifying metrics and specifications. The use of local LLMs has been completely replaced by Gemini 1.5 to obtain better performances. To use the code correctly it is necessary to create the following .py file:
  - `./config.py`: Configuration file to set your Gemini API key. The file is structured as follows
     ```python
      API_KEY = "YOUR_API_KEY"
     ```
- `./claim_extractor.py`: Code that takes care of executing task 1. It processes all the input json and launches the correct function based on the classification of the table. It executes a series of control prints, colored based on the type of table processed. It involved the use of Regex to extract the information from the tables, then replaced with Gemini. The output is stored in `./JSON_CLAIMS` in the following format.
    ```json
     [
        {
          "Claim 0": "|{|Dataset, WMT-16|,|Lang. Pair, DE-EN|}, # Trn.+Vld., 4,551,054|"
        },
        {
          "Claim 1": "|{|Dataset, WMT-16|,|Lang. Pair, DE-EN|}, # Test, 2,999|"
        }
    ]
    ```
- `./format_json.py`: Convert json claims to a more readable format. The output is stored in  `./JSON_CLAIMS_CONVERTED`
  ```json
  [
       {
          "0": {
              "specifications": {
                  "0": {
                      "name": "Dataset",
                      "value": "WMT-16"
                  },
                  "1": {
                      "name": "Lang. Pair",
                      "value": "DE-EN"
                  }
              },
              "Measure": "# Trn.+Vld.",
              "Outcome": "4,551,054"
          }
        },
        {
          "1": {
              "specifications": {
                  "0": {
                      "name": "Dataset",
                      "value": "WMT-16"
                  },
                  "1": {
                      "name": "Lang. Pair",
                      "value": "DE-EN"
                  }
              },
              "Measure": "# Test",
              "Outcome": "2,999"
          }
      }
  ]
  ```
## Task 2: Profiling
The purpose of Task 2 is to analyze the claims extracted from the tables and generate comprehensive profiling data. This task provides statistical insights into the claims by calculating various distributions and averages. The results are stored in structured formats for easy interpretation and further analysis.
A profiling of the extracted claims is produced, containing the following distributions:
- Distribution of metrics
- Distribution of specifications names
- Distribution of values ​​for each name for each specification
- Average of the values ​​associated with each metric
The results are stored in `./NAME_PROFILING.csv`.

- `./distribution/dict_generator.py`: Produces two dictionaries in json format:
  - `./distribution/metrics.json`: Extracts all metrics from claims and associates them with corresponding output values
  - `./distribution/specifications.json`: Extracts all specifications from claims and associates them with corresponding output values.
- `./distribution/profiling.py`: From the previously extracted dictionaries, calculate the distributions required by the task

## Task 3: Alignment
The goal of Task 3 is to standardize and unify the terminology used across extracted claims, ensuring consistency in metrics and specifications. This task identifies synonyms, aligns names to their canonical forms, and recalculates distributions based on aligned data. The result is a cleaned, unified dataset ready for further analysis or reporting.
Allows you to align the names of metrics and specifications to join words that have the same meaning (e.g. same stem).
- `./alignment/alignment.py`: allows you to unify the values ​​associated with each metric or specification. The association allows you to unify the position of each metric or specification as follows "paperID_tableID_claimID_specification_ID". The output produced is stored in `./alignment/aligned_output.json`.
- `./alignment/synonym_dict_generator.py`: It allows to build a synonym dictionary. It uses an LLM model (**All-Mini**). It associates to each key an array of strings that are traceable to the key. An array like the following is produced and stored in `./alignment/synonym_dict.json`.
  ```json
  "model": [
        "model",
        "models"
    ],
    "wait-k": [
        "wait-k"
    ],
    "dataset": [
        "data set",
        "dataset"
    ]
  ```
- `./alignment/merge_alignment.py`: The previously aligned values ​​are merged using the newly computed dictionary. The output is stored in `./alignment/merged_fields_output.json`.
- `./alignment/dict_distribution.py`: It allows to build, starting from the distributions obtained in task 2, a dictionary of the distributions of aligned metrics and specifications using the synonym dictionary. The extracted dictionaries will be used again by `./distribution/profiling.py` to compute the profiling of task 2 again, but after the alignment of the names. Output is stored in `./alignment/NAME_PROFILING_ALIGNED.csv`

## Running tools
The following shell files allow you to automatically execute the python codes for the execution of tasks 1, 2 and 3 respectively: `./task1.sh`, `./task2.sh`, `./task3.sh`.
