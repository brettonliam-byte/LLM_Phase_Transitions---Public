# Integral Calculus Symbolic Reasoning Benchmark

## Experiment Overview
This benchmark evaluates the ability of various Large Language Models (LLMs) to solve a complex indefinite integral:

$$ \int \frac{\tan^3(\ln x)}{x} dx $$

*   **Total Models Tested:** 23 (across two phases).
*   **Range:** 1B parameters (Mobile) to 1T parameters (DeepSeek/Kimi).
*   **Architectures:** Dense Transformers, Sparse Mixture-of-Experts (MoE), Hybrid Mamba (SSM), and "Reasoning" models (RLVR).

## Key Findings (Phase 1 & 2)

Calculus problems serve as an excellent probe for **Symbolic Reasoning Phase Transitions**, revealing distinct capability thresholds:

### 1. The "7B" Threshold
Initial testing (Phase 1) suggested a phase transition around the 7B parameter mark, where models began to reliably handle substitution ($u = \ln x$) without hallucinating algebraic identities.

### 2. Architecture vs. Scale (Phase 2)
The second phase of testing challenged the "bigger is better" hypothesis:
*   **Hybrid Wins:** The **Nemotron Nano 12B** (Hybrid Mamba) outperformed the **Llama 3.3 70B** (Dense), proving that State Space Models (SSMs) excel at maintaining the logical state required for multi-step math.
*   **Active Parameter Trap:** Sparse MoE models with low *active* parameter counts (e.g., Trinity Mini with 3B active) failed where denser models of similar size succeeded, indicating a specific minimum active memory requirement for symbolic logic.

### 3. The Rise of Metacognition
The strongest performers (Olmo 3 32B Think, DeepSeek R1, Kimi K2) exhibited **Metacognition** (thinking about thinking). They explicitly verified their own answers by differentiating the result, a step completely missing from standard "chat" models.

## Files
*   `Integral_Test_Analysis_2.pdf` / `.tex`: Comprehensive analysis of all 23 models, including the architectural breakdown.
*   `Integral Test.txt`: Raw transcripts for all models (Phase 1 & Phase 2 combined).
*   `Integral Analysis 2.txt`: Text-based summary of the Phase 2 analysis.
*   `integral_test_benchmark(legacy)/`: Archive of previous test runs and analyses.

## Evaluation Criteria
Models were graded on:
1.  **Correctness:** Final boxed answer matching $\frac{1}{2}\tan^2(\ln x) + \ln|\cos(\ln x)| + C$ (or equivalent).
2.  **Process:** Valid derivation steps (substitution $u=\ln x$, identity $\tan^2 = \sec^2 - 1$).
3.  **Stability:** Absence of hallucinations (e.g., inventing trig identities).
