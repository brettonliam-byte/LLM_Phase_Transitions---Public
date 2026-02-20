# Logprob API Collector

This tool is designed to capture detailed token-level logprobabilities from LLM APIs (specifically OpenAI and OpenRouter). It allows for deep analysis of model confidence and "thinking" patterns.

## Contents

- **`query_llm.js`**: A Node.js script that executes LLM queries according to `llm_config.json` and saves the full raw response, including logprobs, as JSON.
- **`export_logprobs_to_excel.py`**: A Python script that parses the JSON output and generates an Excel file. It includes a summary of responses and detailed sheets for token-level logprobs.
- **`extract_token_logprobs.py`**: A utility to extract and isolate specific token probabilities from the collected data.
- **`llm_outputs/`**: Directory where raw JSON responses are stored.

## Setup & Usage

### 1. Requirements
- **Node.js**: v18+ (for native `fetch` support).
- **Python**: 3.x with `pandas` and `openpyxl`.

### 2. Configuration
Ensure your API keys are set in a `.env` file in the project root:
```bash
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### 3. Execution
1.  Configure your prompt and model in `llm_config.json`.
2.  Run the query script:
    ```bash
    node query_llm.js
    ```
3.  Export the results to Excel for analysis:
    ```bash
    python export_logprobs_to_excel.py llm_outputs/your_result.json
    ```
