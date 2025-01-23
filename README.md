# RefineNB

A CLI tool for translating and extracting content from Jupyter notebooks.

## Features

- Translate notebook content (markdown and code cells) to different languages
- Extract notebook content to JSON format

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