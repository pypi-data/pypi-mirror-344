# Language Change

A Python package for simulating language evolution across different historical periods of English.

## Installation

```bash
pip install languagechange
```

Or using Poetry:

```bash
poetry install
```

## Overview

This package provides tools to transform Modern English sentences into approximations of Old English and Middle English. It works by applying word-by-word replacements based on historical linguistic patterns.

## Usage

### Command Line Interface

```bash
# Transform a custom sentence
python -m languagechange.languagechange transform "Nothing ever comes to one that is worth having, except as a result of hard work."

# Use the default test sentence
python -m languagechange.languagechange transform
```

### Python API

```python
from languagechange import LanguageEvolution

# Initialize the language evolution engine
evolution = LanguageEvolution()

# Transform a sentence
sentence = "Nothing ever comes to one that is worth having, except as a result of hard work."

# Get Old English version
old_english = evolution.transform_sentence(sentence, evolution.old_english_replacements)
print(f"Old English: {old_english}")  # Output: "Þū should bēon better æt your job"

# Get Middle English version
middle_english = evolution.transform_sentence(sentence, evolution.middle_english_replacements)
print(f"Middle English: {middle_english}")  # Output: "Thou should been better at your job"

# Using the generator to get all forms
for i, version in enumerate(evolution.generate_evolution(sentence)):
    stage = ["Old English", "Middle English", "Modern English"][i]
    print(f"{stage}: {version}")
```

## Features

- Transform Modern English text to Old English (approximately 5th to 11th century)
- Transform Modern English text to Middle English (approximately 11th to 15th century)
- Preserve capitalization and punctuation during transformation
- Command-line interface with Typer
- Python API for programmatic usage

## Development

### Running Tests

```bash
pytest
```

## License

This work is licensed under [CC BY-NC-ND 4.0 ](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1)
