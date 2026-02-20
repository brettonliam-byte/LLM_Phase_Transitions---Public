# Experiment Results: Caesar Cipher with Chain-of-Thought (COTGemma)

## Overview
This experiment revisits the **Caesar cipher** task with the **Gemma 3** family. 

**Key Difference:**
*   **Initial Experiment (OL3file):** The prompt included the constraint **"return the deciphered message only"**. This forced the models to output the answer directly, suppressing intermediate reasoning.
*   **This Experiment (COTGemma):** The constraint was **removed**. The models were free to output verbose explanations, enabling **Chain-of-Thought (CoT)** reasoning.

*   **Target Phrase:** "I think therefore I am"
*   **Temperature Range:** 0 to 2.0 (0.1 increments)
*   **Repetitions:** 50 attempts per temperature step.

## Results by Model

### Gemma 3 1B (G1B)
*   **Success Rate:** 0%
*   **Analysis:** Even with the freedom to reason, the 1B model lacked the capability to deduce the cipher or perform the shift correctly.

### Gemma 3 4B (G4B)
*   **Success Rate:** 0%
*   **Analysis:** Similar to the 1B model, the 4B model failed to solve the task, even with verbose output.

### Gemma 3 12B (G12B)
*   **Success Rate:** **~6.5% (69 total solves)**
*   **Comparison:** 
    *   **Zero-Shot (Return Only):** < 0.2% (2 solves).
    *   **CoT (Free):** ~6.5%.
*   **Analysis:** Removing the constraint triggered a **significant improvement**. The model often recognized the cipher as "Caesar" or "ROT13" (sometimes incorrectly), but when it correctly identified the shift (often through trial and error in the text), it successfully decoded the message. This confirms that the model's reasoning capability is present but was suppressed by the strict formatting constraint in the previous experiment.

### Gemma 3 27B (G27B)
*   **Success Rate:** **~1.5% (16 total solves)**
*   **Comparison:**
    *   **Zero-Shot (Return Only):** 0%.
    *   **CoT (Free):** ~1.5%.
*   **Analysis:** The 27B model also showed improvement, transitioning from complete failure to occasional success. Interestingly, it had a lower raw success count than the 12B model in this specific run, potentially due to over-thinking or hallucinating more complex ciphers given its larger context window and training depth.

## Conclusion
**Chain-of-Thought is Critical for Gemma 3 on Logic Tasks.**
The contrast between the near-zero performance in the "Return Only" experiment and the measurable success in this "Free" experiment demonstrates that **Gemma 3 models (specifically 12B+) rely heavily on verbalizing their reasoning process** to solve logic puzzles like ciphers. Forcing them to output only the answer effectively lobotomizes their problem-solving logic for this difficulty class.

In contrast, the **Qwen 4B** model (tested separately) achieved 100% success even with constraints, highlighting a fundamental difference in reasoning efficiency or training focus between the two model families.
