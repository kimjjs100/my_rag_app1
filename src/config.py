import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANUALS_DIR = DATA_DIR / "manuals"
ALARMS_DIR = DATA_DIR / "alarms"
MODELS_DIR = BASE_DIR / "models"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Model Configs
# Using multilingual MiniLM for efficient memory usage on 8GB VRAM
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL_NAME = "llama3.1"
OLLAMA_BASE_URL = "http://localhost:11434"

# RAG Configs
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
RETRIEVER_K = 3
