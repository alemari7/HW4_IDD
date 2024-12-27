from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

def extract_information_from_text(text_to_analyze, model_name="distilbert-base-uncased-distilled-squad"):
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
