# Analysis Tool

This directory contains scripts for processing and analyzing the results of LLM experiments. It provides functionality to extract specific answers from raw model outputs and score them against correct answers.

## Contents

- **`analyse.py`**: The main script for scoring extracted answers. It compares model outputs against a list of correct answers defined in `analysis_config.py` using fuzzy string matching.
- **`extract_answers_integral.py`**: A specialized script for extracting answers to integral calculus problems. It specifically looks for standard calculus notation (e.g., ending in "+ C").
- **`extract_answers.py` / `extract_answers_maths.py`**: General-purpose extraction scripts for other types of queries.
- **`analysis_config.py`**: Configuration file for `analyse.py`. Define input files, output paths, and correct answer strings here.
- **`extract_config.py`**: Configuration file for extraction scripts.

## Setup & Usage

1.  **Install Requirements**:
    Ensure you have the necessary Python packages installed:
    ```bash
    pip install pandas openpyxl
    ```

2.  **Configuration**:
    - Edit `extract_config.py` to point to your raw experiment results (Excel file).
    - Edit `analysis_config.py` to define the correct answers for scoring.

3.  **Run Extraction**:
    Run the appropriate extraction script for your data type:
    ```bash
    python extract_answers_integral.py
    ```
    This will generate a "cleaned" Excel file in the `intermediate/` directory.

4.  **Run Analysis**:
    Run the analysis script on the cleaned data:
    ```bash
    python analyse.py
    ```
    The final scored results will be saved to the `results/` directory.
