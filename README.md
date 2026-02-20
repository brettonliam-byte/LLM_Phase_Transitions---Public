# LLM Phase Transitions & Emergent Reasoning

This project investigates **phase transitions** in Large Language Model (LLM) behavior, specifically focusing on how reasoning, symbolic manipulation, and physical intuition emerge as a function of **model scale** and **sampling temperature**.

## Project Overview
We use a multi-modal experimental framework (Python, Node.js, and Mathematica) to systematically probe LLMs. By sweeping across model sizes (from 1B to 1T+ parameters) and temperatures (0.0 to 2.0), we identify the "critical points" where models transition from deterministic failure to emergent success, and eventually to creative hallucination.

### [View Interactive Dashboard](https://brettonliam-byte.github.io/LLM_Phase_Transitions/)

## Core Research Areas

### 1. Linguistic Phase Transitions (Caesar & Substitution Ciphers)
Testing at what point a model can "internally" decode symbolic shifts without external scratchpads.
- **Zero-Shot vs. Chain-of-Thought**: Comparing "System 1" (fast) vs "System 2" (slow) decryption.
- **Scale Impact**: Identifying the parameter threshold (e.g., 12B vs 27B) for stable decryption.

### 2. Physical Intuition (The Helicopter Cable Problem)
A benchmark designed to distinguish between **reasoning** (derivation from first principles) and **retrieval** (pattern matching from training data).
- **The Challenge**: Can the model correctly identify that a cable under constant drag forms a straight line, resisting the linguistic pull of the common "catenary curve"?

### 3. Mathematical Stability (Calculus Integrals)
Benchmarking the ability of models to solve complex integrals like $\int \frac{(\tan(\ln(x)))^3}{x} \, dx$.
- **Temperature Sensitivity**: Observing how symbolic coherence breaks down as sampling noise increases.

## Repository Structure

- **`/experiments`**: Detailed logs, data, and analysis for each benchmark (Caesar, Physics, Integrals).
- **`/llm_experiment_framework`**: A Python framework for batch querying models via OpenRouter, Ollama, and more.
- **`/LogprobAPICollector`**: Specialized tools for capturing token-level logprobabilities to analyze model confidence.
- **`/results_viz`**: Interactive HTML dashboards and visualizations.
- **`/scripts`**: Utility scripts for data processing, analysis, and dashboard generation.
- **`/notebooks`**: Wolfram Mathematica notebooks used for exploratory research.
- **`/analysis_tool`**: Python scripts for extracting and scoring model answers.

## Getting Started

### Requirements
- **Python 3.x**: `pip install -r llm_experiment_framework/requirements.txt`
- **Node.js**: v18+ (for API collectors)
- **Ollama**: For local model execution.

### Configuration
1. Create a `.env` file in the root based on `llm_experiment_framework/.env.example`.
2. Add your `OPENROUTER_API_KEY` or other provider keys.

### Running an Experiment
```bash
# Using the Python Framework
python llm_experiment_framework/main.py

# Using the Node.js Collector (for logprobs)
cd LogprobAPICollector
node query_llm.js
```

## Authors
- **Bretton Liam** (@brettonliam-byte)
