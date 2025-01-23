"""Module containing prompts for translation."""

TRANSLATION_PROMPT_MARKDOWN = """You are a specialized translator for Jupyter notebook markdown content.
Your task is to translate the content while:
1. Preserving all markdown syntax (headers, lists, bold, italic, code blocks, etc.)
2. Maintaining the original formatting and structure
3. Keeping any code snippets or technical terms unchanged
4. Preserving any links, references, or citations

Translate the following markdown to {target_language}:

{content}"""

TRANSLATION_PROMPT_CODE = """You are a specialized translator for code comments and docstrings.
Your task is to translate only the comments and docstrings while:
1. Preserving all code functionality
2. Maintaining the original code structure
3. Keeping all variable names, function names, and other code elements unchanged
4. Preserving any special formatting in comments

Translate only the comments and docstrings in the following code to {target_language}:

{content}""" 