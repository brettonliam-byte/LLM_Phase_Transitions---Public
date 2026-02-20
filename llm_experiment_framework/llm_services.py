import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the root of the repository
# We look for .env in the parent directory of 'llm_experiment_framework'
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to standard search if root .env not found
    load_dotenv()

def get_openrouter_response(prompt, model, temperature):
    """
    Sends a prompt to the OpenRouter API and gets a response.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def get_openai_response(prompt, model, temperature):
    """
    Sends a prompt to the OpenAI API and gets a response.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def get_anthropic_response(prompt, model, temperature):
    """
    Sends a prompt to the Anthropic API and gets a response.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["content"][0]["text"]

def get_google_response(prompt, model, temperature):
    """
    Sends a prompt to the Google Gemini API and gets a response.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    # Google's model names often don't have the 'models/' prefix in short form, 
    # but the API endpoint needs it if not present.
    if not model.startswith("models/"):
        model_path = f"models/{model}"
    else:
        model_path = model

    url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": temperature,
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    # Error handling for Google's specific response format
    res_json = response.json()
    if "candidates" not in res_json or not res_json["candidates"]:
        if "error" in res_json:
            raise Exception(f"Google API Error: {res_json['error']['message']}")
        raise Exception(f"Google API Error: No candidates returned. Response: {res_json}")
        
    return res_json["candidates"][0]["content"]["parts"][0]["text"]

def get_ollama_response(prompt, model, temperature):
    """
    Sends a prompt to the Ollama API and gets a response.
    """
    # Try multiple common env var names for Ollama
    endpoint = os.getenv("OLLAMA_API_ENDPOINT")
    if not endpoint:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        # If base_url ends with /v1, strip it for the /api/generate endpoint
        if base_url.endswith("/v1"):
            base_url = base_url[:-3]
        elif base_url.endswith("/v1/"):
            base_url = base_url[:-4]
        
        # Ensure it doesn't end with a slash before appending
        base_url = base_url.rstrip("/")
        endpoint = f"{base_url}/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(endpoint, json=data)
    response.raise_for_status()
    return response.json()["response"]

def get_lmstudio_response(prompt, model, temperature):
    """
    Sends a prompt to the LM Studio API and gets a response.
    """
    endpoint = os.getenv("LMSTUDIO_API_ENDPOINT", "http://localhost:1234/v1/chat/completions")
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# A dictionary to map service names to their functions
SERVICE_MAP = {
    "openrouter": get_openrouter_response,
    "openai": get_openai_response,
    "anthropic": get_anthropic_response,
    "google": get_google_response,
    "ollama": get_ollama_response,
    "lmstudio": get_lmstudio_response,
}

def get_llm_response(service, prompt, model, temperature):
    """
    A generic function to call the correct LLM service.
    """
    service = service.lower()
    if service not in SERVICE_MAP:
        raise ValueError(f"Unknown service: {service}. Supported: {list(SERVICE_MAP.keys())}")

    # For some services, we might want to keep the full model name or strip it
    # Google likes 'gemini-1.5-pro', Anthropic likes 'claude-3-opus-20240229'
    return SERVICE_MAP[service](prompt, model, temperature)