# Experiment Results: Caesar Cipher (OLQWEN34B)

## Overview
This experiment tested the ability of the **Qwen 2.5 4B** (or Qwen 3 4B preview) model to decode a message encrypted with a **Caesar cipher**. This serves as a direct comparison to the Gemma 3 family experiments.

*   **Target Phrase:** "I think therefore I am"
*   **Temperature Range:** 0 to 2.0 (0.1 increments)
*   **Repetitions:** 50 attempts per temperature step.

## Results: Qwen 3 4B

### Performance
*   **Overall:** The Qwen model significantly outperformed the Gemma 3 family on this task.
*   **Low Temperature (0.0):** **100% Success Rate.** The model deterministically and correctly decoded the message every single time.
*   **Mid Temperature (0.1 - 1.5):** The model maintained a robust success rate, generally fluctuating between **40% and 70%**. This indicates a strong "basin of attraction" for the correct solution even with induced randomness.
*   **High Temperature (1.6 - 2.0):** A clear **Phase Transition** is visible here. Performance drops sharply, crashing to near zero by Temp 2.0 as the model's output becomes too chaotic to sustain the logical decoding chain.

### Formatting & Spacing
*   **Spacing:** Unlike the Gemma models in the substitution task, the Qwen model showed **negligible spacing issues**. It almost always produced the clean, correctly spaced phrase when it solved the cipher. This suggests a higher quality of tokenization or training data regarding standard phrase structures.

### Origin Recognition
*   **Context Awareness:** There is a strong correlation between the model correctly decoding the phrase and it recognizing the source.
    *   In successful decodes, the model frequently identified the phrase as coming from **René Descartes** ("Cogito, ergo sum"), often citing the Latin origin.
    *   This "Origin Recognition" rate tracked closely with the solve rate, suggesting that recognizing the famous quote helped 'anchor' the decoding process against the noise of higher temperatures.

## Comparison to Gemma 3
*   **Gemma 3 (All sizes):** Failed the Caesar cipher task almost completely (0% success).
*   **Qwen 3 4B:** Achieved 100% success at Temp 0 and sustained high performance.
*   **Conclusion:** For this specific logic/decoding task, the Qwen 4B model demonstrates significantly higher capability and robustness than the equivalent (and even larger) Gemma 3 models.
