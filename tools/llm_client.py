import requests
import os

def call_llm(prompt: str, system: str = "") -> str:
    """Direct OpenRouter call — use when needed outside Band agents"""
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "google/gemma-4-31b-it:free",
            "messages": messages,
            "max_tokens": 1000
        }
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"LLM Error: {response.status_code}"