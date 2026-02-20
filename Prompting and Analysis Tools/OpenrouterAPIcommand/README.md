# OpenRouter API Command

A streamlined tool for executing repeated queries to OpenRouter models and logging the results directly to Excel.

## Contents

- **`query_llm.js`**: The main Node.js script. It reads configuration from `llm_config.json`, handles API communication, and coordinates with a Python helper to save data.
- **`update_excel.py`**: A Python helper script that manages the Excel file operations.
- **`llm_config.json`**: The configuration file defining the model, prompt, number of iterations (N), and output file path.
- **`llm_outputs/`**: Default directory for storing raw JSON response data.

## Setup & Usage

### 1. Requirements
- **Node.js**: v18+.
- **Python**: 3.x with `pandas` and `openpyxl`.

### 2. Usage
1.  Set your `OPENROUTER_API_KEY` in the `.env` file.
2.  Edit `llm_config.json` to specify your experiment:
    ```json
    {
      "provider": "openrouter",
      "model": "meta-llama/llama-3.3-70b-instruct",
      "N": 10,
      "user_prompt": "Your question here",
      "excel_file": "./results.xlsx"
    }
    ```
3.  Run the script:
    ```bash
    node query_llm.js
    ```
