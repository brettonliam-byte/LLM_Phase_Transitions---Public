# analysis_config.py

ANALYSIS_CONFIG = {
    # REQUIRED: Path to the CLEANED Excel file from the extraction step.
    # This path should point into the `intermediate/` directory.
    "input_file": "intermediate/llama_integral_experiment_CLEANED.xlsx",

    # REQUIRED: A list of all valid or "correct" strings to check against.
    # The analysis will score each cell against every answer in this list
    # and keep the HIGHEST score.
    "correct_answers": [
        "1/2*tan(ln(x))^2 + ln(cos(ln(x))) + C",
        "1/2*sec(ln(x))^2 - ln(sec(ln(x))) + C",
	"1/2*tan(ln(x))^2 - ln(sec(ln(x))) + C", 
	"1/2*sec(ln(x))^2 + ln(cos(ln(x))) + C"
        # Add other mathematically equivalent answers here
    ],

    # REQUIRED: The name for the final analysis Excel file.
    # This file will be saved in the `results/` directory.
    "output_file": "final_analysis_results.xlsx"
}
