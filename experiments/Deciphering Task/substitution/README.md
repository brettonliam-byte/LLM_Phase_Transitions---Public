# Numerical Substitution Cipher Experiment

## Experiment Overview
This experiment tests the **Gemma 3** family on a **Numerical Substitution Cipher** (A=1, B=2, ... Z=26).

*   **Task:** Decode a sequence of numbers into the phrase "I think therefore I am".
*   **Complexity:** This task requires strict 1-to-1 mapping and memory retrieval, distinct from the pattern-matching shift of a Caesar cipher.

## Relevance to Phase Transitions
This experiment highlights **partial state transitions** or "formatting vs. reasoning" decoupling.
*   **The "Close" State:** The 4B model exhibited a unique phase where it could correctly decode the *letters* (informational content) but consistently failed to structure them into *words* (formatting/spacing).
*   **Granularity:** This suggests that "decoding ability" and "output structuring" are separate latent capabilities that may emerge at different scales (phases), rather than a single "solving" capability turning on at once.

## Files
*   `OL4file.md`: Detailed analysis of the substitution task.
*   `OL4file.xlsx`: Raw data log.
