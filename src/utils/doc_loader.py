from typing import List
from enum import Enum
from pathlib import Path

# Note: These imports depend on the packages being installed in the background.
from langchain_community.document_loaders import PyMuPDFLoader, PDFPlumberLoader
# PyMuPDF4LLMLoader might need to be imported from a specific module depending on version, 
# but usually it's available in community or via direct package if integrated.
# Langchain integration for pymupdf4llm is relatively new. 
# If not directly available in standard import, we might use the base package.
# Checking documentation, PyMuPDF4LLMLoader is in langchain_community.document_loaders.markdown
# But for safety, we'll try standard import or fallback.

try:
    from langchain_community.document_loaders import PyMuPDF4LLMLoader
except ImportError:
    # Fallback or placeholder if library structure is different in installed version
    # The requirement file has pymupdf4llm, so we might need a custom wrapper if langchain hasn't caught up.
    # But let's assume it works based on recent updates. 
    pass

from langchain_core.documents import Document
from src.utils.logger import app_logger

class ParsingStrategy(Enum):
    FAST_TEXT = "fast_text"      # PyMuPDF: Best for speed and simple text
    TABLE_HEAVY = "table_heavy"  # PDFPlumber: Best for preserving table structure
    LAYOUT_COMPLEX = "layout"    # PyMuPDF4LLM: Best for converting images/layout to Markdown

class DocumentFactory:
    @staticmethod
    def get_loader(file_path: str, strategy: ParsingStrategy = ParsingStrategy.FAST_TEXT):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        app_logger.info(f"Loading {file_path} using strategy: {strategy.value}")
        
        if strategy == ParsingStrategy.FAST_TEXT:
            return PyMuPDFLoader(file_path)
        
        elif strategy == ParsingStrategy.TABLE_HEAVY:
            return PDFPlumberLoader(file_path)
            
        elif strategy == ParsingStrategy.LAYOUT_COMPLEX:
            # PyMuPDF4LLM extracts as markdown (good for multimodal context)
            # Ensure the class is available
            if 'PyMuPDF4LLMLoader' not in globals():
                 # Use a custom wrapper if the loader class isn't imported successfully
                 # or directly use pymupdf4llm package
                 from langchain_community.document_loaders import PyMuPDFLoader
                 app_logger.warning("PyMuPDF4LLMLoader not found, falling back to PyMuPDFLoader")
                 return PyMuPDFLoader(file_path)
            return PyMuPDF4LLMLoader(file_path)
            
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    @staticmethod
    def load_documents(file_path: str, strategy: ParsingStrategy = ParsingStrategy.FAST_TEXT) -> List[Document]:
        try:
            loader = DocumentFactory.get_loader(file_path, strategy)
            documents = loader.load()
            app_logger.info(f"Successfully loaded {len(documents)} document pages from {file_path}")
            return documents
        except Exception as e:
            app_logger.error(f"Error loading document {file_path}: {e}")
            raise e
