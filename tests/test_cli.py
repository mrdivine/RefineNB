"""Tests for the command line interface."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import nbformat
import json

from src.cli import main, translate, output

@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()

@pytest.fixture
def sample_notebook(tmp_path):
    """Create a sample notebook file for testing."""
    notebook_path = tmp_path / "test.ipynb"
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"editable": False},
                "source": "# Test Notebook"
            },
            {
                "cell_type": "code",
                "metadata": {"editable": False},
                "source": "print('Hello World')",
                "outputs": [],
                "execution_count": None
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }
    notebook_path.write_text(json.dumps(notebook_content))
    return notebook_path

def test_main_help(runner):
    """Test the main CLI help message."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "RefineNB - Translate and extract content from Jupyter notebooks" in result.output

def test_translate_command_help(runner):
    """Test the translate command help message."""
    result = runner.invoke(main, ["translate", "--help"])
    assert result.exit_code == 0
    assert "Translate notebook content to the specified language" in result.output

def test_output_command_help(runner):
    """Test the output command help message."""
    result = runner.invoke(main, ["output", "--help"])
    assert result.exit_code == 0
    assert "Extract notebook content to JSON format" in result.output

def test_prepare_command_help(runner):
    """Test the prepare command help message."""
    result = runner.invoke(main, ["prepare", "--help"])
    assert result.exit_code == 0
    assert "Prepare a notebook for editing" in result.output

def test_translate_missing_required_options(runner):
    """Test translate command fails when required options are missing."""
    result = runner.invoke(main, ["translate"])
    assert result.exit_code != 0
    assert "Missing option" in result.output

def test_output_missing_required_options(runner):
    """Test output command fails when required options are missing."""
    result = runner.invoke(main, ["output"])
    assert result.exit_code != 0
    assert "Missing option" in result.output

def test_prepare_missing_required_options(runner):
    """Test prepare command fails when required options are missing."""
    result = runner.invoke(main, ["prepare"])
    assert result.exit_code != 0
    assert "Missing option" in result.output

def test_translate_nonexistent_notebook(runner):
    """Test translate command with nonexistent notebook."""
    result = runner.invoke(main, ["translate", "-nb", "nonexistent.ipynb", "-l", "DE"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_output_nonexistent_notebook(runner):
    """Test output command with nonexistent notebook."""
    result = runner.invoke(main, ["output", "-nb", "nonexistent.ipynb", "-o", "output.json"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_prepare_nonexistent_notebook(runner):
    """Test prepare command with nonexistent notebook."""
    result = runner.invoke(main, ["prepare", "-nb", "nonexistent.ipynb"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_translate_command_not_implemented(runner, sample_notebook):
    """Test translate command raises NotImplementedError."""
    result = runner.invoke(main, ["translate", "-nb", str(sample_notebook), "-l", "DE"])
    assert result.exit_code != 0
    assert isinstance(result.exception, NotImplementedError)
    assert "Translation functionality not yet implemented" in str(result.exception)

def test_output_command_executes_successfully(runner, sample_notebook):
    """Test output command executes successfully."""
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["output", "-nb", str(sample_notebook), "-o", "output.json"])
        assert result.exit_code == 0
        assert "Extracting from notebook:" in result.output
        assert "Successfully extracted content to:" in result.output
        assert Path("output.json").exists()

def test_prepare_command_executes_successfully(runner, sample_notebook):
    """Test that the prepare command successfully makes cells editable."""
    result = runner.invoke(main, ["prepare", "-nb", str(sample_notebook)])
    print(result.output)  # For debugging
    assert result.exit_code == 0
    assert "Preparing notebook for editing:" in result.output
    assert "Successfully prepared notebook for editing" in result.output
    
    # Verify the notebook was modified correctly
    notebook = nbformat.read(sample_notebook, as_version=nbformat.NO_CONVERT)
    for cell in notebook.cells:
        assert cell.metadata.get("editable", False) is True
        assert cell.metadata.get("deletable", False) is True 