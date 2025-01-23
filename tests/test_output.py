"""Tests for notebook output functionality."""

import json
import pytest
import nbformat
from nbformat.notebooknode import NotebookNode

from src.output import NotebookOutputWriter, extract_notebook_to_json


@pytest.fixture
def sample_notebook() -> NotebookNode:
    """Create a sample notebook for testing."""
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
                "metadata": {"tags": ["header"]},
                "source": "# Test Notebook"
            },
            {
                "cell_type": "code",
                "metadata": {"tags": ["example"]},
                "source": "print('Hello, World!')",
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": "Hello, World!\n"
                    }
                ],
                "execution_count": 1
            },
            {
                "cell_type": "raw",
                "metadata": {},
                "source": "Raw content"
            }
        ]
    }
    return nbformat.from_dict(notebook_dict)


@pytest.fixture
def sample_notebook_path(tmp_path, sample_notebook) -> str:
    """Create a sample notebook file for testing."""
    path = tmp_path / "test.ipynb"
    nbformat.write(sample_notebook, path)
    return str(path)


class TestNotebookOutputWriter:
    """Tests for the NotebookOutputWriter class."""

    def test_extract_cells_content(self, sample_notebook):
        """Test extracting cell content."""
        writer = NotebookOutputWriter(sample_notebook)
        cells = writer.extract_cells_content()
        
        assert len(cells) == 2  # Only markdown and code cells
        
        # Check markdown cell
        assert cells[0]["type"] == "markdown"
        assert cells[0]["content"] == "# Test Notebook"
        
        # Check code cell
        assert cells[1]["type"] == "code"
        assert cells[1]["content"] == "print('Hello, World!')"

        # Verify only type and content are present
        for cell in cells:
            assert set(cell.keys()) == {"type", "content"}

    def test_write_to_json(self, sample_notebook, tmp_path):
        """Test writing output to JSON file."""
        output_path = tmp_path / "output.json"
        writer = NotebookOutputWriter(sample_notebook)
        writer.write_to_json(str(output_path))
        
        assert output_path.exists()
        with open(output_path) as f:
            cells = json.load(f)
        
        assert isinstance(cells, list)
        assert len(cells) == 2  # Only markdown and code cells
        assert all(set(cell.keys()) == {"type", "content"} for cell in cells)
        assert all(cell["type"] in {"markdown", "code"} for cell in cells)

    def test_write_to_json_with_invalid_path(self, sample_notebook, tmp_path):
        """Test writing to an invalid path."""
        invalid_path = tmp_path / "nonexistent" / "output.json"
        writer = NotebookOutputWriter(sample_notebook)
        
        with pytest.raises(ValueError, match="Failed to write output"):
            writer.write_to_json(str(invalid_path))


def test_extract_notebook_to_json_creates_output_directory(sample_notebook_path, tmp_path):
    """Test that extract_notebook_to_json creates output directory if needed."""
    output_path = tmp_path / "subdir" / "output.json"
    extract_notebook_to_json(sample_notebook_path, str(output_path))
    
    assert output_path.exists()
    with open(output_path) as f:
        cells = json.load(f)
    assert len(cells) == 2  # Only markdown and code cells
    assert all(set(cell.keys()) == {"type", "content"} for cell in cells)
    assert all(cell["type"] in {"markdown", "code"} for cell in cells)


def test_extract_notebook_to_json_with_nonexistent_notebook(tmp_path):
    """Test extracting from a nonexistent notebook."""
    with pytest.raises(FileNotFoundError):
        extract_notebook_to_json(
            "nonexistent.ipynb",
            str(tmp_path / "output.json")
        )


def test_extract_cells_content():
    """Test that only code and markdown cells are extracted."""
    # Create a mock notebook with different cell types
    notebook = NotebookNode({
        'cells': [
            {
                'cell_type': 'code',
                'source': 'print("Hello")',
                'metadata': {},
                'outputs': []
            },
            {
                'cell_type': 'markdown',
                'source': '# Header',
                'metadata': {}
            },
            {
                'cell_type': 'raw',
                'source': 'raw content',
                'metadata': {}
            }
        ]
    })

    writer = NotebookOutputWriter(notebook)
    cells = writer.extract_cells_content()

    # Verify the results
    assert len(cells) == 2  # Only code and markdown cells
    assert cells[0] == {'type': 'code', 'content': 'print("Hello")'}
    assert cells[1] == {'type': 'markdown', 'content': '# Header'} 