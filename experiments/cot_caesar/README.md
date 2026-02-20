# Caesar Cipher Chain-of-Thought (CoT) Experiment

## Experiment Overview
This directory focuses on the **Chain-of-Thought (CoT)** capabilities of the **Gemma 3** family when solving a **Caesar Cipher**.

*   **Task:** Decode the phrase "I think therefore I am".
*   **Condition:** Unlike the zero-shot experiment, models here were **unconstrained**. They were allowed (and naturally tended) to generate verbose explanations, step-by-step shifts, and reasoning traces before providing the final answer.

## Relevance to Phase Transitions
This experiment serves as a contrast to the `caesar_zero_shot` baseline to visualize the "reasoning gap."
*   **Emergence via Compute:** We analyze if allowing the model to generate more tokens (effective test-time compute) triggers a **phase transition** in performance for smaller models (e.g., does the 4B model suddenly succeed where it failed in zero-shot?).
*   **Stability:** By comparing the temperature curves of CoT vs. Zero-Shot, we can determine if reasoning stabilizes the solution, creating a wider "phase" of success against noise (temperature).

## Files
*   `COTGemma.md`: Analysis of the CoT performance.
*   `analyze_cot.js`: Script used to parse and analyze the verbose CoT outputs.
*   `data/`: Directory containing raw output files.
