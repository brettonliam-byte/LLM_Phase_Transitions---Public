import pandas as pd
import json
import os
import sys

# Encoding fix for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def export_to_excel(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    experiments = data.get('experiments', [])
    model = data.get('config', {}).get('model', 'Unknown Model')
    prompt = data.get('config', {}).get('user_prompt', 'Unknown Prompt')

    excel_path = json_path.replace('.json', '.xlsx')
    
    # We'll create multiple sheets for the Excel file
    # Sheet 1: Metadata
    metadata_df = pd.DataFrame([
        ["Model", model],
        ["Prompt", prompt],
        ["Timestamp", data.get('timestamp', '')],
        ["Iterations per Temp", data.get('config', {}).get('N', 1)],
    ])

    # Sheet 2: All Responses (Transposed: Rows=Iteration, Cols=Temperature)
    # We want a summary table like the original framework
    summary_data = {}
    
    for exp in experiments:
        temp = exp.get('temperature')
        col_name = f"Temp_{temp:.2f}"
        responses = [it.get('text', '') for it in exp.get('iterations', [])]
        summary_data[col_name] = responses

    # Find max length to align iterations
    max_len = max([len(v) for v in summary_data.values()]) if summary_data else 0
    for k in summary_data:
        while len(summary_data[k]) < max_len:
            summary_data[k].append("")
            
    summary_df = pd.DataFrame(summary_data)
    summary_df.index.name = "Iteration"
    summary_df.index += 1

    # Sheet 3...N: Logprob detailed view for EACH temperature if needed,
    # but that might be TOO much data. Let's create a sheet for 'Average Logprobs' or 'Sample'

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        metadata_df.to_excel(writer, sheet_name='Metadata', index=False, header=False)
        summary_df.to_excel(writer, sheet_name='Responses Summary')
        
        # Optionally, for each temperature, create a sheet with token-level logprobs for the FIRST iteration
        for exp in experiments:
            temp = exp.get('temperature')
            first_iter = exp.get('iterations', [])[0] if exp.get('iterations') else None
            
            if first_iter and first_iter.get('logprobs'):
                # Extract token logprobs
                # format is usually: { content: [ { token: "...", logprob: ..., top_logprobs: [...] } ] }
                lp_data = first_iter['logprobs']
                tokens_list = []
                
                # Handling OpenAI/OpenRouter format
                content_list = lp_data.get('content', [])
                for entry in content_list:
                    token = entry.get('token', '')
                    logprob = entry.get('logprob', 0)
                    top_lps = entry.get('top_logprobs', [])
                    
                    row = {"Token": token, "Logprob": logprob}
                    for idx, top in enumerate(top_lps):
                        row[f"Top_{idx+1}_Token"] = top.get('token', '')
                        row[f"Top_{idx+1}_Logprob"] = top.get('logprob', 0)
                    tokens_list.append(row)
                
                if tokens_list:
                    tokens_df = pd.DataFrame(tokens_list)
                    sheet_name = f"Logprobs_T{temp:.2f}_I1"[:31] # Excel limit
                    tokens_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Successfully exported results to: {excel_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_logprobs_to_excel.py <path_to_results_json>")
    else:
        export_to_excel(sys.argv[1])
