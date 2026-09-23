from langchain_community.llms import Ollama
import os

# Allow overriding model via environment variable
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def get_llm(model=OLLAMA_MODEL):
    return Ollama(model=model, base_url=OLLAMA_BASE_URL)

def generate_completion(prompt_text: str, model=OLLAMA_MODEL):
    llm = get_llm(model)
    return llm.invoke(prompt_text)
