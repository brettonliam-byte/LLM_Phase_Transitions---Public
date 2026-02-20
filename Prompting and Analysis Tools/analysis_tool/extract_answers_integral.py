# extract_answers_integral.py
# A specialized version of the extraction script designed for integral calculus problems.
# It uses anchor-based extraction, specifically looking for "+ C" as an end anchor.

import pandas as pd
import re
from pathlib import Path

try:
    from extract_config import EXTRACT_CONFIG
except ImportError:
    print("Error: Could not import 'EXTRACT_CONFIG' from extract_config.py.")
    EXTRACT_CONFIG = {}

def extract_answer(cell_content):
    """
    Tries to extract a plausible integral calculus expression by finding start and end anchors.
    Prioritizes answers ending with "+ C".
    """
    if not isinstance(cell_content, str) or not cell_content.strip():
        return ""

    # --- Anchor-Based Extraction Logic ---

    # 1. Find the End Anchor: The last occurrence of "+ C". This is essential for integrals.
    end_anchor_pattern = r"\+\s*C"
    end_matches = list(re.finditer(end_anchor_pattern, cell_content, re.IGNORECASE))
    if not end_matches:
        # If no "+ C" is found, we cannot be confident this is an integral answer. Return blank.
        return ""
    
    last_end_match = end_matches[-1]
    end_pos = last_end_match.end()

    # 2. Find the Start Anchor: Look for common preceding keywords or symbols.
    # We search in the substring *before* the "+ C" we found.
    search_area = cell_content[:last_end_match.start()]
    
    start_anchor_patterns = [
        r"=\s*$",                # An equals sign right at the end of a phrase (e.g., "... = ")
        r"is\s*:$",              # "is:"
        r"is\s*$",               # "is"
        r"get\s*$",              # "get"
        r"have\s*$",             # "have"
        r"solution is\s*$",      # "solution is"
    ]
    
    start_pos = -1
    for pattern in start_anchor_patterns:
        matches = list(re.finditer(pattern, search_area, re.IGNORECASE | re.MULTILINE))
        if matches:
            # Take the match that is closest to our end position (i.e., the last one found in search_area)
            current_start_pos = matches[-1].end()
            if current_start_pos > start_pos: # Prefer anchors closer to the actual expression
                start_pos = current_start_pos
    
    # If no specific keyword anchor was found, try to find the start of the line.
    if start_pos == -1:
        # Find the start of the line where our expression likely begins.
        # This prevents picking up text from previous lines.
        line_start_before_c = search_area.rfind('\n') + 1
        start_pos = line_start_before_c

    # 3. Extract and Clean the Final Answer
    # Extract the substring between the determined start and end positions.
    final_expression = cell_content[start_pos:end_pos].strip()

    # Final cleanup: remove any leading/trailing punctuation that isn't part of the math
    # (e.g., a trailing period or leading comma, but not a dot within a number or function).
    final_expression = re.sub(r'^[,\.]?\s*', '', final_expression) # Remove leading comma/period
    final_expression = re.sub(r'\s*[,\.]?$', '', final_expression) # Remove trailing comma/period

    # A final length check to ensure a meaningful expression is returned.
    # "C" or "+ C" alone is not a solution.
    if len(final_expression) > 3 and final_expression.lower() != '+ c':
        return final_expression
    else:
        return ""

def run_extraction():
    """
    Main function to run the answer extraction process.
    """
    print("--- Starting LLM Response Extraction (INTEGRAL VERSION) ---")
    
    input_path_str = EXTRACT_CONFIG.get("input_file")
    output_filename = EXTRACT_CONFIG.get("output_file")
    sheets_to_process = EXTRACT_CONFIG.get("sheets_to_process", [])

    if not all([input_path_str, output_filename]):
        print("Error: 'input_file' and 'output_file' must be set in extract_config.py")
        return

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_path_str
    intermediate_dir = script_dir / "intermediate"
    intermediate_dir.mkdir(exist_ok=True)
    
    # Add _integral suffix to the output file to distinguish it
    base, ext = Path(output_filename).stem, Path(output_filename).suffix
    integral_output_filename = f"{base}_integral{ext}"
    output_path = intermediate_dir / integral_output_filename

    if not input_path.exists():
        print(f"Error: Input file not found at '{input_path}'")
        return

    print(f"Loading raw results from: {input_path.name}")

    try:
        xls = pd.ExcelFile(input_path, engine='openpyxl')
        all_sheet_names = xls.sheet_names
        
        final_sheets_to_process = all_sheet_names
        if sheets_to_process:
            final_sheets_to_process = [s for s in sheets_to_process if s in all_sheet_names]
            missing = set(sheets_to_process) - set(final_sheets_to_process)
            if missing:
                print(f"Warning: Sheets not found and will be skipped: {list(missing)}")
        
        print(f"Found {len(final_sheets_to_process)} sheets to process.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

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
                    
                    extracted_df.to_excel(writer, sheet_name=sheet, index=False)
                except Exception as e:
                    print(f"     - Error processing sheet '{sheet}': {e}")
                    continue
        
        if write_mode == 'a':
            writer.save()
    except Exception as e:
        print(f"An error occurred while writing to the Excel file: {e}")
        return
    
    print(f"\n--- Integral Extraction Complete ---")
    print(f"Results saved to: '{output_path}'")

if __name__ == "__main__":
    run_extraction()
