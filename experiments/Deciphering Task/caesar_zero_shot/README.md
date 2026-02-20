# Caesar Cipher Zero-Shot Experiment

## Experiment Overview
This directory contains data and results for testing the **Gemma 3** family of models on a **Caesar Cipher** decoding task under strict **Zero-Shot** conditions.

*   **Task:** Decode the phrase "I think therefore I am" from a Caesar cipher shift.
*   **Constraint:** The models were explicitly instructed to **"return the deciphered message only"**. This negative constraint suppresses the model's ability to "think out loud" (Chain of Thought), forcing it to perform the decryption step in a single forward pass (or implicitly within the hidden states) before outputting the first token.

## Relevance to Phase Transitions
This experiment is designed to detect **emergent capabilities** in "system 1" (intuitive/fast) thinking.
*   **Phase Transition:** We observe at what model size (1B, 4B, 12B, 27B) the ability to internally simulate the cipher shift emerges without the "scratchpad" of external reasoning.
*   **Temperature Sensitivity:** The experiment sweeps temperatures (0.0 - 2.0) to identify the stability of this capability. A sharp drop-off in success rate at a critical temperature often indicates a fragile phase transition where the "basin of attraction" for the correct answer is narrow.

## Files
*   `OL3file.md`: Detailed summary of results and analysis.
*   `OL3file.xlsx`: Raw data of model outputs across temperature ranges.
