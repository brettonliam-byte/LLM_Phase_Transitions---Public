# extract_config.py

EXTRACT_CONFIG = {
    # REQUIRED: Path to the raw Excel file from the experiment framework.
    "input_file": "../llm_experiment_framework/results/llama_integral_experiment.xlsx",

    # REQUIRED: The name for the output file containing the extracted answers.
    # This file will be saved in the `intermediate/` directory.
    # The extraction script you run (e.g., extract_answers_integral.py)
    # will automatically add a suffix (e.g., '_integral') to this filename.
    "output_file": "llama_integral_experiment_CLEANED.xlsx",

    # OPTIONAL: A list of specific sheet names to process.
    # If this list is empty or the key is removed, the script will process ALL sheets.
    # If you provide names, only those sheets will be processed and updated in the output file.
    # Example: ["sheet_name_1", "sheet_name_2"]
    "sheets_to_process": []
}