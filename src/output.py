"""Module for extracting and saving notebook content to JSON."""

import json
from pathlib import Path
from typing import Dict, List

import nbformat
from nbformat.notebooknode import NotebookNode

from src.utils import NotebookValidator


class NotebookOutputWriter:
    """Handles extracting and writing notebook content to JSON files."""

    def __init__(self, notebook: NotebookNode):
        """Initialize with a validated notebook."""
        self.notebook = notebook

    def extract_cells_content(self) -> List[Dict[str, str]]:
        """Extract only code and markdown cells content.
        
        Returns:
            List of dictionaries containing cell type and content for
            code and markdown cells only.
        """
        ALLOWED_CELL_TYPES = {'code', 'markdown'}
        return [
            {
                "type": cell["cell_type"],
                "content": cell["source"]
            }
            for cell in self.notebook.cells
            if cell["cell_type"] in ALLOWED_CELL_TYPES
        ]

    def write_to_json(self, output_path: str) -> None:
        """Write the extracted content to a JSON file.
        
        Args:
            output_path: Path where the JSON file should be saved.
            
        Raises:
            ValueError: If the output path is invalid or write fails.
        """
        try:
            cells = self.extract_cells_content()
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cells, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Failed to write output to {output_path}: {str(e)}")


def extract_notebook_to_json(notebook_path: str, output_path: str) -> None:
    """Extract notebook content to a JSON file.
    
    Args:
        notebook_path: Path to the input notebook file.
        output_path: Path where the JSON file should be saved.
        
    Raises:
        FileNotFoundError: If the notebook file doesn't exist.
        ValueError: If the notebook is invalid or writing fails.
    """
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read and validate the notebook
    validator = NotebookValidator()
    notebook = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
    validator.ensure_notebook_structure_is_valid(notebook)
    
    # Create writer and save output
    writer = NotebookOutputWriter(notebook)
    writer.write_to_json(output_path) 