import pytest
from src.utils.doc_loader import ParsingStrategy, DocumentFactory
from pathlib import Path

# Mocking file existence would be needed for real unit tests without files
# or we use real files in a fixture.

def test_strategy_enum():
    assert ParsingStrategy.FAST_TEXT.value == "fast_text"
    assert ParsingStrategy.TABLE_HEAVY.value == "table_heavy"
    assert ParsingStrategy.LAYOUT_COMPLEX.value == "layout"

def test_loader_file_not_found():
    with pytest.raises(FileNotFoundError):
        DocumentFactory.get_loader("non_existent_file.pdf")
