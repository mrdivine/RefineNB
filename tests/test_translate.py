"""Tests for notebook translation functionality."""

import pytest
from pathlib import Path
import nbformat
from nbformat.notebooknode import NotebookNode
from unittest.mock import patch, MagicMock

from src.translate import NotebookTranslator, TranslationOutput


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns predictable translations."""
    with patch('langchain_openai.ChatOpenAI') as mock:
        structured_llm = MagicMock()
        mock.return_value.with_structured_output.return_value = structured_llm
        
        def mock_translate(prompt):
            return TranslationOutput(
                translated_content="¡Hola Mundo!" if "Hello World" in prompt["content"] else prompt["content"],
                source_language="English",
                translation_notes="Test translation",
                metadata={"confidence": 0.9}
            )
        
        structured_llm.invoke.side_effect = mock_translate
        yield mock


@pytest.fixture
def sample_notebook() -> NotebookNode:
    """Create a test notebook with markdown and code cells for translation testing.
    
    Creates a simple notebook containing:
    - A markdown cell with a heading
    - A code cell with comments and a print statement
    
    The notebook is structured to test both markdown and code cell translation,
    including preservation of formatting, comments, and code functionality.
    
    Returns:
        dict: A dictionary representing a Jupyter notebook with version 4.x format,
              containing markdown and code cells with standard metadata
    """
    notebook_dict = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            }
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Hello World"
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": '''# This is a comment
print('Hello, World!')  # This prints a greeting''',
                "outputs": [],
                "execution_count": 1
            }
        ]
    }
    return nbformat.from_dict(notebook_dict)


class TestNotebookTranslator:
    """Tests for the NotebookTranslator class."""

    def test_validate_language_code(self, mock_llm):
        """Test language code validation."""
        translator = NotebookTranslator()
        
        # Valid language code should not raise error
        translator.validate_language_code("es")
        
        # Invalid language code should raise ValueError
        with pytest.raises(ValueError, match="Invalid language code"):
            translator.validate_language_code("invalid_code")

    def test_translate_markdown_cell(self, mock_llm):
        """Test markdown cell translation with structured output."""
        translator = NotebookTranslator()
        content = "# Hello World"
        translated = translator.translate_markdown_cell(content, "es")
        
        assert isinstance(translated, str)
        assert translated.startswith("#"), "Translated markdown should preserve heading format"


    def test_translate_code_cell(self, mock_llm):
        """Test code cell translation with structured output."""
        translator = NotebookTranslator()
        
        # Test code without comments - should not be translated
        code = "print('Hello, World!')"
        translated = translator.translate_cell_content(code, "code", "es")
        assert "print(" in translated  # Only verify print function name remains unchanged
        
        # Test code with comments - only comments should be translated
        code_with_comments = '''
            # This is a comment
            print('Hello, World!')  # This prints a greeting
            '''
        translated = translator.translate_cell_content(code_with_comments, "code", "es")
        assert translated != code_with_comments  # Comments should be translated
        assert translated.count("#") == 2  # Should have two comments
        assert "print(" in translated  # Print function name should remain unchanged

    def test_translate_notebook(self, mock_llm, sample_notebook):
        """Test translating a notebook with structured output."""
        translator = NotebookTranslator()
        translated_nb = translator.translate_notebook(sample_notebook, "es")
        
        assert isinstance(translated_nb, NotebookNode)
        assert len(translated_nb.cells) == len(sample_notebook.cells)

    def test_invalid_language_code(self, mock_llm):
        """Test handling of invalid language codes."""
        translator = NotebookTranslator()
        with pytest.raises(ValueError, match="Invalid language code"):
            translator.translate_cell_content("Hello", "markdown", "invalid_code")

    def test_translate_notebook_to_file(self, sample_notebook, tmp_path):
        """Test saving translated notebook to file."""
        output_path = tmp_path / "translated.ipynb"
        translator = NotebookTranslator()
        
        translator.translate_notebook_to_file(
            sample_notebook, 
            str(output_path), 
            "es"
        )
        
        assert output_path.exists()
        translated_nb = nbformat.read(output_path, as_version=4)
        assert isinstance(translated_nb, NotebookNode)
        assert len(translated_nb.cells) == len(sample_notebook.cells)
        assert any(greeting in translated_nb.cells[0].source for greeting in ["¡Hola Mundo!", "Hola Mundo"])  # Verify translation