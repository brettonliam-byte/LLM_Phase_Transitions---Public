# extract_answers_maths.py
# A specialized version of the extraction script that validates for mathematical expressions.

import pandas as pd
import re
from pathlib import Path

try:
    from extract_config import EXTRACT_CONFIG
except ImportError:
    print("Error: Could not import 'EXTRACT_CONFIG' from extract_config.py.")
    EXTRACT_CONFIG = {}

# Whitelist for common mathematical function names and single letters often used as variables
MATH_FUNCTION_NAMES = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'exp', 'd', 'dx', 'dy', 'dt', 'pi', 'e', 'x', 'y', 'z', 'a', 'b', 'c', 'k', 'n'}

def is_likely_math_expression(text):
    """
    Checks if a string is likely a mathematical expression.
    It must contain at least one common math operator or numbers.
    It also checks for an excessive amount of non-math-related words.
    """
    if not text or len(text.strip()) < 3: # Too short to be a meaningful expression
        return False
    
    # 1. Check for presence of essential math-related characters
    # This regex looks for common operators, numbers, or typical math functions
    math_char_pattern = re.compile(r'[\d\+\-\*\/\^=()\[\]]|sin|cos|tan|log|ln|exp', re.IGNORECASE)
    if not math_char_pattern.search(text):
        return False # No math characters found

    # 2. Check for an excessive amount of non-math words (prose detection)
    # Split by non-alphanumeric characters to get "words"
    words = re.findall(r'[a-zA-Z]+', text)
    prose_word_count = 0
    for word in words:
        if word.lower() not in MATH_FUNCTION_NAMES:
            prose_word_count += 1
            
    # If there are more than 2 prose words, it's likely not a pure math expression
    if prose_word_count > 2:
        return False
    
    # 3. Final check for density of letters vs total length (to catch very long prose with few math chars)
    # This is a fallback to catch very long prose with just one math char.
    total_alphanum = sum(1 for char in text if char.isalnum())
    if total_alphanum > 0:
        letters_not_math_func = sum(1 for char in text if char.isalpha() and char.lower() not in MATH_FUNCTION_NAMES)
        if letters_not_math_func / total_alphanum > 0.5: # If more than 50% of alphanum chars are non-math letters
            return False

    return True

def _post_process_equals_sign(text):
    """
    If the text contains an equals sign, extracts the part after the last equals sign.
    """
    if not isinstance(text, str) or '=' not in text:
        return text.strip()
    return text.rsplit('=', 1)[-1].strip()

def salvage_math_expression(text):
    """
    Attempts to find a pure mathematical expression within a larger string.
    This is used when an initial candidate fails the full math expression check.
    """
    if not text:
        return ""

    # Strategy 1: Look for strings within quotes inside the text
    try:
        quoted_items = re.findall(r'"([^"]*)"|\'([^\']*)\'', text)
        all_quotes = [item for tpl in quoted_items for item in tpl if item]
        # Iterate from last to first to find the latest valid one
        for quote in reversed(all_quotes):
            # Apply equals sign pruning before validation
            processed_quote = _post_process_equals_sign(quote.strip())
            if is_likely_math_expression(processed_quote):
                return processed_quote
    except Exception:
        pass

    # Strategy 2: Look for a substring around "+ C"
    try:
        if "+ c" in text.lower():
            # Find all occurrences of "+ C"
            matches = list(re.finditer(r"\+\s*C", text, re.IGNORECASE))
            if matches:
                # Take the last match and try to extract the expression around it
                # For now, let's just try to get the line containing it, then process it.
                last_match = matches[-1]
                line_start = text.rfind('\n', 0, last_match.start()) + 1
                line_end = text.find('\n', line_start)
                if line_end == -1: line_end = len(text)
                
                line_containing_c = text[line_start:line_end].strip()
                # Apply equals sign pruning and validation
                processed_line = _post_process_equals_sign(line_containing_c)
                if is_likely_math_expression(processed_line):
                    return processed_line
    except Exception:
        pass
    
    # Strategy 3: Look for a standalone math expression pattern (e.g., something = result)
    # This is similar to _post_process_equals_sign but actively *finds* the pattern
    # It attempts to capture a final expression that contains an equals sign.
    match = re.search(r'=(.*)', text) # Capture everything after an equals sign
    if match:
        potential_math = match.group(1).strip()
        if is_likely_math_expression(potential_math):
            return potential_math

    return "" # No math expression could be salvaged

def extract_answer(cell_content):
    """
    Tries to extract a plausible mathematical expression from a cell's content.
    """
    if not isinstance(cell_content, str) or not cell_content.strip():
        return ""

    # Heuristics to find initial candidate strings
    candidates = []

    # 1. Keyword phrases
    phrases = [
        r"the final answer is:?", r"the solution is:?", r"the result is:?",
        r"final expression:?", r"final answer\s*=\s*",
    ]
    for phrase in phrases:
        match = re.search(f"{phrase}(.*)", cell_content, re.IGNORECASE | re.DOTALL)
        if match:
            candidates.append(match.group(1).strip().splitlines()[0].strip()) # Take first line after phrase

    # 2. Last line containing "+ C"
    try:
        last_match_pos = -1
        for match in re.finditer(r"\+\s*C", cell_content, re.IGNORECASE):
            last_match_pos = match.start()
        if last_match_pos != -1:
            line_start = cell_content.rfind('\n', 0, last_match_pos) + 1
            line_end = cell_content.find('\n', line_start)
            if line_end == -1: line_end = len(cell_content)
            candidates.append(cell_content[line_start:line_end].strip())
    except Exception: pass

    # 3. Last quoted text
    try:
        quoted_items = re.findall(r'"([^"]*)"|\'([^\']*)\'', cell_content)
        all_quotes = [item for tpl in quoted_items for item in tpl if item]
        if all_quotes:
            candidates.append(all_quotes[-1].strip())
    except Exception: pass

    # 4. Fallback: Last non-empty line
    lines = [line.strip() for line in cell_content.strip().splitlines() if line.strip()]
    if lines:
        candidates.append(lines[-1])


    # Process candidates: apply equals-pruning, validate, and salvage if needed
    for candidate in candidates:
        if not candidate: continue
        
        processed_candidate = _post_process_equals_sign(candidate)
        
        # First attempt: validate the processed candidate directly
        if is_likely_math_expression(processed_candidate):
            return processed_candidate
        
        # Second attempt: if direct validation fails, try to salvage a math expression from it
        salvaged = salvage_math_expression(processed_candidate)
        if salvaged: # If a math expression was successfully salvaged
            return salvaged

    # If no valid math expression was found after all heuristics and salvaging, return a blank string
    return ""

def run_extraction():
    """
    Main function to run the answer extraction process.
    """
    print("--- Starting LLM Response Extraction (MATHS VERSION) ---")
    
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
    
    base, ext = Path(output_filename).stem, Path(output_filename).suffix
    maths_output_filename = f"{base}_maths{ext}"
    output_path = intermediate_dir / maths_output_filename

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
    
    print(f"\n--- Maths Extraction Complete ---")
    print(f"Results saved to: '{output_path}'")

if __name__ == "__main__":
    run_extraction()
