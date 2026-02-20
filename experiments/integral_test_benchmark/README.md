# Integral Test Benchmark

This experiment benchmarks the ability of various LLMs to solve a specific, non-trivial calculus integral:

$$\int \frac{(	an(\ln(x)))^3}{x} \, dx$$

## Experiment Design
- **Task:** Solve the integral from first principles.
- **Substitution:** The problem is best solved by substituting $u = \ln(x)$, $du = \frac{1}{x} dx$, reducing it to $\int 	an^3(u) \, du$.
- **Objective:** Observe how models handle symbolic manipulation, trigonometric identities, and the integration constant ($+ C$).

## Contents

- **`Output/`**: Contains the raw experiment results in Excel format for various models, including:
  - Llama 3.3 70B
  - Gemma 3 (various sizes)
  - Qwen 3
  - DeepSeek R1 (Reasoning model)
- **`Misc/`**: Supplemental notes and early analysis.

## Analysis
Results from this benchmark are visualized in the main dashboard under **"Integral Solving Performance"**. Key observations include:
- **Phase Transition:** Smaller models often "hallucinate" complex but incorrect trigonometric reductions.
- **Temperature Sensitivity:** Correctness often peaks at low temperatures ($T \approx 0.2$) and rapidly degrades as sampling noise introduces symbolic errors.
- **Reasoning Models:** Models like DeepSeek R1 show a much wider "success phase," maintaining correct derivations even at higher temperatures.
