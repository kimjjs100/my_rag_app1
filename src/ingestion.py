import os
from pathlib import Path
from src.config import MANUALS_DIR, ALARMS_DIR, VECTOR_STORE_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME
from src.utils.doc_loader import DocumentFactory, ParsingStrategy
from src.utils.logger import app_logger

# Imports
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def run_ingestion(parsing_strategy=ParsingStrategy.TABLE_HEAVY):
    app_logger.info("Starting Ingestion Process...")
    
    # 1. Initialize Embeddings
    app_logger.info(f"Loading Embedding Model: {EMBEDDING_MODEL_NAME}")
    # This will download the model to local cache if not present
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # 2. Iterate and Load Docs
    all_splits = []
    
    # Check if directory exists
    if not MANUALS_DIR.exists():
        app_logger.error(f"Manuals directory not found: {MANUALS_DIR}")
        return

    pdf_files = list(MANUALS_DIR.glob("*.pdf"))
    if not pdf_files:
        app_logger.warning(f"No PDF files found in {MANUALS_DIR}")
        return

    for pdf_path in pdf_files:
        app_logger.info(f"Processing {pdf_path.name}...")
        
        try:
            docs = DocumentFactory.load_documents(str(pdf_path), strategy=parsing_strategy)
            
            # 3. Splitting
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE, 
                chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", " ", ""]
            )
            splits = text_splitter.split_documents(docs)
            all_splits.extend(splits)
            app_logger.info(f"Created {len(splits)} chunks from {pdf_path.name}")
        except Exception as e:
            app_logger.error(f"Skipping {pdf_path.name} due to error: {e}")

    # Process Alarms Directory
    if ALARMS_DIR.exists():
        alarm_files = list(ALARMS_DIR.glob("*.pdf"))
        # You might want to support other formats for alarms here, e.g. .txt or .csv
        # For now, assuming PDFs
        if alarm_files:
            app_logger.info(f"Found {len(alarm_files)} alarm documents.")
            for alarm_path in alarm_files:
                app_logger.info(f"Processing {alarm_path.name}...")
                try:
                    docs = DocumentFactory.load_documents(str(alarm_path), strategy=parsing_strategy)
                    # Use the same splitter for now
                    splits = text_splitter.split_documents(docs)
                    all_splits.extend(splits)
                    app_logger.info(f"Created {len(splits)} chunks from {alarm_path.name}")
                except Exception as e:
                    app_logger.error(f"Skipping {alarm_path.name} due to error: {e}")

    if not all_splits:
        app_logger.info("No documents obtained. Exiting ingestion.")
        return

    # 4. Indexing (ChromaDB)
    app_logger.info(f"Indexing {len(all_splits)} chunks into ChromaDB at {VECTOR_STORE_DIR}...")
    
    # Ensure persistence directory exists
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings,
        persist_directory=str(VECTOR_STORE_DIR)
    )
    app_logger.info("Ingestion Complete.")

if __name__ == "__main__":
    # Default to PDFPlumber as requested by user
    run_ingestion(parsing_strategy=ParsingStrategy.TABLE_HEAVY)
