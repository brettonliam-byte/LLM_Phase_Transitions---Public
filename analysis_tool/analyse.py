# analyse.py
import pandas as pd
import difflib
from pathlib import Path

try:
    from analysis_config import ANALYSIS_CONFIG
except ImportError:
    print("Error: Could not import 'ANALYSIS_CONFIG' from analysis_config.py.")
    ANALYSIS_CONFIG = {}

def get_best_similarity_score(response_text, correct_answers_list):
    """
    Calculates the similarity of response_text against a list of correct answers
    and returns the highest score.
    """
    if not isinstance(response_text, str):
        response_text = ""

    if not correct_answers_list:
        return 0.0

    max_score = 0.0
    for correct_answer in correct_answers_list:
        # SequenceMatcher provides a ratio of matching characters.
        current_score = difflib.SequenceMatcher(None, response_text.lower(), correct_answer.lower()).ratio()
        if current_score > max_score:
            max_score = current_score
    
    return max_score

def run_analysis():
    """
    Main function to run the analysis based on the imported configuration.
    """
    print("--- Starting LLM Response Analysis ---")

    # 1. Load and Validate Configuration
    input_path_str = ANALYSIS_CONFIG.get("input_file")
    correct_answers = ANALYSIS_CONFIG.get("correct_answers") # Now a list
    output_filename = ANALYSIS_CONFIG.get("output_file")

    if not all([input_path_str, correct_answers, output_filename]):
        print("Error: 'input_file', 'correct_answers', and 'output_file' must be set in analysis_config.py")
        return
    
    if not isinstance(correct_answers, list) or not correct_answers:
        print("Error: 'correct_answers' must be a non-empty list in analysis_config.py")
        return

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_path_str

    # Ensure the output directory exists
    results_dir = script_dir / "results"
    results_dir.mkdir(exist_ok=True)
    output_path = results_dir / output_filename

    if not input_path.exists():
        print(f"Error: Input file not found at '{input_path}'")
        return

    print(f"Loading experiment results from: {input_path.name}")
    print(f"Analyzing against {len(correct_answers)} possible correct answers.")
    
    # 2. Read the Input Excel File
    try:
        xls = pd.ExcelFile(input_path)
        sheet_names = xls.sheet_names
        print(f"Found {len(sheet_names)} sheets to analyze.")
    except Exception as e:
        print(f"Error: Could not read the Excel file. Make sure it's a valid .xlsx file. Details: {e}")
        return

    # 3. Process Each Sheet and Write to Output
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet in sheet_names:
            print(f"  -> Processing sheet: '{sheet}'...")
            try:
                df = pd.read_excel(xls, sheet_name=sheet)

                if 'Iteration' not in df.columns:
                    print(f"     - Skipping sheet '{sheet}' as it does not have an 'Iteration' column.")
                    continue
                
                data_columns = [col for col in df.columns if col != 'Iteration']
                
                analysis_df = df[['Iteration']].copy()

                for col in data_columns:
                    analysis_df[col] = df[col].apply(lambda cell_content: get_best_similarity_score(cell_content, correct_answers))
                
                new_sheet_name = f"ANALYSIS_{sheet}"[:31]
                analysis_df.to_excel(writer, sheet_name=new_sheet_name, index=False)

            except Exception as e:
                print(f"     - Error processing sheet '{sheet}': {e}")
                continue
    
    print(f"\n--- Analysis Complete ---")
    print(f"Results saved to: '{output_path}'")

if __name__ == "__main__":
    run_analysis()