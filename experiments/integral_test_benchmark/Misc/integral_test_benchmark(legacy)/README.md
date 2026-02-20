# Integral Calculus Symbolic Reasoning Benchmark

## Experiment Overview
This benchmark evaluates the ability of various LLMs (ranging from 1B to 405B parameters) to solve a complex indefinite integral:

$$ \int \frac{\tan^3(\ln x)}{x} dx $$

*   **Models Tested:** Gemma 3 (1B-27B), Llama 3 (70B, 405B), Mistral 7B, Deepseek R1, and others.
*   **Evaluation:** Solutions were graded on **correctness** (final answer) and **process** (derivation steps).

## Relevance to Phase Transitions
Calculus problems serve as an excellent probe for **Symbolic Reasoning Phase Transitions**.
*   **The "7B" Threshold:** The results highlight a potential phase transition around the 7B parameter mark, where models begin to reliably handle multi-step substitutions ($u = \ln x$) without hallucinating algebraic identities.
*   **Reasoning vs. Scale:** The benchmark compares massive generalist models (Llama 70B) against smaller, reasoning-optimized models (Deepseek, Mistral), revealing that "phase" (reasoning capability) is not solely a function of size, but of training methodology (e.g., RL for reasoning).
*   **Failure Modes:** Distinct failure modes (e.g., hallucinated identities in 1B models vs. subtle sign errors in larger models) map the "trajectory" of mathematical learning in LLMs.

## Files
*   `Integral_Test_Analysis.md`: Detailed report categorizing model performance.
*   `Integral_Test_Analysis.pdf`: PDF version of the analysis.
*   `Integral_Test_Transcripts.pdf`: Raw transcripts of the model outputs (formatted).
*   `Integral Test.txt`: Original raw text source of model outputs.
