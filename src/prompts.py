"""Module containing prompts for translation."""

TRANSLATION_PROMPT_MARKDOWN = """You are a specialized translator for markdown content, especially Jupyter notebook markdown.

Your task is to translate the provided text into {target_language} while adhering to the following rules:
1. Preserve all markdown syntax, including headers, lists, bold, italic, links, references, and citations.
2. Keep any code snippets, function names, variables, and technical terms in the original language.
3. Maintain the original structure and formatting of the content.
4. Adapt translations to the target language where applicable, ensuring cultural relevance (e.g., date formats, special terms). 
5. Make sure not to make literal translations but use idiomatic translations that are natural in the target language and keep the meaning of the original text.

IMPORTANT:
- Return the output in markdown-ready format, preserving all formatting and technical details.
- Clearly distinguish between translatable text and technical elements.

Content to translate:
{content}"""

TRANSLATION_PROMPT_CODE ="""You are a specialized translator for code comments and docstrings.
Your task is to translate ONLY the comments and docstrings in the provided code to {target_language}. 
Ensure that you:
1. Preserve all actual code exactly as it is—do not translate or alter function names, variable names, or class names.
2. Maintain all special characters, code formatting, and structure within the comments and docstrings.
3. Retain the original layout of the code.
4. Follow any language-specific rules: 
   - If translating into German, replace flags labeled "!Exercise" with "!Aufgabe."

IMPORTANT:
- Do not wrap the code in markdown code block syntax (```). 
- Return only the translated code without any additional explanation.

Code to translate:
{content}"""

