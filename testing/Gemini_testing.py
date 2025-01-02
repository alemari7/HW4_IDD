import google.generativeai as genai
from config import API_KEY

def gemini_key_extractor(claims):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "from the following sequence of key-value pairs, tell me which ones you think are metrics. Print me just the names of the metrics and don't add any other string "

    response = model.generate_content(f"{prompt} {claims}")

    keys= response.text.split("\n")
    keys = [element for element in keys if element]
    print(f"Keys: {keys}")
    return keys
