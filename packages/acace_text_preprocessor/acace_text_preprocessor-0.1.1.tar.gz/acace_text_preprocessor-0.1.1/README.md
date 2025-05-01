# ACACE Text Preprocessor

A text preprocessing module for the Adaptive Context-Aware Content Engine (ACACE).

## Features

- HTML tag removal and entity decoding
- Whitespace normalization
- Simple and efficient text cleaning

## Installation

```bash
pip install acace_text_preprocessor
```

## Usage

```python
from acace_text_preprocessor import preprocess_text

# Clean and normalize text
cleaned_text = preprocess_text("Your <b>HTML</b> text with   extra   spaces")
print(cleaned_text)  # Output: "Your HTML text with extra spaces"
```

## License

MIT License
