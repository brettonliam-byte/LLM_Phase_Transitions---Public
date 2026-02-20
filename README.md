# LLM Phase Transitions

This project investigates the concept of "phase transitions" in Large Language Models (LLMs), exploring how their behavior changes in response to varying parameters, particularly "temperature."

## Methodology

The experiments are conducted using Mathematica to systematically query various LLMs. We utilize both local models via the **Ollama** library and remote models via the **OpenRouter** API. The core idea is to test the models' reasoning, decoding, and creative capabilities under different conditions.

### Core Tasks
1.  **Caesar Cipher Decoding:** Models are prompted to decode the message `'N ymnsp ymjwjktwj N fr'` (which decodes to "I think therefore I am") across a range of temperatures.
2.  **Creative Generation:** Models are asked to generate items (e.g., tool names) based on specific personas and historical contexts.

## Experiments

The experiments are documented in the following Mathematica notebooks:

### Cipher Decoding Experiments
*   **`Gemma3_Temp_Caesar.nb`**: A comprehensive test of the **Gemma 3** family (`1b`, `4b`, `12b`, `27b`) on the Caesar cipher task.
    *   **Variables:** Temperature (0 to 2, step 0.2), Repetitions (25).
    *   **Output:** `OL4file.xlsx`
*   **`17.11.25.nb`**: Tests the **Qwen 3** (`4b`) model on the Caesar cipher task.
    *   **Variables:** Temperature (0 to 2, step 0.1), Repetitions (50).
    *   **Output:** `OLQWEN34B.xlsx`
*   **`25.11.25.nb`**: Tests the **GLM-4.5-Air** model (`z-ai/glm-4.5-air:free`) via the OpenRouter API.
    *   **Variables:** Temperature (0 to 2, step 0.2), Repetitions (25).
    *   **Output:** `OR5.xlsx`

### Creative Generation Experiments
*   **`20.10.25.nb`**: Tests **Gemma 3** (`12b`) on a creative generation task at high temperature (Temp 2).
    *   **Prompts:**
        1.  "You are a villager living in rural England in 1066. Can you give me the name of a tool?"
        2.  "You are a wealthy noble living in London, England in 1066. Can you give me the name of a tool?"
    *   **Variables:** Temperature (2), Repetitions (50).
    *   **Output:** `OL2file.xlsx`

### Legacy Experiments
*   `7.11.25.nb`: Early tests with `gemma3` models.
*   `10.11.25.nb`: Tests using a numerical substitution cipher.
*   `13.10.25.nb` & `13.10.25 Chat.nb`: Exploratory work with creative generation tasks (e.g., generating names for cats and tools).

## Results

The raw results of the experiments are exported to `.xlsx` files. These files contain the responses of the LLMs for each model and temperature setting, allowing for analysis of the "phase transition" from deterministic accuracy to creative hallucination or failure.

## How to Run the Code

The experiments are defined in the Mathematica notebooks (`.nb` files).

To run the experiments yourself, you will need:
1.  **Mathematica**: A working installation.
2.  **Ollama**: For running local models (Gemma, Qwen). Ensure the specific models used in the notebooks are pulled (e.g., `ollama pull gemma3:12b`).
3.  **OpenRouter API Key**: Required for `25.11.25.nb` to access remote models.
4.  **Custom Functions**: Some notebooks rely on `LLMSynthesize` (built-in) or custom wrappers like `LLMRequest` defined within the notebook itself.