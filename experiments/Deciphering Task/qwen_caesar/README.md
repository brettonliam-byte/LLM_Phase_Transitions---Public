# Qwen Caesar Cipher Baseline

## Experiment Overview
This directory contains benchmarking results for the **Qwen 2.5 4B** (or Qwen 3 4B Preview) model on the **Caesar Cipher** task.

*   **Task:** Decode the phrase "I think therefore I am".
*   **Role:** This experiment acts as a **Control Group / Cross-Architecture Comparison** to the Gemma 3 experiments.

## Relevance to Phase Transitions
By testing a different model architecture of similar size (4B), we can isolate which "phase transitions" are universal to LLM scaling and which are specific to a model family's training dynamics.
*   **Performance Delta:** Qwen 4B showed significantly distinct behavior (higher success rate, different failure modes) compared to Gemma 3 4B.
*   **Critical Temperature:** This data helps pinpoint the "critical temperature" where Qwen's reasoning coherence collapses (identified around T=1.6 in the logs), providing a data point for the "thermodynamics" of text generation.

## Files
*   `OLQWEN34B.md`: Summary of Qwen's performance ("34B" in filename refers to Qwen 3 4B).
*   `OLQWEN34B.xlsx`: Raw experimental data.
*   `analyze_qwen.js`: Analysis script for Qwen outputs.
