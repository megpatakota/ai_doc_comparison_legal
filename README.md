# AI Document Comparison on Legal Documents

Here’s a professional `README.md` for your GitHub repository, structured similarly to your example:

---

# Document Processing Pipeline

[![Project Status](https://img.shields.io/badge/Status-In%20Development-orange)]()
[![by Meg Patakota](https://img.shields.io/badge/by-Meg%20Patakota-blue)](https://megpatakota.co.uk)

> ⚠️ **Disclaimer:** This project is a work in progress. Features, code structure, and documentation may evolve over time.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Flow](#pipeline-flow)
- [Data Structure](#data-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project is a **document processing pipeline** that standardizes, extracts, and compares structured sections from input documents using **LLMs** and **text-processing techniques**. 

The pipeline:
- **Extracts key sections** from `.docx` documents.
- **Standardizes content** using a predefined template.
- **Compares versions** of documents to highlight differences.

![Process Diagram - Pipeline1](./images/mainllm.png)

![Process Diagram - Pipeline2](./images/simplellm.png)


---

## Installation

### Prerequisites
- Python 3.13+
- Poetry (for dependency management)

### Clone the Repository

```bash
git clone https://github.com/yourusername/document-processing-pipeline.git
cd document-processing-pipeline
```

### Install Dependencies
Using Poetry:

```bash
poetry install
```

---
# Output

You can use https://markdownlivepreview.com to paste the .txt file output for better formatting and readability
---
## Pipeline Flow

### 1️⃣ **Document Preprocessing**
- Reads `.docx` input files.
- Cleans and tokenizes text.
- Identifies major sections.

### 2️⃣ **Section Extraction**
- Uses predefined rules or LLMs to detect and extract structured content.

### 3️⃣ **Standardization**
- Formats extracted sections into a structured output.
- Aligns content with predefined templates.

### 4️⃣ **Comparison & Analysis**
- Compares extracted sections between two document versions.
- Identifies differences and generates structured outputs.

---

## Data Structure

The repository follows this structure:

```
.
├── data
│   ├── input                    # Raw input documents
│   ├── output                   # Processed and structured outputs
│   ├── temp                      # Intermediate processing files
├── notebooks                     # Jupyter Notebooks for analysis
├── src                           # Core processing scripts
├── templates                     # Jinja2 templates for formatting
├── pipeline1.py                  # Main processing pipeline
├── compare.py                    # Comparison module
├── simple_llm.py                 # LLM-based processing
├── README.md                      # Project documentation
```

---

## Contributing

Contributions are welcome! To contribute:
1. **Fork the repository**.
2. **Create a new branch** (`feature-branch`).
3. **Submit a pull request (PR)**.

---

## License

This project is maintained by **Meg Patakota**. Not licensed for redistribution or commercial use without explicit permission.

---

Let me know if you’d like any refinements! 🚀



