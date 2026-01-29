# Offline RAG System for Ship Maintenance

This project provides an offline Retrieval Augmented Generation (RAG) system for ship sensors and alarm monitoring.

## Prerequisites
- **Python 3.10+**
- **NVIDIA GPU** (Recommended for Local LLM & Embedding)
- **Ollama** installed and running with `llama3.1` model.

## Installation

1. **Clone the repository** (if not already done).

2. **Setup Virtual Environment**:
   ```bash
   # Create virtual environment
   python3 -m pip install --user virtualenv
   python3 -m virtualenv .venv
   
   # Activate virtual environment
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Ingestion (Build Knowledge Base)
Place your PDF manuals in `data/manuals/`.

```bash
# Default strategy (Table Heavy for manuals - Recommended)
python main.py ingest

# Faster text-only strategy
python main.py ingest --strategy fast_text

# Layout preservation (Markdown)
python main.py ingest --strategy layout
```

### 2. Analysis (Run RAG)
Ensure Ollama is running (`ollama serve`).

```bash
python main.py analyze --code ALARM-001 --temp 45.5 --pressure 102.0
```

## Configuration
- Modify `src/config.py` to change model names or paths.
- Logs are available in `logs/` directory.

## Directory Structure
- `data/manuals`: Place PDF files here.
- `vector_store`: ChromaDB storage (auto-generated).
- `models`: HuggingFace model cache.
- `logs`: Application and debug logs.
