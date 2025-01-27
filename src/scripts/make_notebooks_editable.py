import sys
from pathlib import Path
from typing import List
sys.path.append(str(Path(__file__).parent.parent))

from editable import NotebookEditor
from rich.console import Console
from rich.progress import track

console = Console()

def make_notebooks_editable(notebook_paths: List[str]) -> None:
    """
    Make multiple notebooks editable by applying the NotebookEditor to each path.
    
    Args:
        notebook_paths (List[str]): List of paths to Jupyter notebooks
    """
    editor = NotebookEditor()
    
    console.print("[bold green]Starting batch notebook editing process...[/]")
    
    successful = []
    failed = []
    
    for path in track(notebook_paths, description="Processing notebooks..."):
        try:
            editor.update_notebook_cells_to_editable(path)
            successful.append(path)
        except Exception as e:
            console.print(f"[bold red]Error processing {path}:[/] {str(e)}")
            failed.append((path, str(e)))
    
    # Print summary
    console.print("\n[bold]Processing Summary:[/]")
    console.print(f"[green]Successfully processed:[/] {len(successful)} notebooks")
    console.print(f"[red]Failed to process:[/] {len(failed)} notebooks")
    
    if failed:
        console.print("\n[bold red]Failed Notebooks:[/]")
        for path, error in failed:
            console.print(f"- {path}: {error}")

if __name__ == "__main__":
    # Hard-coded list of notebook paths
    NOTEBOOK_PATHS = [
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/01_Introduction_to_Data_Analysis/chapter-01-solutions/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-en-solution.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/01_Introduction_to_Data_Analysis/chapter-01-solutions/01_02_Less_Suitable_Use_Cases-solution.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/01_Introduction_to_Data_Analysis/chapter-01/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-exercise.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/01_Introduction_to_Data_Analysis/chapter-01/01_02_Less_Suitable_Use_Cases-exercise.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/02_Effective_Prompt_Design_for_Data_Analysis/chapter-02-solutions/02_01_Prompt_Design_and_Data_Analysis-solution.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/02_Effective_Prompt_Design_for_Data_Analysis/chapter-02-solutions/02_02_Prompt_Paradigms_in_Data_Interaction-solution.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/03_Data_Preparation_and_Cleaning/Notebooks/Data_Cleaning_and_Visualization_Walkthrough-solutions.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/03_Data_Preparation_and_Cleaning/Notebooks/Retail_Sales_Cleaning_Complete_Notebook_Final.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/Images_and_Tricky_Excel.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/Import_and_Clean_JSON.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/json_import.ipynb",
        "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT/05_Data_Privacy_and_Security_Considerations/Notebooks/Data Privacy and Security Considerations.ipynb"
    ]
    # NOTEBOOK_PATHS = [
    #     "/Users/dude1/PycharmProjects/RefineNB/tests/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-en-solution.ipynb"
    #     ]
    
    make_notebooks_editable(NOTEBOOK_PATHS)
