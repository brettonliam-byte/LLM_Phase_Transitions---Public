import pandas as pd
import json
import os
import glob
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(PROJECT_ROOT, 'OpenrouterAPIcommand', 'llm_outputs')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'OpenrouterAPIcommand', 'combined_responses.xlsx')

def process_responses():
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory not found at {INPUT_DIR}")
        return

    # Find all JSON response files
    json_pattern = os.path.join(INPUT_DIR, '*_response_*.json')
    files = glob.glob(json_pattern)
    
    # Sort files by modification time (newest last) or name
    # Sorting by name usually keeps iterations together if timestamps match
    files.sort()

    print(f"Found {len(files)} response files. Processing...")

    data_list = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Basic Metadata
                filename = os.path.basename(file_path)
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))

                # Extract Content
                content = ""
                reasoning = ""
                
                # Check for standard normalized format (new script version)
                if 'normalized_response' in data:
                    content = data['normalized_response'].get('content', '')
                    reasoning = data['normalized_response'].get('reasoning', '')
                # Check for direct OpenAI format (old script version or raw dumps)
                elif 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0]['message'].get('content', '')
                    reasoning = data['choices'][0]['message'].get('reasoning', '')
                # Fallback
                else:
                    content = str(data)

                # Extract Config Details
                config = data.get('config_used', {})
                model = config.get('model', 'Unknown')
                temperature = config.get('temperature', 'N/A')
                
                # Extract Iteration Info
                iteration = data.get('iteration', 1)
                
                entry = {
                    'Model': model,
                    'Iteration': iteration,
                    'Temperature': temperature,
                    'Content': content,
                    'Reasoning': reasoning, # Include reasoning if available (e.g. O1/R1 models)
                    'Filename': filename,
                    'Date': creation_time
                }
                
                data_list.append(entry)
                
        except Exception as e:
            print(f"Skipping {os.path.basename(file_path)}: {e}")

    if not data_list:
        print("No valid data found to export.")
        return

    # Create DataFrame
    df = pd.DataFrame(data_list)

    # Reorder columns nicely
    cols = ['Model', 'Iteration', 'Content', 'Reasoning', 'Temperature', 'Date', 'Filename']
    # Filter columns that actually exist in the dataframe (in case some are missing entirely)
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    # Export to Excel
    try:
        df.to_excel(OUTPUT_FILE, index=False, engine='openpyxl')
        print(f"\nSuccessfully exported {len(df)} rows to:")
        print(f"{OUTPUT_FILE}")
    except PermissionError:
        print(f"\nError: Could not write to {OUTPUT_FILE}.")
        print("Please close the file if it is currently open in Excel and try again.")
    except Exception as e:
        print(f"\nError exporting to Excel: {e}")

if __name__ == "__main__":
    process_responses()
