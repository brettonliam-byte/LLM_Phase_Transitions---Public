# extract_answers_stable.py
# This is a copy of the previous version of the extraction script for comparison.

import pandas as pd
import re
from pathlib import Path

try:
    from extract_config import EXTRACT_CONFIG
except ImportError:
    print("Error: Could not import 'EXTRACT_CONFIG' from extract_config.py.")
    EXTRACT_CONFIG = {}

def _post_process_equals_sign(text):
    """
    If the text contains an equals sign, extracts the part after the last equals sign.
    Assumes format like "integral = answer".
    """
    if not isinstance(text, str) or '=' not in text:
        return text.strip()
    
    return text.rsplit('=', 1)[-1].strip()

def extract_answer(cell_content):
    """
    Tries to extract the final answer from a cell's content using a series of heuristics.
    """
    if not isinstance(cell_content, str) or not cell_content.strip():
        return "" # Return empty for empty or non-string cells

    extracted_candidate = ""

    # --- Heuristics for finding the answer ---

    # 1. Look for specific phrases indicating a final answer (case-insensitive)
    phrases = [
        r"the final answer is:?",
        r"the solution is:?",
        r"the result is:?",
        r"final expression:?",
        r"final answer\s*=\s*",
    ]
    for phrase in phrases:
        match = re.search(f"{phrase}(.*)", cell_content, re.IGNORECASE | re.DOTALL)
        if match:
            result = match.group(1).strip()
            first_line = result.splitlines()[0].strip()
            if first_line:
                extracted_candidate = first_line
                break

    # 2. Look for the last line containing "+ C" (for integral problems)
    if not extracted_candidate:
        try:
            last_match_pos = -1
            for match in re.finditer(r"\+\s*C", cell_content, re.IGNORECASE):
                last_match_pos = match.start()

            if last_match_pos != -1:
                line_start = cell_content.rfind('', 0, last_match_pos) + 1
                line_end = cell_content.find('', line_start)
                if line_end == -1:
                    line_end = len(cell_content)
                
                answer_line = cell_content[line_start:line_end].strip()
                if answer_line:
                    extracted_candidate = answer_line
        except Exception:
            pass

    # 3. Look for content within the last pair of quotes
    if not extracted_candidate:
        try:
            quoted_items = re.findall(r'"([^"]*)"|\'([^\']*)\'', cell_content)
            all_quotes = [item for tpl in quoted_items for item in tpl if item]
            if all_quotes:
                extracted_candidate = all_quotes[-1].strip()
        except Exception:
            pass

    # POST-PROCESSING: Prune "integral = " part if an answer candidate was found
    if extracted_candidate:
        processed_answer = _post_process_equals_sign(extracted_candidate)
        if processed_answer:
            return processed_answer

    # 4. Fallback: Last non-empty line
    lines = [line.strip() for line in cell_content.strip().splitlines() if line.strip()]
    if lines:
        return lines[-1]

    # 5. Final Fallback: Return original content
    return cell_content

def run_extraction():
    """
    Main function to run the answer extraction process.
    """
    print("--- Starting LLM Response Extraction ---")
    
    # 1. Load and Validate Configuration
    input_path_str = EXTRACT_CONFIG.get("input_file")
    output_filename = EXTRACT_CONFIG.get("output_file")
    sheets_to_process = EXTRACT_CONFIG.get("sheets_to_process", []) # New optional setting

    if not all([input_path_str, output_filename]):
        print("Error: 'input_file' and 'output_file' must be set in extract_config.py")
        return

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_path_str
    intermediate_dir = script_dir / "intermediate"
    intermediate_dir.mkdir(exist_ok=True)
    output_path = intermediate_dir / output_filename

    if not input_path.exists():
        print(f"Error: Input file not found at '{input_path}'")
        return

    print(f"Loading raw results from: {input_path.name}")

    # 2. Determine which sheets to process
    try:
        xls = pd.ExcelFile(input_path, engine='openpyxl')
        all_sheet_names = xls.sheet_names
        
        if sheets_to_process:
            # Filter to only process specified sheets
            final_sheets_to_process = [s for s in sheets_to_process if s in all_sheet_names]
            missing_sheets = set(sheets_to_process) - set(final_sheets_to_process)
            if missing_sheets:
                print(f"Warning: The following specified sheets were not found in the input file and will be skipped: {list(missing_sheets)}")
        else:
            # If list is empty, process all sheets
            final_sheets_to_process = all_sheet_names
            
        print(f"Found {len(final_sheets_to_process)} sheets to process.")

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # 3. Set up ExcelWriter for either creating or updating the file
    write_mode = 'a' if output_path.exists() else 'w'
    if_exists_strategy = 'replace' if write_mode == 'a' else None
    
    print(f"Output file '{output_path.name}' will be {'updated' if write_mode == 'a' else 'created'}.")

    try:
        with pd.ExcelWriter(output_path, engine='openpyxl', mode=write_mode, if_sheet_exists=if_exists_strategy) as writer:
            for sheet in final_sheets_to_process:
                print(f"  -> Extracting answers from sheet: '{sheet}'...")
                try:
                    df = pd.read_excel(xls, sheet_name=sheet, header=1)
                    
                    if 'iteration' not in [str(c).lower() for c in df.columns]:
                        print(f"     - Skipping sheet '{sheet}' (no 'Iteration' column).")
                        continue

                    iteration_col_name = [c for c in df.columns if c.lower() == 'iteration'][0]
                    extracted_df = df[[iteration_col_name]].copy()
                    data_columns = [c for c in df.columns if c.lower() != 'iteration']
                    
                    for col in data_columns:
                        extracted_df[col] = df[col].apply(extract_answer)
                    
                    # This will overwrite the sheet if it exists, or create it if it doesn't
                    extracted_df.to_excel(writer, sheet_name=sheet, index=False)

                except Exception as e:
                    print(f"     - Error processing sheet '{sheet}': {e}")
                    continue
        
        # Manually save if in append mode to ensure changes are written
        if write_mode == 'a':
            writer.save()

    except Exception as e:
        print(f"An error occurred while writing to the Excel file: {e}")
        return
    
    print(f"\n--- Extraction Complete ---")
    print(f"Results saved to: '{output_path}'")

if __name__ == "__main__":
    run_extraction()
