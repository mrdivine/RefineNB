import os
from pathlib import Path

def find_ipynb_files(directory: str):
    """
    Recursively search for all .ipynb files in the given directory and print their full file paths.

    Args:
        directory (str): The root directory to search in.
    """
    directory_path = Path(directory)

    if not directory_path.is_dir():
        print(f"The provided path is not a directory: {directory}")
        return

    print(f"Searching for .ipynb files in: {directory}\n")
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".ipynb"):
                full_path = Path(root) / file
                print(full_path)

# Example usage:
if __name__ == "__main__":
    directory_to_search = "/Users/dude1/PycharmProjects/Data Analysis with ChatGPT"
    find_ipynb_files(directory_to_search)