# Utility Scripts

This directory contains various scripts for post-processing experiment data, generating visualizations, and managing the project dashboard.

## Dashboard Generation
- **`generate_dashboard.py`**: Reads `dashboard_config.json` and generates the root `index.html`. This creates the central hub for viewing all experiment results.
  - *Requirements*: Python 3.x.
  - *Usage*: `python generate_dashboard.py`

## Data Processing
- **`process_llm_outputs.py`**: Scans the `OpenrouterAPIcommand/llm_outputs/` directory for JSON files and compiles them into a single, structured Excel file (`combined_responses.xlsx`).
  - *Requirements*: Python 3.x, `pandas`, `openpyxl`.
- **`count_phrases.js`**: Analyzes the frequency of specific phrases or patterns across a set of model responses.

## Visualizations
- **`generate_cable_viz.py`**, **`generate_integral_viz.py`**, **`generate_physical_viz.py`**: Specialized Python scripts that process experiment data and output rich, interactive HTML visualizations (stored in `results_viz/`).
  - *Requirements*: Python 3.x.

## Debugging & Inspection
- **`test_openrouter.js`**: A simple script to verify OpenRouter API connectivity.
- **`inspect_raw.js`**: Prints formatted contents of raw JSON response files to the console for quick inspection.
