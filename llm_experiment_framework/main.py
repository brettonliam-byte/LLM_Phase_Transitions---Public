import pandas as pd
import numpy as np
import time
import os
import re
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from llm_services import get_llm_response

# Import the single source of truth for configuration
try:
    from config import EXPERIMENTS
except ImportError:
    print("Error: Could not import 'EXPERIMENTS' from config.py. Please ensure the file exists.")
    EXPERIMENTS = []

# Load .env from the root of the repository
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    print(f"Loading environment variables from {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Excel has a hard limit of 32,767 characters per cell.
EXCEL_CHAR_LIMIT = 32700 

def generate_unique_sheet_name(model_full_name, prompt):
    """
    Generates a unique and valid Excel sheet name (max 31 chars).
    Structure: [ShortModel]_[PromptSnippet]_[Hash]
    """
    # 1. Clean up model name (take the part after the last slash)
    model_part = model_full_name.split('/')[-1]
    model_part = re.sub(r"[^a-zA-Z0-9]", "", model_part)[:10]
    
    # 2. Clean up prompt snippet
    prompt_snippet = re.sub(r"[^a-zA-Z0-9]", "", prompt)[:12]
    
    # 3. Generate a short hash of the full prompt to guarantee uniqueness
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:4]
    
    # 4. Combine
    sheet_name = f"{model_part}_{prompt_snippet}_{prompt_hash}"
    
    # 5. Final safety check for Excel restricted characters
    invalid_chars = r"[:\\/?*\[\]]"
    sheet_name = re.sub(invalid_chars, "_", sheet_name)
    
    return sheet_name[:31]

def sanitize_sheet_name(name):
    """
    Legacy sanitizer - kept for backward compatibility if needed.
    """
    invalid_chars = r"[:\\/?*\[\]]"
    sanitized = re.sub(invalid_chars, "_", name)
    return sanitized[:31]

def run_experiments():
    """
    Runs experiments from config.py.
    
    Transposed Structure:
    - Rows: Iterations (Iteration 1, 2, 3...)
    - Columns: Temperatures (Temp_0.00, Temp_0.10...)
    """
    if not EXPERIMENTS:
        print("No experiments found in config.py.")
        return

    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    print(f"Found {len(EXPERIMENTS)} experiments in queue.")

    for i, experiment in enumerate(EXPERIMENTS):
        prompt = experiment.get("prompt")
        model_full_name = experiment.get("model")
        temp_range = experiment.get("temperature_range")
        iterations = experiment.get("iterations", 1)
        output_filename = experiment.get("output_file", "results.xlsx")

        if not prompt or not model_full_name or not temp_range:
            continue

        if not os.path.isabs(output_filename):
            output_file = os.path.join(results_dir, output_filename)
        else:
            output_file = output_filename

        service, model_name = model_full_name.split('/', 1)

        # --- Resumability Check with Unique Naming ---
        sheet_name = generate_unique_sheet_name(model_full_name, prompt)
        
        if os.path.exists(output_file):
            try:
                with pd.ExcelFile(output_file, engine='openpyxl') as xls:
                    if sheet_name in xls.sheet_names:
                        print(f"\n[{i+1}/{len(EXPERIMENTS)}] Skipping: {sheet_name} (Already exists in {output_filename})")
                        continue
            except Exception as e:
                print(f"Warning: Could not read existing file {output_filename} to check sheets: {e}")

        print(f"\n[{i+1}/{len(EXPERIMENTS)}] Starting Experiment: {model_full_name}")
        print(f"   Prompt Snippet: {prompt[:50]}...")
        print(f"   Target: {os.path.basename(output_file)} -> Sheet: {sheet_name}")

        # --- 1. Collect Data in Transposed Format ---
        temps = np.arange(temp_range["start"], temp_range["end"] + temp_range["step"], temp_range["step"])
        
        transposed_data = {
            "Iteration": list(range(1, iterations + 1))
        }

        for temp in temps:
            print(f"   Running Temp {temp:.2f}...")
            temp_column_responses = []
            
            for iter_idx in range(iterations):
                while True: # Interactive Retry Loop
                    try:
                        response = get_llm_response(service, prompt, model_name, temp)
                        
                        # --- Excel Character Limit Check ---
                        if len(response) > EXCEL_CHAR_LIMIT:
                            print(f"      Warning: Iteration {iter_idx+1} exceeded Excel character limit ({len(response)} chars). Truncating start.")
                            # Truncate the beginning, keep the end.
                            # We leave a small buffer and a label
                            response = "[TRUNCATED START]... " + response[-(EXCEL_CHAR_LIMIT - 50):]
                            
                        temp_column_responses.append(response)
                        break
                    except Exception as e:
                        print(f"      Error (Iter {iter_idx+1}): {e}")
                        print("      !!! Experiment Paused due to Error !!!")
                        user_choice = input("      Press [Enter] to RETRY, 's' to SKIP this iteration, or 'q' to QUIT: ").strip().lower()
                        
                        if user_choice == 'q':
                            print("Quitting...")
                            exit()
                        elif user_choice == 's':
                            temp_column_responses.append(f"SKIPPED_ERROR: {e}")
                            break
                
                if service in ['openai', 'anthropic', 'google']:
                    time.sleep(2) 
                else:
                    time.sleep(0.1)
            
            transposed_data[f"Temp_{temp:.2f}"] = temp_column_responses

        df = pd.DataFrame(transposed_data)

        # --- 2. Save to Excel ---
        if os.path.exists(output_file):
            mode = 'a'
            if_sheet_exists = 'replace'
        else:
            mode = 'w'
            if_sheet_exists = None

        try:
            with pd.ExcelWriter(output_file, mode=mode, engine='openpyxl', if_sheet_exists=if_sheet_exists) as writer:
                # Write Model and Prompt to the first row (A1 and B1)
                info_header = pd.DataFrame([[f"Model: {model_full_name}", f"Prompt: {prompt}"]])
                info_header.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=0, startcol=0)
                
                # Write the main data starting at B2 (row 1, col 1)
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, startcol=1)
            print(f"   Saved to sheet: '{sheet_name}' in {os.path.basename(output_file)}")
        except Exception as e:
            print(f"   Error saving: {e}")

    print("\nAll experiments completed.")

if __name__ == "__main__":
    run_experiments()
