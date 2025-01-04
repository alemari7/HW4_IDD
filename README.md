# Knowledge Extractor

The goal of this project is to extract knowledge from a set of JSON files containing information about tables in scientific papers. The extracted claims include the name of the metric, its value, and all related specifications (name and value). Claims are extracted from HTML tables and enriched with contextual data (e.g., references, captions, and footnotes). Subsequently, profiling operations are performed to analyze the distribution of metrics and specifications. Finally, term alignment is carried out to standardize the terminology.

## Directory Structure

- `./sources`: Directory containing all input data used by the code to extract knowledge. It includes:
  - PDFs of the papers.
  - JSON files generated for each paper as part of the information extraction process.

- `./sources/classifier.py`: Generates a default classification by associating each table ID (`paperID_TableID`) with a default value (0). Users can classify the tables to process them appropriately.

- `classification_mapping.json`: Output file from `./sources/classifier.py`. It is used to process tables based on their classification.

---

## Task 1: Claim Extraction

Task 1 focuses on extracting structured claims from tables in scientific papers. The claims include metrics, their values, and associated specifications derived from tables and their contexts (e.g., captions, references, and footnotes). Advanced natural language processing (NLP) techniques are employed, including local and cloud-based language models, to achieve precise and reliable results.

### Components

- `./testing`: Contains test scripts to validate individual table types. Outputs are stored in `./testing/output_test`.

- `./testing/LLM_testing`: 
  - Contains code for testing that calls APIs of implemented language models (LLMs).
  - Utilizes the `Transformers` and `google.generativeai` libraries for local (BERT-based models) and cloud (Gemini 1.5) LLMs.
  - The use of local LLMs has been replaced with Gemini 1.5 for improved performance.
  - **Setup:** Create a `./config.py` file to configure the Gemini API key:
    ```python
    API_KEY = "YOUR_API_KEY"
    ```

- `./claim_extractor.py`: Processes all input JSON files and executes the appropriate functions based on table classification. Outputs are stored in `./JSON_CLAIMS` in the following format:
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

- `./format_json.py`: Converts JSON claims to a more readable format. Outputs are stored in `./JSON_CLAIMS_CONVERTED`:
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

---

## Task 2: Profiling

Task 2 analyzes the extracted claims to generate comprehensive profiling data. It provides statistical insights into claims by calculating distributions and averages. The results are stored in structured formats for easy interpretation and further analysis.

### Components

- Profiling includes:
  - Distribution of metrics.
  - Distribution of specification names.
  - Distribution of values for each specification.
  - Average values associated with each metric.

- Outputs are saved in `./NAME_PROFILING.csv`.

- `./distribution/dict_generator.py`: Produces JSON dictionaries:
  - `./distribution/metrics.json`: Maps metrics to their respective values.
  - `./distribution/specifications.json`: Maps specifications to their respective values.

- `./distribution/profiling.py`: Computes distributions from the extracted dictionaries.

---

## Task 3: Alignment

Task 3 standardizes and unifies terminology across extracted claims, ensuring consistency in metrics and specifications. Synonyms are identified, terms are aligned to canonical forms, and distributions are recalculated based on the aligned data. The result is a unified dataset ready for further analysis or reporting.

### Components

- `./alignment/alignment.py`: Aligns values for metrics and specifications and associates them with unique identifiers (`paperID_tableID_claimID_specification_ID`). Outputs are saved in `./alignment/aligned_output.json`.

- `./alignment/synonym_dict_generator.py`: Builds a synonym dictionary using an LLM (**All-Mini**). Outputs are saved in `./alignment/synonym_dict.json`:
    ```json
    {
        "model": ["model", "models"],
        "wait-k": ["wait-k"],
        "dataset": ["data set", "dataset"]
    }
    ```

- `./alignment/merge_alignment.py`: Merges aligned values using the synonym dictionary. Outputs are saved in `./alignment/merged_fields_output.json`.

- `./alignment/dict_distribution.py`: Updates distributions from Task 2 using aligned data. Outputs are saved in `./alignment/NAME_PROFILING_ALIGNED.csv`.

---

## Running the Tools

Shell scripts are provided to automate the execution of Python codes for each task:
- `./task1.sh`: Executes Task 1.
- `./task2.sh`: Executes Task 2.
- `./task3.sh`: Executes Task 3.
