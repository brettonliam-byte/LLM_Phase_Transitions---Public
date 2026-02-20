import pandas as pd
import json
import os
import sys
import numpy as np

# Encoding fix for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def extract_and_analyze_logprobs(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    experiments = data.get('experiments', [])
    model = data.get('config', {}).get('model', 'Unknown')
    
    raw_rows = []
    candidate_rows = [] # To store all top 5 candidates separately for aggregation
    
    print(f"Analyzing logprob data for {model}...")

    for exp in experiments:
        temp = exp.get('temperature')
        for iter_data in exp.get('iterations', []):
            iteration = iter_data.get('iteration')
            logprobs_container = iter_data.get('logprobs')
            
            if not logprobs_container:
                continue
                
            content = logprobs_container.get('content', [])
            is_thinking = False
            response_pos = 0 

            for entry in content:
                token = entry.get('token', '')
                
                if "<think>" in token:
                    is_thinking = True
                    continue
                if "</think>" in token:
                    is_thinking = False
                    continue
                
                if is_thinking:
                    continue

                logprob = entry.get('logprob', 0)
                top_lps = entry.get('top_logprobs', []) 

                # 1. Main row (Chosen Token)
                row = {
                    "Temperature": temp,
                    "Iteration": iteration,
                    "Pos": response_pos,
                    "Token": token,
                    "Logprob": logprob,
                    "Is_Chosen": True
                }
                raw_rows.append(row)

                # 2. Candidate rows (Aggregate ALL candidates including the chosen one for stats)
                # We include the chosen token in the candidate list to get its full stats
                candidate_rows.append({
                    "Temperature": temp,
                    "Pos": response_pos,
                    "Token": token,
                    "Logprob": logprob
                })

                for t_entry in top_lps:
                    t_token = t_entry.get('token', '')
                    if t_token == token: continue # Already added as chosen
                    candidate_rows.append({
                        "Temperature": temp,
                        "Pos": response_pos,
                        "Token": t_token,
                        "Logprob": t_entry.get('logprob', -99.0)
                    })
                
                response_pos += 1

    if not raw_rows:
        print("No valid logprob data found after filtering.")
        return

    # Convert to DataFrames
    df_raw = pd.DataFrame(raw_rows)
    df_candidates = pd.DataFrame(candidate_rows)
    
    output_path = json_path.replace('.json', '_token_analysis.xlsx')
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Sheet 1: The Raw Log (Every token in every iteration)
        df_raw.to_excel(writer, sheet_name='Iteration_Log', index=False)
        
        # Sheet 2: Token Candidate Analysis (The "Particular Token" Mean)
        # Group by Pos, Temperature, and Token to find the mean logprob of EACH candidate
        token_stats = df_candidates.groupby(['Pos', 'Temperature', 'Token'])['Logprob'].agg(['mean', 'std', 'count']).reset_index()
        token_stats.columns = ['Pos', 'Temperature', 'Token_Candidate', 'Mean_Logprob', 'Std_Dev', 'Iteration_Count']
        
        # Sort so most likely tokens for each position/temp are at the top
        token_stats = token_stats.sort_values(by=['Pos', 'Temperature', 'Mean_Logprob'], ascending=[True, True, False])
        token_stats.to_excel(writer, sheet_name='Top_Token_Stats', index=False)
        
        # Sheet 3: Confidence Decay (Mean Logprob of CHOSEN token per position/temp)
        confidence_decay = df_raw.groupby(['Pos', 'Temperature'])['Logprob'].mean().unstack(level=1)
        confidence_decay.to_excel(writer, sheet_name='Confidence_Decay_Grid')
        
        # Sheet 4: Experiment Summary (Mean confidence per Temperature)
        temp_summary = df_raw.groupby('Temperature')['Logprob'].agg(['mean', 'std', 'count']).reset_index()
        temp_summary.columns = ['Temperature', 'Grand_Mean_Logprob', 'Std_Dev', 'Total_Tokens']
        temp_summary.to_excel(writer, sheet_name='Temperature_Summary', index=False)

    print(f"\nAnalysis complete! Data saved to: {output_path}")
    print("Key Analysis Sheets:")
    print("  - Top_Token_Stats: Mean logprobs for every token candidate at every position.")
    print("  - Confidence_Decay_Grid: Quick view of how confidence drops as temperature rises.")
    print("  - Iteration_Log: The raw response data for every single iteration.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_token_logprobs.py <path_to_results_json>")
    else:
        extract_and_analyze_logprobs(sys.argv[1])
