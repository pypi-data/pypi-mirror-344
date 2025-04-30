# Trallie Documentation

**Trallie** (Transfer Learning for Information Extraction) is a Python framework that enables structured data extraction from unstructured text using natural language rules and large language models (LLMs). It removes the need for manual data annotation or complex training.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Configuration](#configuration)
6. [Extending Trallie](#extending-trallie)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## 🚀 Features

- Use LLMs to extract structured info based on human-readable rules.
- No labeled training data required.
- Works with OpenAI models or your own LLM backend.
- Output is normalized into structured JSON formats.

---

## 📦 Installation

To install Trallie from source:

```bash
git clone https://github.com/PiSchool/trallie.git
cd trallie
pip install -e .
```

### Requirements

- Python 3.9+
- API key (e.g. from OpenAI) for LLM access

---

## ⚡ Quick Start

Here's a minimal example to extract information:

```python
from trallie import run_extraction

data = {"text": "The Eiffel Tower is located in Paris, France."}
rules = {"location": "Identify geographic locations mentioned in the text."}

result = run_extraction(data, rules)
print(result)
```

### Output (example)

```json
{"location": ["Paris, France"]}
```

---

## 🧠 Core Concepts

### Rule-Based Extraction

Define what to extract using natural language rules like:

- `"person": "Extract all names of people mentioned."`
- `"event": "Find any events described in the text."`

### Extractor

Trallie handles everything through its `Extractor` interface, which:

- Receives input text and rules
- Formats prompts
- Sends them to the selected LLM backend
- Normalizes the results into structured output

---

## ⚙️ Configuration

You can customize Trallie using:

- Python function parameters
- Prompt templates
- Model selection (OpenAI or others)

Add a `.env` file for API configuration:

```
OPENAI_API_KEY=your_key_here
```

---

## 🧩 Extending Trallie

Ways to extend the framework:

- Customize prompt templates
- Add new extractors or normalizers
- Integrate with your NLP or ETL pipelines

---

## 🛠️ Troubleshooting

- **Invalid Schema**: Ensure your rules match expected output formats.
- **Poor Results**: Adjust your prompts or verify model configuration.
- **Rate Limits**: Use batching or rate-limiting with external APIs.

---

## 📄 License

Trallie is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/PiSchool/trallie/blob/main/LICENSE) file for details.
