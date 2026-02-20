# Results Visualizations

This directory contains interactive HTML dashboards and visualizations that summarize the findings of various LLM experiments.

## Visualizations

- **`integral_visualization.html`**: Analyzes model performance on complex calculus integrals. It focuses on how temperature affects correctness and consistency.
- **`cable_shape_performance.html`**: Visualizes model reasoning when tasked with determining the shape of a hanging cable under drag. It highlights the difference between "pattern-matching" (catenary) and "reasoning" (straight line).
- **`comprehensive_visualization.html`**: A high-level overview combining multiple benchmarks to provide a comparative look at different model architectures (MoE, Dense, Reasoning-optimized).
- **`visualization.html`**: General baseline performance metrics across all models.

## Supporting Data
The visualizations are powered by JSON data exports:
- `experiment_data.json`
- `cot_data.json`
- `qwen_data.json`

## How to View
These files are designed to be viewed in any modern web browser. They are also linked from the central dashboard at the root of the repository (`index.html`).
