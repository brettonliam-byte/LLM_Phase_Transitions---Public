import json
import re
import os

# Paths
# Note: JSON path kept for reference but sweep data is ignored per request.
INTEGRAL_MD_PATH_1 = r"LLM_Phase_Transitions/experiments/integral_test_benchmark/Misc/integral_test_benchmark(legacy)/Integral_Test_Analysis.md"
INTEGRAL_MD_PATH_2 = r"LLM_Phase_Transitions/experiments/integral_test_benchmark/Output/Integral_Test_2_Analysis.md"
OUTPUT_HTML_PATH = r"LLM_Phase_Transitions/results_viz/integral_visualization.html"

def get_nuanced_score(status, notes):
    """
    Assigns a score based on status and qualitative notes.
    """
    status = status.lower()
    notes = notes.lower()
    
    if "correct" in status or "success" in status:
        return 100
    
    if "partial" in status:
        if "substitute" in notes or "format" in notes:
            return 80 # Good math, bad finishing
        return 50 # Partial credit
        
    if "incorrect" in status or "failed" in status:
        if "sign error" in notes:
            return 75 # Arithmetic slip, logic mostly sound
        if "formatting" in notes:
            return 80
        # Fundamental errors
        return 0
        
    return 0

def parse_integral_md(file_path):
    print(f"Parsing Integral MD from {file_path}...")
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Relaxed Regex to capture: | Model | Status | [Notes]
        # Matches lines starting with | **...
        row_pattern = re.compile(r'\|\s*\*\*(.*?)\*\*\s*\|\s*([^|]+)(?:\|\s*([^|]*))?')
        
        for line in lines:
            match = row_pattern.search(line)
            if match:
                model_name = match.group(1).strip()
                status_raw = match.group(2).strip()
                notes_raw = match.group(3).strip() if match.group(3) else ""
                
                # Determine Score
                score = get_nuanced_score(status_raw, notes_raw)
                
                # Determine Grade/Label for display
                if score == 100: grade = "Pass"
                elif score >= 70: grade = "Minor Error"
                elif score >= 40: grade = "Partial"
                else: grade = "Fail"

                # Infer size from name
                size = 0
                size_match = re.search(r'(\d+)[Bb]', model_name)
                if not size_match:
                     # Heuristics for models without size in name
                     if "2512" in model_name: size = 22 # Approx for Devstral/Mistral
                     elif "Mini" in model_name: size = 4
                     elif "Lite" in model_name: size = 2
                     elif "K2" in model_name: size = 200
                     elif "Flash" in model_name: size = 50
                     elif "Fast" in model_name: size = 50
                     elif "Air" in model_name: size = 70
                else:
                    size = int(size_match.group(1))

                data.append({
                    "model": model_name,
                    "size": size,
                    "score": score,
                    "grade": grade,
                    "notes": notes_raw
                })

    except Exception as e:
        print(f"Error parsing Integral MD: {e}")
    return data

def generate_html(int_md_data_1, int_md_data_2):
    print("Generating HTML...")
    
    # Merge MD data, filtering duplicates
    all_md_models = {}
    for m in int_md_data_1 + int_md_data_2:
        all_md_models[m['model']] = m
    
    combined_md_list = list(all_md_models.values())

    payload = {
        "integral_models": combined_md_list
    }
    
    html_part1 = """
<!DOCTYPE html>
<html>
<head>
    <title>Integral Test Visualizations</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f9; }
        .chart-container { background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; }
    </style>
</head>
<body>
    <h1>Integral Test Experiments</h1>
    <p>Performance on solving $\int \frac{\tan^3(\ln x)}{x} dx$.</p>
    <p><strong>Scoring Criteria:</strong> 100 = Correct, 80 = Correct logic but minor format/substitution oversight, 75 = Sign error only, 0 = Fundamental mathematical error.</p>

    <div class="chart-container">
        <h2>Model Performance vs. Parameter Size</h2>
        <div id="int_scatter"></div>
    </div>
    
    <div class="chart-container">
        <h2>Detailed Model Ranking</h2>
        <div id="int_bar"></div>
    </div>

    <script>
"""
    
    data_assignment = f"        const data = {json.dumps(payload)};"

    html_part2 = """
        // --- Integral Test Charts ---

        // 1. Scatter: Size vs Nuanced Score
        const intScatterX = [];
        const intScatterY = [];
        const intScatterText = [];
        const intScatterColor = [];
        
        data.integral_models.forEach(m => {
            if(m.size > 0) {
                intScatterX.push(m.size);
                intScatterY.push(m.score);
                // Create hover text with notes
                const hover = m.model + '<br>' + m.grade + '<br>' + (m.notes ? m.notes.substring(0, 50) + '...' : '');
                intScatterText.push(hover);
                
                // Color based on score bucket
                if (m.score === 100) intScatterColor.push('#2ca02c'); // Green
                else if (m.score >= 70) intScatterColor.push('#ff7f0e'); // Orange
                else intScatterColor.push('#d62728'); // Red
            }
        });

        const traceIntScatter = {
            x: intScatterX,
            y: intScatterY,
            mode: 'markers',
            text: intScatterText, // hover text
            hoverinfo: 'text',
            marker: { size: 14, color: intScatterColor, line: {color: 'black', width: 1} }
        };

        Plotly.newPlot('int_scatter', [traceIntScatter], {
            title: 'Integral Test: Parameter Size vs Nuanced Score',
            xaxis: { title: 'Parameter Size (Billions)', type: 'log' },
            yaxis: { title: 'Score (0-100)', range: [-5, 105] },
            hovermode: 'closest'
        });
        
        // 2. Bar Chart: Model List Sorted
        const sortedModels = [...data.integral_models].sort((a,b) => b.score - a.score);
        
        const traceBar = {
            x: sortedModels.map(m => m.model),
            y: sortedModels.map(m => m.score),
            text: sortedModels.map(m => m.grade),
            type: 'bar',
            marker: { 
                color: sortedModels.map(m => {
                    if (m.score === 100) return '#2ca02c';
                    if (m.score >= 70) return '#ff7f0e';
                    return '#d62728';
                })
            }
        };
        
        Plotly.newPlot('int_bar', [traceBar], {
            title: 'Model Performance Ranking',
            yaxis: { title: 'Score' },
            margin: { b: 150 }
        });

    </script>
</body>
</html>
"""
    
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_part1)
        f.write(data_assignment)
        f.write(html_part2)
    print(f"Generated HTML at {OUTPUT_HTML_PATH}")

if __name__ == "__main__":
    i_md_1 = parse_integral_md(INTEGRAL_MD_PATH_1)
    i_md_2 = parse_integral_md(INTEGRAL_MD_PATH_2)
    
    generate_html(i_md_1, i_md_2)
