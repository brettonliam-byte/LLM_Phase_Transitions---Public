# LLM Experiment Framework

A Python-based framework for conducting experiments with Large Language Models (LLMs) across varying temperatures and iteration counts. It supports multiple providers including OpenRouter, OpenAI, Anthropic, Google Gemini, Ollama, and LM Studio.

## Contents

- **`main.py`**: The entry point for running experiments. It iterates through the configurations defined in `config.py`, queries the specified models, and saves results to Excel.
- **`llm_services.py`**: Handles the API logic for different LLM providers.
- **`config.py`**: Central configuration file. Define your experiments here (prompts, models, temperature ranges, iterations).
- **`.env.example`**: Template for environment variables (API keys).

## Setup & Usage

1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Main dependencies: `pandas`, `numpy`, `requests`, `python-dotenv`, `openpyxl`)*

2.  **Environment Variables**:
    Copy `.env.example` to `.env` in the root of the repository (or this folder) and add your API keys:
    ```bash
    OPENROUTER_API_KEY=your_key_here
    OPENAI_API_KEY=your_key_here
    ...
    ```

3.  **Configure Experiments**:
    Open `config.py` and add your experiment dictionaries to the `EXPERIMENTS` list.
    ```python
    {
        "prompt": "Your test prompt",
        "model": "provider/model-name",
        "temperature_range": {"start": 0.0, "end": 1.0, "step": 0.1},
        "iterations": 5,
        "output_file": "my_results.xlsx"
    }
    ```

4.  **Run Experiments**:
    ```bash
    python main.py
    ```
    Results will be saved to the `results/` directory as Excel files.
