"""Utility functions for notebook operations."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import nbformat
from nbformat.notebooknode import NotebookNode
from nbformat.validator import NotebookValidationError


class NotebookValidator:
    """Validates and processes Jupyter notebooks with clear, single-responsibility methods."""
    
    VALID_CELL_TYPES = {"markdown", "code", "raw"}
    
    @staticmethod
    def ensure_file_exists(notebook_path: Path) -> None:
        """Verify that the notebook file exists at the given path."""
        if not notebook_path.exists():
            raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    @staticmethod
    def ensure_file_has_ipynb_extension(notebook_path: Path) -> None:
        """Verify that the file has a .ipynb extension."""
        if notebook_path.suffix != ".ipynb":
            raise ValueError(f"File must be a Jupyter notebook (.ipynb), got: {notebook_path.suffix}")

    @staticmethod
    def parse_notebook_from_json(notebook_path: Path) -> NotebookNode:
        """Parse the notebook JSON file into a NotebookNode object."""
        try:
            return nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON in notebook file")
        except Exception as e:
            raise ValueError("Invalid JSON in notebook file")

    @staticmethod
    def ensure_notebook_structure_is_valid(notebook: NotebookNode) -> None:
        """Validate the notebook structure using nbformat.
        
        Args:
            notebook: The notebook to validate
            
        Raises:
            NotebookValidationError: If notebook structure is invalid
        """
        try:
            nbformat.validate(notebook)
        except Exception as e:
            raise NotebookValidationError(e)

    @staticmethod
    def ensure_notebook_has_cells(notebook: NotebookNode) -> None:
        """Verify that the notebook contains at least one cell."""
        if not notebook.cells:
            raise ValueError("Notebook contains no cells")

    @staticmethod
    def ensure_cell_has_required_attributes(cell: NotebookNode, cell_index: int) -> None:
        """Verify that a cell has the required attributes."""
        if not isinstance(cell, dict):
            raise ValueError(f"Cell {cell_index} is not a valid cell object")
        if "cell_type" not in cell:
            raise ValueError(f"Cell {cell_index} is missing cell_type attribute")
        if "source" not in cell:
            raise ValueError(f"Cell {cell_index} is missing source content")

    @staticmethod
    def ensure_cell_type_is_valid(cell: Dict[str, Any], cell_index: int) -> None:
        """Verify that the cell type is valid."""
        if cell["cell_type"] not in NotebookValidator.VALID_CELL_TYPES:
            raise ValueError(f"Cell {cell_index} has invalid type: {cell['cell_type']}")

    @classmethod
    def validate_cell(cls, cell: NotebookNode, cell_index: int) -> None:
        """Validate a single notebook cell."""
        cls.ensure_cell_has_required_attributes(cell, cell_index)
        cls.ensure_cell_type_is_valid(cell, cell_index)

    def validate_cell_types(self, notebook: NotebookNode) -> None:
        """
        Validate that all cells have valid types.
        
        Args:
            notebook: The notebook to validate
            
        Raises:
            NotebookValidationError: If any cell has an invalid type
        """
        valid_types = {"markdown", "code", "raw"}
        for cell in notebook.cells:
            if cell.cell_type not in valid_types:
                raise NotebookValidationError(f"Invalid cell type: {cell.cell_type}")


class NotebookReader:
    """Reads and processes Jupyter notebooks with clear, single-responsibility methods."""

    def __init__(self, validator: Optional[NotebookValidator] = None):
        """Initialize with an optional validator."""
        self.validator = validator or NotebookValidator()

    def validate_notebook_path(self, notebook_path: str) -> Path:
        """Validate the notebook file path."""
        path = Path(notebook_path)
        self.validator.ensure_file_exists(path)
        self.validator.ensure_file_has_ipynb_extension(path)
        return path

    def read_notebook(self, notebook_path: str) -> NotebookNode:
        """Read notebook from a validated path.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            NotebookNode: The validated notebook
            
        Raises:
            FileNotFoundError: If notebook file doesn't exist
            NotebookValidationError: If notebook structure is invalid
            ValueError: If notebook contains invalid JSON
        """
        try:
            notebook = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
            self.validator.ensure_notebook_structure_is_valid(notebook)
            return notebook
        except FileNotFoundError:
            raise FileNotFoundError(f"Notebook not found: {notebook_path}")
        except nbformat.reader.NotJSONError as e:
            raise ValueError("Invalid JSON in notebook file") from e
        except Exception as e:
            raise NotebookValidationError(e) from e

    def validate_notebook(self, notebook: NotebookNode) -> None:
        """Validate the notebook structure and contents."""
        self.validator.ensure_notebook_structure_is_valid(notebook)
        self.validator.ensure_notebook_has_cells(notebook)
        self.validator.validate_cell_types(notebook)

    def validate_notebook_cells(self, notebook: NotebookNode) -> None:
        """Validate all cells in the notebook."""
        for idx, cell in enumerate(notebook.cells, 1):
            self.validator.validate_cell(cell, idx)

    def read_notebook_from_path(self, notebook_path: str) -> NotebookNode:
        """Orchestrate the reading and validation of a notebook."""
        try:
            path = self.validate_notebook_path(notebook_path)
            notebook = self.read_notebook(path)
            self.validate_notebook(notebook)
            self.validate_notebook_cells(notebook)
            return notebook
        except Exception as e:
            if "Invalid JSON" in str(e):
                raise ValueError("Invalid JSON in notebook file")
            raise

    def extract_cells_content(self, notebook: NotebookNode) -> List[Dict[str, str]]:
        """Extract content and type from notebook cells."""
        return [
            {
                "type": cell.cell_type,
                "content": cell.source
            }
            for cell in notebook.cells
        ]


# Create default instances for convenience
default_validator = NotebookValidator()
default_reader = NotebookReader(default_validator)


def read_and_validate_notebook(notebook_path: str) -> NotebookNode:
    """Read and validate a notebook from a file path using default reader."""
    return default_reader.read_notebook_from_path(notebook_path)


def extract_notebook_cells(notebook_path_or_node: Union[str, NotebookNode]) -> List[Dict[str, str]]:
    """Extract cells from a notebook using default reader.
    
    Args:
        notebook_path_or_node: Either a path to a notebook file or a NotebookNode object
        
    Returns:
        List of dictionaries containing cell type and content
    """
    if isinstance(notebook_path_or_node, str):
        notebook = default_reader.read_notebook(notebook_path_or_node)
    else:
        notebook = notebook_path_or_node
    return default_reader.extract_cells_content(notebook) 