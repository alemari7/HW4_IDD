from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

import google.generativeai as genai
from config import API_KEY

def extract_metric_from_text(text_to_analyze, model_name="distilbert-base-uncased-distilled-squad"):
    """
    Utilizza un modello per il question answering per estrarre informazioni da un testo.
    
    Args:
        prompt (str): La domanda a cui rispondere.
        text_to_analyze (str): Il testo da cui estrarre la risposta.
        model_name (str): Il nome del modello Hugging Face da utilizzare.
    
    Returns:
        str: Risposta estratta dal modello.
    """

    prompt = "What metrics are mentioned in the text?"


    # Carica il tokenizer e il modello
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # Unisci il prompt con il testo da analizzare
    input_text = f"Question: {prompt}\nText: {text_to_analyze}"

    # Tokenizza il prompt e il testo
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Ottieni le risposte
    with torch.no_grad():
        outputs = model(**inputs)

    # Ottieni gli indici di inizio e fine della risposta
    start_index = outputs.start_logits.argmax()
    end_index = outputs.end_logits.argmax()

    # Decodifica la risposta
    answer_tokens = inputs.input_ids[0][start_index:end_index + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    # Ritorna la risposta estratta
    return answer.strip()


def extract_specification_from_text(text_to_analyze, spec, model_name="distilbert-base-uncased-distilled-squad"):
    """
    Utilizza un modello per il question answering per estrarre informazioni da un testo.
    
    Args:
        prompt (str): La domanda a cui rispondere.
        text_to_analyze (str): Il testo da cui estrarre la risposta.
        model_name (str): Il nome del modello Hugging Face da utilizzare.
    
    Returns:
        str: Risposta estratta dal modello.
    """

    prompt = f"What does the specification value '{spec}' represent? in the given Caption?"

    # Carica il tokenizer e il modello
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # Unisci il prompt con il testo da analizzare
    input_text = f"Question: {prompt}\nCaption: {text_to_analyze}"

    # Tokenizza il prompt e il testo
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Ottieni le risposte
    with torch.no_grad():
        outputs = model(**inputs)

    # Ottieni gli indici di inizio e fine della risposta
    start_index = outputs.start_logits.argmax()
    end_index = outputs.end_logits.argmax()

    # Decodifica la risposta
    answer_tokens = inputs.input_ids[0][start_index:end_index + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    # Ritorna la risposta estratta
    return answer.strip()


def gemini_key_extractor(claims):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "from the following sequence of key-value pairs, tell me which ones you think are metrics. Print me just the names of the metrics and don't add any other string "

    response = model.generate_content(f"{prompt} {claims}")

    keys= response.text.split("\n")
    keys = [element for element in keys if element]
    return keys
