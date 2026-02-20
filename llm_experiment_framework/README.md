# LLM Experiment Framework

This framework allows you to run batch LLM queries against various models and services. It is designed to test model performance across a range of temperatures, running multiple iterations for each temperature step and saving the results to a structured Excel file.

## Setup

Follow these steps to set up the experiment framework.

#### **1. Set Up API Keys**

This framework requires API keys to communicate with various LLM services.

1.  Navigate to the root directory of the `LLM_Phase_Transitions` repository.
2.  Create a new file named `.env`.
3.  Copy the contents of `.env.example` (located in this directory) into your new `.env` file.
4.  Fill in the necessary API keys and endpoints for the services you intend to use.

Your `.env` file should look something like this:

```
# OpenRouter API Key
OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"

# OpenAI API Key
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# Ollama API Endpoint (defaults to http://localhost:11434)
OLLAMA_BASE_URL="http://localhost:11434"
```

#### **2. Install Dependencies**

Navigate to the `llm_experiment_framework` directory and install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Running an Experiment

#### **1. Configure Your Experiments**

Open `config.py` to define the experiments you want to run. The configuration is a list of Python dictionaries called `EXPERIMENTS`.

Each dictionary represents a batch of experiments for a single prompt and has the following structure:

```python
EXPERIMENTS = [
    {
        "prompt": "You are a Roman citizen living in the year 450 AD. What god(s) do you believe in?",
        "model": "ollama/gemma:2b",
        "temperature_range": {
            "start": 0.0,
            "end": 2.0,
            "step": 0.2
        },
        "iterations": 10,
        "output_file": "roman_gods_experiment.xlsx"
    },
    # You can add more experiment blocks here
]
```

-   `prompt`: The text of the prompt you want to send to the model.
-   `model`: The model to use, specified in the format `"service/model_name"`.
    -   **Examples:** `"ollama/gemma:2b"`, `"openrouter/google/gemini-pro-1.5"`, `"openai/gpt-4"`.
-   `temperature_range`: A dictionary defining the temperature sweep.
    -   `start`: The starting temperature (e.g., `0.0`).
    -   `end`: The ending temperature (e.g., `2.0`).
    -   `step`: The increment for each step in the temperature range (e.g., `0.2`).
-   `iterations`: The number of times to run the prompt for *each* temperature step.
-   `output_file`: The name of the Excel file where results will be saved. This file will be created in the `results/` directory.

#### **2. Execute the Script**

Once your `.env` and `config.py` files are set up, run the main script from the `llm_experiment_framework` directory:

```bash
python main.py
```

The script will begin executing the experiments, printing its progress to the console.

## Viewing the Output

The results will be saved in an `.xlsx` file inside the `results/` directory.

-   Each unique prompt/model combination gets its own **sheet** within the workbook.
-   Within a sheet, each **row** corresponds to an iteration.
-   Each **column** corresponds to a temperature step.
-   The **cells** contain the raw text response from the LLM for that specific iteration and temperature.