# LLM Phase Transition Experiments

This directory is the central hub for all benchmarking experiments designed to identify **phase transitions** in Large Language Model (LLM) reasoning capabilities.

## Experiment Categories

### 1. Linguistic & Symbolic Reasoning
- **`caesar_zero_shot/`**: Tests the "intuitive" (System 1) decryption ability of Gemma 3 models. Focuses on whether models can decode a Caesar cipher in a single step without "thinking out loud."
- **`cot_caesar/`**: Compares the above to "Chain-of-Thought" (System 2) reasoning. Helps visualize the performance boost provided by external reasoning steps.
- **`qwen_caesar/`**: A comparative baseline using the Qwen model family to identify architecture-independent scaling laws.
- **`substitution/`**: Tests numerical substitution ciphers (A=1, B=2...) to observe transitions in 1-to-1 mapping and structural output capabilities.

### 2. Physical & Logical Derivation
- **`Physical test/`**: The "Helicopter Cable" problem. A benchmark designed to distinguish between **first-principles reasoning** and **pattern-matched retrieval**. It tests if models can correctly derive that a hanging cable under constant drag forms a straight line, rather than a catenary curve.

### 3. Mathematical Proficiency
- **`integral_test_benchmark/`**: A focused test on complex calculus integration ($\int \frac{(	an(\ln(x)))^3}{x} \, dx$). Analyzes the stability of symbolic manipulation across varying model temperatures.

## Key Research Questions
1.  **At what parameter scale do specific reasoning capabilities "turn on"?** (e.g., Is 12B the threshold for zero-shot decryption?)
2.  **How does "temperature" (sampling noise) affect these capability phases?** Is there a critical temperature where reasoning coherence abruptly collapses?
3.  **Does architecture (Dense vs. MoE vs. Hybrid) change the nature of these transitions?**

## Data Format
Most experiments store results in **Excel (.xlsx)** for raw data and **Markdown (.md)** for descriptive analysis and visualization summaries.
