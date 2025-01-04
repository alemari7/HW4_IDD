# Knowledge Extractor
The goal is to extract knowledge from a set of json files containing information related to tables contained in scientific papers. The extracted claims contain the name of the metric, its value and all the specifications (name and value). The claims are extracted from the HTML tables and integrated with data obtained from the context (references, captions and footnotes). Subsequently, profiling operations are performed to obtain the distribution of the metrics and specifications. Finally, an alignment of the terms is performed.

- `./sources`: Directory that contains all the input data that the code uses to extract knowledge. It contains all the papers in PDF format and for each paper an information extraction was performed producing the json files contained in the folder of the same name.

- `./sources/classifier.py`: Generates a default classification in which it associates each table id (paperID_TableID) with a default value (0). The user will classify the tables in order to process them in the most correct way

- `classification_mapping.json`: `./sources/classifier.py` output. It is used to process the table based on its typology.

## Task 1
- `./testing`: Contains all the testing code to test table types individually, the output is stored in `./testing/output_test`

- `./testing/LLM_testing`: Code used not only for testing that makes calls to the APIs of the implemented LLMs. It uses the Transformers and google.generativeai libraries to make calls to local LLMs (BERT-based models) and in the cloud to Gemini 1.5 respectively. It allows to extract additional information from the tables (captions and references) and to correctly process the tables by identifying metrics and specifications. The use of local LLMs has been completely replaced by Gemini 1.5 to obtain better performances. To use the code correctly it is necessary to create the following .py file:
  - `./config.py`: Configuration file to set your Gemini API key. The file is structured as follows
     ```python
      API_KEY = "YOUR_API_KEY"
     ```
- `./claim_extractor.py`: Code that takes care of executing task 1. It processes all the input json and launches the correct function based on the classification of the table. It executes a series of control prints, colored based on the type of table processed. It involved the use of Regex to extract the information from the tables, then replaced with Gemini. The output is stored in ./JSON_CLAIMS in the following format.
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
