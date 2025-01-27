# Future Steps
https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/
Memory Agent

# RefineNB

A CLI tool for translating and extracting content from Jupyter notebooks.

## Features

- Translate notebook content (markdown and code cells) to different languages
- Extract notebook content to JSON format
- Make notebook cells editable and deletable

## Installation

```bash
pip install -e .
```

## Usage

### Translate a notebook

```bash
refinenb translate --notebook-path path/to/notebook.ipynb --language DE
```

### Extract notebook content

```bash
refinenb output --notebook-path path/to/notebook.ipynb --output path/to/output.json
```

### Make notebook cells editable

```bash
refinenb make-editable --notebook-path path/to/notebook.ipynb
```
This command modifies the notebook in place, making all cells editable and deletable.

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT 

# Notebooks in Course 1
```shell
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/01_Introduction_to_Data_Analysis/chapter-01-solutions/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-en-solution.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/01_Introduction_to_Data_Analysis/chapter-01-solutions/01_02_Less_Suitable_Use_Cases-solution.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/01_Introduction_to_Data_Analysis/chapter-01/01_01_Overview_of_LLM_Capabilities_in_Data_Analysis-exercise.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/01_Introduction_to_Data_Analysis/chapter-01/01_02_Less_Suitable_Use_Cases-exercise.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/02_Effective_Prompt_Design_for_Data_Analysis/chapter-02-solutions/02_01_Prompt_Design_and_Data_Analysis-solution.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/02_Effective_Prompt_Design_for_Data_Analysis/chapter-02-solutions/02_02_Prompt_Paradigms_in_Data_Interaction-solution.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/03_Data_Preparation_and_Cleaning/Notebooks/Data_Cleaning_and_Visualization_Walkthrough-solutions.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/03_Data_Preparation_and_Cleaning/Notebooks/Retail_Sales_Cleaning_Complete_Notebook_Final.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/Images_and_Tricky_Excel.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/Import_and_Clean_JSON.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/04_Data_Formats_and_Input_Techniques/Notebooks/json_import.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/05_Data_Privacy_and_Security_Considerations/Notebooks/Data\ Privacy\ and\ Security\ Considerations.ipynb
/Users/dude1/PycharmProjects/Data\ Analysis\ with\ ChatGPT/05_Data_Privacy_and_Security_Considerations/Notebooks/Untitled.ipynb
```