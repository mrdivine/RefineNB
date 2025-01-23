"""Tests for notebook utility functions."""

import json
from pathlib import Path
import pytest
import nbformat
from nbformat.notebooknode import NotebookNode
from nbformat.validator import NotebookValidationError

from src.utils import (
    NotebookValidator,
    NotebookReader,
    read_and_validate_notebook,
    extract_notebook_cells,
)


@pytest.fixture
def valid_notebook_path(tmp_path) -> str:
    """Create a valid sample notebook for testing.
    
    Returns:
        str: Path to a test notebook file
    """
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Test Notebook"
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "print('Hello, World!')",
                "outputs": [],
                "execution_count": None
            },
            {
                "cell_type": "raw",
                "metadata": {},
                "source": "Raw content"
            }
        ]
    }
    
    notebook = nbformat.from_dict(notebook)
    
    path = tmp_path / "test.ipynb"
    nbformat.write(notebook, path)
    return str(path)


@pytest.fixture
def invalid_json_notebook_path(tmp_path) -> str:
    """Create a notebook with invalid JSON for testing."""
    path = tmp_path / "invalid.ipynb"
    with open(path, "w") as f:
        f.write("invalid json")
    return str(path)


@pytest.fixture
def notebook_with_no_cells() -> NotebookNode:
    """Create a notebook with no cells for testing."""
    return nbformat.NotebookNode({
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": []
    })


@pytest.fixture
def notebook_with_invalid_cell_type() -> NotebookNode:
    """Create a notebook with an invalid cell type for testing."""
    return nbformat.NotebookNode({
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [{
            "cell_type": "invalid",
            "source": "test"
        }]
    })


@pytest.fixture
def notebook_with_missing_attributes() -> NotebookNode:
    """Create a notebook with cells missing required attributes."""
    return nbformat.NotebookNode({
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [{
            # Missing cell_type and source
        }]
    })


