"""Module for translating notebook content."""

from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
import nbformat
from nbformat.notebooknode import NotebookNode

from src.utils import NotebookValidator
from src.prompts import TRANSLATION_PROMPT_MARKDOWN, TRANSLATION_PROMPT_CODE


class TranslationOutput(BaseModel):
    """Structured output for translations."""
    translated_content: str = Field(description="The translated content, preserving all code and markdown formatting")
    source_language: Optional[str] = Field(default=None, description="Detected source language")
    translation_notes: Optional[str] = Field(default=None, description="Any notes about the translation")
    metadata: Dict = Field(
        default_factory=dict,
        description="Additional metadata about the translation (e.g., confidence scores, alternative translations)"
    )


class NotebookTranslator:
    """Class for translating notebook content."""
    
    def __init__(self):
        """Initialize the translator."""
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-4")
        self.structured_llm = self.llm.with_structured_output(TranslationOutput)
        self.supported_languages = {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }

    def validate_language_code(self, target_lang: str) -> None:
        """
        Validate that the provided language code is supported.
        
        Args:
            target_lang: The target language code to validate
            
        Raises:
            ValueError: If the language code is not supported
        """
        if target_lang not in self.supported_languages:
            raise ValueError(f"Invalid language code: {target_lang}")

    def is_markdown_cell(self, cell_type: str) -> bool:
        """
        Check if the cell is a markdown cell.
        
        Args:
            cell_type: The type of cell to check
            
        Returns:
            bool: True if cell is markdown type
        """
        return cell_type == "markdown"

    def is_code_cell(self, cell_type: str) -> bool:
        """
        Check if the cell is a code cell.
        
        Args:
            cell_type: The type of cell to check
            
        Returns:
            bool: True if cell is code type
        """
        return cell_type == "code"

    def has_translatable_code_content(self, content: str) -> bool:
        """
        Check if code cell contains comments or docstrings that need translation.
        
        Args:
            content: The cell content to check
            
        Returns:
            bool: True if content contains comments or docstrings
        """
        return any(marker in content for marker in ['#', '"""', "'''"])

    def translate_markdown_cell(self, content: str, target_lang: str) -> str:
        """
        Translate markdown cell content with structured output.
        
        Args:
            content: The markdown content to translate
            target_lang: The target language code
            
        Returns:
            str: Translated markdown content
        """
        prompt = TRANSLATION_PROMPT_MARKDOWN.format(
            target_language=self.supported_languages[target_lang],
            content=content
        )
        result = self.structured_llm.invoke(prompt)
        return result.translated_content

    def translate_code_cell(self, content: str, target_lang: str) -> str:
        """
        Translate code cell content with structured output.
        
        Args:
            content: The code content to translate
            target_lang: The target language code
            
        Returns:
            str: Translated code content
        """
        if not self.has_translatable_code_content(content):
            return content
            
        prompt = TRANSLATION_PROMPT_CODE.format(
            target_language=self.supported_languages[target_lang],
            content=content
        )
        result = self.structured_llm.invoke(prompt)
        return result.translated_content

    def translate_cell_content(self, content: str, cell_type: str, target_lang: str) -> str:
        """
        Translate cell content to target language.
        
        Args:
            content: The cell content to translate
            cell_type: The type of cell ('markdown' or 'code')
            target_lang: The target language code
            
        Returns:
            str: Translated content
        """
        self.validate_language_code(target_lang)

        if self.is_markdown_cell(cell_type):
            return self.translate_markdown_cell(content, target_lang)
        elif self.is_code_cell(cell_type):
            return self.translate_code_cell(content, target_lang)
        return content  # Skip other cell types

    def translate_notebook(self, notebook: NotebookNode, target_lang: str) -> NotebookNode:
        """
        Translate a notebook to target language.
        
        Args:
            notebook: The notebook to translate
            target_lang: The target language code
            
        Returns:
            Translated notebook as NotebookNode
        """
        validator = NotebookValidator()
        validator.ensure_notebook_structure_is_valid(notebook)
        
        # Create a deep copy to avoid modifying the original
        translated_nb = nbformat.from_dict(notebook.copy())
        
        for cell in translated_nb.cells:
            cell.source = self.translate_cell_content(
                cell.source,
                cell.cell_type,
                target_lang
            )
            
        return translated_nb

    def translate_notebook_to_file(
        self,
        notebook: NotebookNode,
        output_path: str,
        target_lang: str
    ) -> None:
        """
        Translate notebook and save to file.
        
        Args:
            notebook: The notebook to translate
            output_path: Path to save translated notebook
            target_lang: The target language code
        """
        translated_nb = self.translate_notebook(notebook, target_lang)
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write translated notebook
        nbformat.write(translated_nb, output_path) 