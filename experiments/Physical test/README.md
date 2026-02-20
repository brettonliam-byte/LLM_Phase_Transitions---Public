# LLM Physical Reasoning Test: Helicopter Cable Shape

## Experiment Overview
This experiment evaluates the physical reasoning capabilities of various Large Language Models (LLMs) ranging from small (<10B) to massive (>600B) parameters, covering Dense, Mixture-of-Experts (MoE), and Hybrid architectures.

The core task was a specific physics problem designed to test **first-principles derivation** against **pattern matching/retrieval**.

### The Problem Prompt
> "A helicopter is flying horizontally at constant speed. One end of a perfectly flexible uniform cable is affixed beneath the helicopter, the other end is not attached to anything; air friction on the cable is not negligible. What shape will the cable take on?"

### Correct Answer
**A Straight Line.**
*   **Reasoning:** In the helicopter's inertial frame, the cable experiences two constant force vectors per unit length: Gravity (downward) and Aerodynamic Drag (horizontal/backward). The vector sum of these constant forces results in a constant "apparent gravity" vector. A flexible cable aligns with this net force vector, resulting in a straight line inclined backward.

## Files
*   **`Physical Reasoning.txt`**: Raw transcripts of the models' responses.
*   **`Analysis of Physical Reasoning.txt`**: Detailed breakdown of each model's answer, architecture, and failure modes.
*   **`../../results_viz/cable_shape_performance.html`**: Interactive visualization plotting model size vs. reasoning quality.

## Aims
1.  **Assess "Reasoning" vs. "Retrieval":** Standard physics textbooks often discuss the "Catenary" (gravity only). We wanted to see if models would default to this memorized answer or correctly derive the new shape given the "drag" constraint.
2.  **Evaluate Architecture Impact:** Determine if specialized architectures (Reasoning models, Hybrids like Mamba-Transformer) outperform standard Dense/MoE models on physics derivation.
3.  **Test Scaling Laws:** Investigate if larger parameter counts essentially guarantee better physical insight.

## Conclusions
1.  **Scale $\neq$ Reasoning:** Larger models (e.g., 405B+, 1T+) frequently failed, often hallucinating complex curves or defaulting to the "Catenary" answer. They tended to "overthink" the fluid dynamics without performing the basic vector simplification.
2.  **Hybrid & Reasoning Models Excel:** Smaller models tuned for reasoning (e.g., Olmo 3.1 32B Think, Nemotron Nano 9B Hybrid) and reasoning-specialized larger models (DeepSeek R1) correctly identified the "Straight Line" solution. This suggests that training methodology (RLHF for reasoning, synthetic data) is more critical than raw size for this type of task.
3.  **Common Failure Modes:**
    *   **The "Catenary" Bias:** Ignoring the drag vector because "hanging cable" strongly activates the "catenary" latent features.
    *   **The "Curve" Fallacy:** Assuming that because air density or velocity might vary (which they don't in this simplified steady-state), the shape *must* be curved.
    *   **Hallucination:** Smaller, non-reasoning models outputting unrelated shapes like "Sine Wave" or "Tractrix".
