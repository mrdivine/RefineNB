from nbformat.notebooknode import NotebookNode
import nbformat
from src.utils import read_and_validate_notebook
class NotebookEditor:
    """Makes notebook cells editable by modifying their metadata."""
    
    def set_cell_metadata_editable(self, cell: NotebookNode) -> None:
        """Make a single cell editable by setting metadata."""
        if 'metadata' not in cell:
            cell.metadata = {}
        cell.metadata['editable'] = True
        cell.metadata['deletable'] = True
        # Remove any locks
        cell.metadata.pop('locked', None)
    
    def convert_notebook_cells_to_editable(self, notebook: NotebookNode) -> NotebookNode:
        """Make all cells in a notebook editable.
        
        Args:
            notebook: The notebook to modify
            
        Returns:
            NotebookNode: The modified notebook with all cells editable
        """
        # Create a copy to avoid modifying the original
        prepared_nb = nbformat.from_dict(notebook.copy())
        
        for cell in prepared_nb.cells:
            self.set_cell_metadata_editable(cell)
            
        return prepared_nb
    
    def update_notebook_cells_to_editable(self, notebook_path: str) -> None:
        """Read a notebook file, make all cells editable, and save back to the same file.
        
        Args:
            notebook_path: Path to the notebook file
        """
        # Use existing utilities to read and validate
        notebook = read_and_validate_notebook(notebook_path)
        
        # Prepare for editing
        prepared_nb = self.convert_notebook_cells_to_editable(notebook)
        
        # Save back to the same file
        nbformat.write(prepared_nb, notebook_path)


if __name__ == "__main__":
    # Simple test on a notebook
    test_notebook_path = "tests/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-en-solution.ipynb"
    try:
        editor = NotebookEditor()
        editor.update_notebook_cells_to_editable(test_notebook_path)
        print(f"Successfully made notebook {test_notebook_path} editable")
    except FileNotFoundError:
        print(f"Error: Test notebook not found at {test_notebook_path}")
    except Exception as e:
        print(f"Error preparing notebook: {str(e)}")

