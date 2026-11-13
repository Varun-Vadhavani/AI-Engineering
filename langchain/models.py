import os
from dotenv import load_dotenv

load_dotenv()

def get_model():
    mode = os.getenv("MODEL_MODE", "local")   # default to the free one

    if mode == "local":
        from langchain_ollama import ChatOllama
        return ChatOllama(model="qwen2.5-coder:7b")

    if mode == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-3.6-flash")

    raise ValueError(f"Unknown MODEL_MODE: {mode}")