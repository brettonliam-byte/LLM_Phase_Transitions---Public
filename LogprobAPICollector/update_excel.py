import pandas as pd
import sys
import json
import os
import openpyxl

# Fix for Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

def update_excel(temp_data_path):
    # 1. Load the new data
    try:
        with open(temp_data_path, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
    except Exception as e:
        print(f"Error loading temp json: {e}")
        return

    excel_path = new_data.get('excel_file')
    responses = new_data.get('responses', [])
    prompt = new_data.get('prompt', '')
    model = new_data.get('model', '')
    timestamp = new_data.get('timestamp', '')

    if not excel_path:
        print("Error: No excel_file path provided in config.")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(excel_path)), exist_ok=True)

    # 2. Load or Create DataFrame
    if os.path.exists(excel_path):
        try:
            df = pd.read_excel(excel_path, engine='openpyxl')
        except Exception as e:
            print(f"Error reading existing Excel file: {e}")
            return
    else:
        df = pd.DataFrame()

    # 3. Construct the new column name
    # We need a unique header for this run. 
    # Let's use "Model | Date | ShortPrompt"
    #short_prompt = (prompt[:30] + '..') if len(prompt) > 30 else prompt
    # Sanitize column name slightly to avoid huge headers
    #short_prompt = short_prompt.replace('\n', ' ')
    
    col_name = f"{model} | {timestamp} | {prompt}"
    
    # Handle duplicate column names if they occur (rare with timestamp)
    if col_name in df.columns:
        col_name = f"{col_name}_{len(df.columns)}"

    # 4. Create the Series for the new column
    # The responses are a list. 
    new_series = pd.Series(responses, name=col_name)

    # 5. Append to DataFrame
    # If df is empty, this just becomes the first column.
    # If df exists, we join. Since indices might not match (length of runs differ), 
    # pandas concat with axis=1 handles this by aligning on index (0, 1, 2...).
    # We must reset index of new_series to ensure it starts at 0.
    new_series.reset_index(drop=True, inplace=True)
    
    # Concatenate
    df = pd.concat([df, new_series], axis=1)

    # 6. Save back to Excel
    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"Successfully appended {len(responses)} iterations to column:")
        print(f"'{col_name}'")
        print(f"in file: {excel_path}")
    except PermissionError:
        print(f"Error: Permission denied writing to {excel_path}.")
        print("Please close the file if it is open in Excel.")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_excel.py <path_to_temp_json>")
    else:
        update_excel(sys.argv[1])
