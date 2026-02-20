# Experiment Results: Substitution Cipher (OL4file)

## Overview
This experiment tested the ability of the **Gemma 3** family of models to decode a message encrypted with a **numerical substitution cipher** (A=1, B=2, etc.).

*   **Target Phrase:** "I think therefore I am"
*   **Temperature Range:** 0 to 2.0 (0.2 increments)
*   **Repetitions:** ~25 attempts per temperature step.

## Results by Model

### Gemma 3 1B (G1B)
*   **Performance:** < 5% success rate.
*   **Analysis:** The model struggled significantly. While it occasionally outputted the correct letters embedded within hallucinations (flagged as "close"), it rarely produced a coherent, clean answer.

### Gemma 3 4B (G4B)
*   **Performance:** **High "Close" Rate, Low "Perfect" Rate.**
*   **Analysis:** The 4B model demonstrates a clear step up in capability. It consistently correctly deciphered the letters of the phrase (e.g., "ITHINKTHEREFOREIAM") but struggled with word segmentation and spacing (outputting "I THINK I REEREA I AM" or similar jumbled spacing).
    *   **Phase Transition:** At lower temperatures (0 - 0.5), nearly 100% of attempts contained the correct letter sequence. As temperature increased, this reliability dropped slightly, but remained high.

### Gemma 3 12B (G12B)
*   **Performance:** **Good (Mixed Perfect & Close).**
*   **Analysis:** The 12B model bridged the gap between raw decoding and formatting.
    *   **Success Rate:** It achieved a "Perfect" solve rate of ~30-50% across most temperatures.
    *   **Close Solves:** When it didn't get it perfect, it almost always got the letters correct (flagged as "Close"), yielding a total effective accuracy of near 100% for the decoding part of the task.

### Gemma 3 27B (G27B)
*   **Performance:** **Excellent (Near Perfect).**
*   **Analysis:** The 27B model demonstrated mastery of the task.
    *   **Success Rate:** consistently achieved >90% "Perfect" solve rates across the temperature range.
    *   **Phase Transition:** Performance remained robust even at higher temperatures, showing that the larger parameter count provides stability and deeper reasoning capabilities for this substitution task.

## Conclusion
A clear "Phase Transition" is visible across model sizes for the substitution cipher task:
1.  **1B:** Incompetent.
2.  **4B:** Competent Decoder, Poor Formatter (Gets the letters, fails the spaces).
3.  **12B:** Competent Decoder, Inconsistent Formatter (Often perfect, sometimes spacing issues).
4.  **27B:** Master (Consistently perfect).

This progression highlights how "intelligence" in LLMs often emerges in layers: first the core logic (decoding), then the subtle adherence to constraints (formatting/spacing).
