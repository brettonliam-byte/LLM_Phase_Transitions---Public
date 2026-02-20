# extract_answers.py
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
        return ""

    # --- NEW High-Priority Combined Heuristic ---
    # First, try to find the last quoted string that also contains "+ C"
    best_candidate = ""
    try:
        # Find all content within single or double quotes
        quoted_items = re.findall(r'"([^"]*)"|\'([^\']*)\'', cell_content)
        all_quotes = [item for tpl in quoted_items for item in tpl if item]
        
        # From the quoted strings, find the last one that contains "+ C"
        last_quote_with_c = ""
        for quote in all_quotes:
            if "+ c" in quote.lower():
                last_quote_with_c = quote
        
        if last_quote_with_c:
            # If found, this is our best candidate. Prune it and return.
            processed_answer = _post_process_equals_sign(last_quote_with_c)
            if processed_answer:
                return processed_answer
    except Exception:
        pass # Ignore errors and proceed to fallback heuristics

    # --- Fallback Heuristics (if the above fails) ---

    # 1. Look for specific phrases like "the final answer is:"
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
                # Also apply pruning here
                processed_answer = _post_process_equals_sign(first_line)
                if processed_answer:
                    return processed_answer

    # 2. Look for the last line containing "+ C"
    try:
        last_match_pos = -1
        for match in re.finditer(r"\+\s*C", cell_content, re.IGNORECASE):
            last_match_pos = match.start()
        if last_match_pos != -1:
            line_start = cell_content.rfind('\n', 0, last_match_pos) + 1
            line_end = cell_content.find('\n', line_start)
            if line_end == -1: line_end = len(cell_content)
            answer_line = cell_content[line_start:line_end].strip()
            if answer_line:
                processed_answer = _post_process_equals_sign(answer_line)
                if processed_answer:
                    return processed_answer
    except Exception:
        pass

    # 3. Last non-empty line (final fallback)
    lines = [line.strip() for line in cell_content.strip().splitlines() if line.strip()]
    if lines:
        return lines[-1]

    # 4. If all else fails, return original content
    return cell_content

def run_extraction():
    """
    Main function to run the answer extraction process.
    """
    print("--- Starting LLM Response Extraction ---")

    # 1. Load and Validate Configuration
    input_path_str = EXTRACT_CONFIG.get("input_file")
    output_filename = EXTRACT_CONFIG.get("output_file")

    if not all([input_path_str, output_filename]):
        print("Error: 'input_file' and 'output_file' must be set in extract_config.py")
        return

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / input_path_str
    
    # Ensure the output directory exists
    intermediate_dir = script_dir / "intermediate"
    intermediate_dir.mkdir(exist_ok=True)
    output_path = intermediate_dir / output_filename

    if not input_path.exists():
        print(f"Error: Input file not found at '{input_path}'")
        return

    print(f"Loading raw results from: {input_path.name}")

    # 2. Read the Input Excel File, preserving original sheet order
    try:
        xls = pd.ExcelFile(input_path)
        sheet_names = xls.sheet_names # This list preserves the order from the file
        print(f"Found {len(sheet_names)} sheets to process.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # 3. Process Each Sheet and Write to Output
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet in sheet_names: # Iterating in the original order
            print(f"  -> Extracting answers from sheet: '{sheet}'...")
            try:
                df = pd.read_excel(xls, sheet_name=sheet, header=1)
                
                if 'Iteration' not in df.columns:
                    print(f"     - Skipping sheet '{sheet}' (no 'Iteration' column).")
                    continue

                # Create a new dataframe for the extracted answers
                extracted_df = df[['Iteration']].copy()
                data_columns = [col for col in df.columns if col != 'Iteration']
                
                # Apply the extraction function to all data cells
                for col in data_columns:
                    extracted_df[col] = df[col].apply(extract_answer)
                
                # Write to the new Excel file, using the original sheet name
                extracted_df.to_excel(writer, sheet_name=sheet, index=False)

            except Exception as e:
                print(f"     - Error processing sheet '{sheet}': {e}")
                continue
    
    print(f"\n--- Extraction Complete ---")
    print("A new file has been created with the extracted answers.")
    print(f"Please manually review and clean the data in: '{output_path}'")
    print("After review, update 'analysis_config.py' to use this new file as its input.")

if __name__ == "__main__":
    run_extraction()
