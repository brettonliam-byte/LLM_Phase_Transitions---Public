# Experiment Results: Caesar Cipher (OL3file)

## Overview
This experiment tested the ability of the **Gemma 3** family of models to decode a message encrypted with a **Caesar cipher**.

*   **Target Phrase:** "I think therefore I am"
*   **Temperature Range:** 0 to 2.0 (0.1 increments)
*   **Repetitions:** 50 attempts per temperature step.

## Results by Model

### Gemma 3 1B (G1B)
*   **Performance:** 0% success rate.
*   **Analysis:** The model consistently failed to decode the cipher, hallucinating unrelated text.

### Gemma 3 4B (G4B)
*   **Performance:** 0% success rate.
*   **Analysis:** No improvement over the 1B model.

### Gemma 3 12B (G12B)
*   **Performance:** < 0.2% success rate (2 correct solves out of 1050 attempts).
*   **Specific Successes:**
    *   **Temp 1.3:** One successful decode.
    *   **Temp 1.8:** One successful decode.
*   **Analysis:** 
    *   The model failed in the vast majority of cases. 
    *   However, the two successful attempts are notable. In both cases, the model spontaneously adopted a **Chain-of-Thought (CoT)** reasoning process, explicitly identifying the cipher type ("Caesar cipher"), deducing the shift amount ("shift back of 5"), and verifying the shift on letters before producing the final answer.
    *   This suggests the model *possesses* the capability to solve the task, but the prompt did not reliably trigger the necessary reasoning steps (CoT) required to utilize that capability.

### Gemma 3 27B (G27B)
*   **Performance:** 0% success rate.
*   **Analysis:** Surprisingly, the 27B model failed to produce any correct solves in this run. It likely suffered from the same lack of CoT triggering as the 12B model, but simply didn't stumble upon the successful path in this specific sample set.

## Conclusion
The results indicate a near-complete failure of the Gemma 3 models (1B - 27B) to zero-shot decode this specific Caesar cipher prompt. 

The **exception** is the **12B model**, which managed 2 correct solves by spontaneously generating a step-by-step reasoning chain. This highlights a "latent capability" that is present but fragile, requiring specific conditions (like high temperature inducing a different generation path) or explicit CoT prompting to manifest reliably.