@pytest.fixture
def sample_notebook() -> NotebookNode:
    """Create a sample notebook for testing.
    
    Returns:
        NotebookNode: A notebook with markdown and code cells
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
                "source": "# Sample Markdown"
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "print('Hello, World!')",
                "outputs": [],
                "execution_count": 1
            }
        ]
    }
    notebook = nbformat.from_dict(notebook_dict)
    return notebook


@pytest.fixture
def invalid_notebook() -> NotebookNode:
    """Create an invalid notebook for testing."""
    notebook_dict = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [
            {
                "cell_type": "invalid_type",  # Invalid cell type
                "metadata": {},
                "source": "Invalid cell"
            }
        ]
    }
    # Create notebook but don't validate (it's meant to be invalid)
    return nbformat.from_dict(notebook_dict)


class TestNotebookValidator:
    """Tests for the NotebookValidator class."""

    def test_ensures_file_exists(self, tmp_path):
        """Test that validator checks file existence."""
        nonexistent_path = tmp_path / "nonexistent.ipynb"
        with pytest.raises(FileNotFoundError, match="Notebook not found"):
            NotebookValidator.ensure_file_exists(nonexistent_path)

    def test_ensures_ipynb_extension(self, tmp_path):
        """Test that validator checks for .ipynb extension."""
        wrong_ext_path = tmp_path / "test.txt"
        wrong_ext_path.touch()
        with pytest.raises(ValueError, match="must be a Jupyter notebook"):
            NotebookValidator.ensure_file_has_ipynb_extension(wrong_ext_path)

    def test_validates_notebook_structure(self, notebook_with_no_cells):
        """Test that validator checks notebook structure."""
        with pytest.raises(ValueError, match="contains no cells"):
            NotebookValidator.ensure_notebook_has_cells(notebook_with_no_cells)

    def test_validates_cell_type(self, notebook_with_invalid_cell_type):
        """Test that validator checks cell types."""
        with pytest.raises(ValueError, match="has invalid type: invalid"):
            NotebookValidator.validate_cell(notebook_with_invalid_cell_type.cells[0], 1)

    def test_validates_cell_required_attributes(self, notebook_with_missing_attributes):
        """Test that validator checks for required cell attributes."""
        with pytest.raises(ValueError, match="missing cell_type attribute"):
            NotebookValidator.validate_cell(notebook_with_missing_attributes.cells[0], 1)

    def test_parse_notebook_handles_invalid_json(self, invalid_json_notebook_path):
        """Test that parsing invalid JSON raises appropriate error."""
        with pytest.raises(ValueError, match="Invalid JSON in notebook file"):
            NotebookValidator.parse_notebook_from_json(Path(invalid_json_notebook_path))

    def test_validates_all_cell_types(self, valid_notebook_path):
        """Test that validator accepts all valid cell types."""
        notebook = nbformat.read(valid_notebook_path, as_version=nbformat.NO_CONVERT)
        for idx, cell in enumerate(notebook.cells, 1):
            NotebookValidator.validate_cell(cell, idx)  # Should not raise

    def test_ensure_notebook_structure_is_valid(self):
        """Test notebook structure validation."""
        invalid_notebook = nbformat.NotebookNode({
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {},
            "cells": [{"invalid": "structure"}]
        })
        with pytest.raises(NotebookValidationError):
            NotebookValidator.ensure_notebook_structure_is_valid(invalid_notebook)

    def test_ensure_cell_has_required_attributes_not_dict(self):
        """Test validation of non-dict cell."""
        with pytest.raises(ValueError, match="not a valid cell object"):
            NotebookValidator.ensure_cell_has_required_attributes(["not a dict"], 0)


class TestNotebookReader:
    """Tests for the NotebookReader class."""

    def test_successfully_reads_valid_notebook(self, valid_notebook_path):
        """Test reading a valid notebook."""
        reader = NotebookReader()
        notebook = reader.read_notebook_from_path(valid_notebook_path)
        assert isinstance(notebook, NotebookNode)
        assert len(notebook.cells) == 3  # markdown, code, and raw cells
        assert notebook.cells[0].cell_type == "markdown"
        assert notebook.cells[1].cell_type == "code"
        assert notebook.cells[2].cell_type == "raw"

    def test_validate_notebook_path_returns_path_object(self, valid_notebook_path):
        """Test that validate_notebook_path returns a Path object."""
        reader = NotebookReader()
        path = reader.validate_notebook_path(valid_notebook_path)
        assert isinstance(path, Path)
        assert path.suffix == ".ipynb"

    def test_read_notebook_returns_notebook_node(self, valid_notebook_path):
        """Test that read_notebook returns a NotebookNode."""
        reader = NotebookReader()
        path = reader.validate_notebook_path(valid_notebook_path)
        notebook = reader.read_notebook(path)
        assert isinstance(notebook, NotebookNode)

    def test_validate_notebook_checks_structure(self, notebook_with_no_cells):
        """Test that validate_notebook checks notebook structure."""
        reader = NotebookReader()
        with pytest.raises(ValueError, match="contains no cells"):
            reader.validate_notebook(notebook_with_no_cells)

    def test_validate_notebook_cells_checks_all_cells(self, notebook_with_invalid_cell_type):
        """Test that validate_notebook_cells checks all cells."""
        reader = NotebookReader()
        with pytest.raises(ValueError, match="has invalid type: invalid"):
            reader.validate_notebook_cells(notebook_with_invalid_cell_type)

    def test_extracts_cells_content(self, valid_notebook_path):
        """Test extracting cell content from a notebook."""
        reader = NotebookReader()
        notebook = reader.read_notebook_from_path(valid_notebook_path)
        cells = reader.extract_cells_content(notebook)
        
        assert len(cells) == 3
        assert cells[0]["type"] == "markdown"
        assert cells[0]["content"] == "# Test Notebook"
        assert cells[1]["type"] == "code"
        assert cells[1]["content"] == "print('Hello, World!')"
        assert cells[2]["type"] == "raw"
        assert cells[2]["content"] == "Raw content"

    def test_fails_on_invalid_json(self, invalid_json_notebook_path):
        """Test handling of invalid JSON."""
        reader = NotebookReader()
        with pytest.raises(ValueError, match="Invalid JSON in notebook file"):
            reader.read_notebook_from_path(invalid_json_notebook_path)

    def test_custom_validator_integration(self, valid_notebook_path):
        """Test that reader works with a custom validator."""
        custom_validator = NotebookValidator()
        reader = NotebookReader(validator=custom_validator)
        notebook = reader.read_notebook_from_path(valid_notebook_path)
        assert isinstance(notebook, NotebookNode)

    def test_validate_notebook_structure_is_valid(self):
        """Test validation of notebook structure through reader."""
        reader = NotebookReader()
        invalid_notebook = nbformat.NotebookNode({
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {},
            "cells": [{"invalid": "structure"}]
        })
        with pytest.raises(NotebookValidationError):
            reader.validate_notebook(invalid_notebook)

    @pytest.mark.parametrize("invalid_path", [
        "nonexistent.txt",  # Wrong extension
        "missing.ipynb",    # Non-existent file
    ])
    def test_read_notebook_from_path_invalid_paths(self, invalid_path):
        """Test reading from invalid paths."""
        reader = NotebookReader()
        with pytest.raises((ValueError, FileNotFoundError)):
            reader.read_notebook_from_path(invalid_path)


class TestConvenienceFunctions:
    """Tests for the convenience functions."""

    def test_read_and_validate_notebook(self, valid_notebook_path):
        """Test the read_and_validate_notebook convenience function."""
        notebook = read_and_validate_notebook(valid_notebook_path)
        assert isinstance(notebook, NotebookNode)
        assert len(notebook.cells) == 3

    def test_extract_notebook_cells(self, valid_notebook_path):
        """Test the extract_notebook_cells convenience function."""
        notebook = read_and_validate_notebook(valid_notebook_path)
        cells = extract_notebook_cells(notebook)
        assert len(cells) == 3
        assert all(isinstance(cell, dict) for cell in cells)
        assert all({"type", "content"} <= cell.keys() for cell in cells)
        assert all(cell["type"] in NotebookValidator.VALID_CELL_TYPES for cell in cells) 