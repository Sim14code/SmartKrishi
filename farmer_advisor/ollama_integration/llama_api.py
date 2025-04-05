# ollama_integration/llama_api.py
import requests

def query_llm(prompt):
    url = "http://localhost:11434/api/generate"  # Ollama default port
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()['response']
