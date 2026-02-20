import json
import re
import os
import csv
import io

# Paths
PHYSICAL_REASONING_PATH = r"LLM_Phase_Transitions/experiments/Physical test/Analysis of Physical Reasoning.txt"
INTEGRAL_JSON_PATH = r"LLM_Phase_Transitions/results_viz/experiment_data.json"
INTEGRAL_MD_PATH = r"LLM_Phase_Transitions/experiments/integral_test_benchmark/Output/Integral_Test_2_Analysis.md"
OUTPUT_HTML_PATH = r"LLM_Phase_Transitions/results_viz/comprehensive_visualization.html"

def parse_physical_reasoning(file_path):
    print(f"Parsing Physical Reasoning from {file_path}...")
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract CSV part
        lines = content.split('\n')
        csv_lines = []
        for line in lines:
            if "Physical Reasoning Test" in line:
                break
            if line.strip():
                csv_lines.append(line)
        
        print(f"Found {len(csv_lines)} CSV lines.")
        
        # Parse using csv module
        csv_content = "\n".join(csv_lines)
        reader = csv.reader(io.StringIO(csv_content))
        
        headers = next(reader, None) # Skip header
        
        for parts in reader:
            if len(parts) >= 3:
                model_name = parts[0].strip()
                shape = parts[1].strip()
                grade = parts[2].strip()
                desc = parts[3].strip() if len(parts) > 3 else ""
                
                # Extract Size
                size = 0
                size_match = re.search(r'(\d+)[Bb]', model_name)
                if not size_match:
                        size_match = re.search(r'(\d+)[Bb]', desc)
                if not size_match:
                        size_match = re.search(r'-(\d+)[Bb]', model_name.lower())
                
                if size_match:
                    size = int(size_match.group(1))
                elif "Trinty Mini" in model_name or "Mini" in model_name:
                    size = 1 # Guess for small
                
                # Convert Grade to Score
                score = 0
                grade_map = {'A+': 100, 'A': 95, 'A-': 90, 'B+': 88, 'B': 85, 'B-': 80, 
                                'C+': 78, 'C': 75, 'C-': 70, 'D': 60, 'F': 40, 'F-': 20}
                score = grade_map.get(grade, 0)
                
                # Architecture/Purpose
                arch = "Dense"
                if "MoE" in desc:
                    arch = "MoE"
                
                purpose = "General"
                if "Instruct" in model_name: purpose = "Instruct"
                if "Coder" in model_name or "Devstral" in model_name: purpose = "Coding"
                if "Reason" in desc or "Think" in model_name: purpose = "Reasoning"

                data.append({
                    "model": model_name,
                    "shape": shape,
                    "grade": grade,
                    "score": score,
                    "size": size,
                    "arch": arch,
                    "purpose": purpose,
                    "desc": desc
                })
    except Exception as e:
        print(f"Error parsing Physical Reasoning: {e}")
    return data

def parse_integral_json(file_path):
    print(f"Parsing Integral JSON from {file_path}...")
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            
        if "OL3file.xlsx" in json_data:
            ol3 = json_data["OL3file.xlsx"]
            for model_key, results in ol3.items():
                size_match = re.search(r'G(\d+)B', model_key)
                size = int(size_match.group(1)) if size_match else 0
                
                xy_data = []
                max_acc = 0
                for res in results:
                    temp = float(res['temp']) if isinstance(res['temp'], (int, float)) else 0
                    total = res.get('total', 50)
                    correct = res.get('correct', 0)
                    acc = (correct / total) * 100 if total > 0 else 0
                    xy_data.append({"x": temp, "y": acc})
                    if acc > max_acc: max_acc = acc
                
                data.append({
                    "model": f"Gemma {size}B",
                    "size": size,
                    "type": "Sweep",
                    "data": xy_data,
                    "max_acc": max_acc,
                    "arch": "Dense"
                })
    except Exception as e:
        print(f"Error parsing Integral JSON: {e}")
    return data

def parse_integral_md(file_path):
    print(f"Parsing Integral MD from {file_path}...")
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        row_pattern = re.compile(r'|\s*\*\*(.*?)\*\*\s*|\s*(.*?)\s*|')
        
        for line in lines:
            match = row_pattern.search(line)
            if match:
                model_name = match.group(1).strip()
                status_raw = match.group(2).strip()
                
                is_correct = "Correct" in status_raw or "Success" in status_raw
                score = 100 if is_correct else 0
                
                size = 0
                size_match = re.search(r'(\d+)[Bb]', model_name)
                if not size_match:
                     if "2512" in model_name: size = 22
                     elif "Mini" in model_name: size = 1
                     elif "Lite" in model_name: size = 2
                else:
                    size = int(size_match.group(1))

                data.append({
                    "model": model_name,
                    "size": size,
                    "score": score,
                    "status": status_raw
                })

    except Exception as e:
        print(f"Error parsing Integral MD: {e}")
    return data

def generate_html(phys_data, int_json_data, int_md_data):
    print("Generating HTML...")
    payload = {
        "physical": phys_data,
        "integral_sweep": int_json_data,
        "integral_models": int_md_data
    }
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LLM Experiment Visualizations</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{ font-family: sans-serif; margin: 20px; background-color: #f4f4f9; }}
        .chart-container {{ background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #333; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 800px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <h1>LLM Phase Transition Experiments</h1>
    
    <div class="chart-container">
        <h2>Physical Reasoning: Helicopter Cable Problem</h2>
        <p>Model performance grading based on deriving the correct "Straight Line" solution vs misconceptions (Catenary, Spiral, etc.).</p>
        <div id="phys_bar"></div>
        <div id="phys_scatter"></div>
    </div>

    <div class="chart-container">
        <h2>Integral Test: Symbolic Integration</h2>
        <p>Performance on solving $\\int \\frac{{\\tan^3(\\ln x)}}{{x}} dx$.</p>
        <div class="grid">
            <div id="int_sweep"></div>
            <div id="int_scatter"></div>
        </div>
    </div>

    <script>
        const data = {json.dumps(payload)};

        // --- Physical Reasoning Charts ---
        
        // 1. Bar Chart: Grades
        const physSorted = [...data.physical].sort((a, b) => b.score - a.score);
        const tracePhysBar = {{
            x: physSorted.map(d => d.model),
            y: physSorted.map(d => d.score),
            text: physSorted.map(d => d.grade + ' (' + d.shape + ')'),
            type: 'bar',
            marker: {{ color: physSorted.map(d => d.score > 80 ? '#2ca02c' : (d.score > 60 ? '#ff7f0e' : '#d62728')) }}
        }};
        Plotly.newPlot('phys_bar', [tracePhysBar], {{
            title: 'Physical Reasoning Grades by Model',
            yaxis: {{ title: 'Score (A+=100, F=40)', range: [0, 105] }},
            margin: {{ b: 150 }}
        }});

        // 2. Scatter: Size vs Score
        const physScatterData = {{
            x: data.physical.map(d => d.size),
            y: data.physical.map(d => d.score),
            mode: 'markers+text',
            text: data.physical.map(d => d.model),
            textposition: 'top center',
            marker: {{ 
                size: 12,
                color: data.physical.map(d => d.arch === 'MoE' ? '#1f77b4' : '#ff7f0e'),
                symbol: data.physical.map(d => d.purpose === 'Reasoning' ? 'star' : 'circle')
            }},
            name: 'Models'
        }};
        
        Plotly.newPlot('phys_scatter', [physScatterData], {{
            title: 'Physical Reasoning: Parameter Size vs Score',
            xaxis: {{ title: 'Parameter Size (Billions)', type: 'log' }},
            yaxis: {{ title: 'Score', range: [0, 105] }},
            hovermode: 'closest'
        }});

        // --- Integral Test Charts ---

        // 3. Line Chart: Temp Sweep (Gemma)
        const tracesIntSweep = data.integral_sweep.map(m => ({{
            x: m.data.map(p => p.x),
            y: m.data.map(p => p.y),
            mode: 'lines+markers',
            name: m.model
        }}));
        
        Plotly.newPlot('int_sweep', tracesIntSweep, {{
            title: 'Gemma Models: Accuracy vs Temperature',
            xaxis: {{ title: 'Temperature' }},
            yaxis: {{ title: 'Accuracy (%)', range: [-5, 105] }}
        }});

        // 4. Scatter: Size vs Success (Combined)
        const intScatterX = [];
        const intScatterY = [];
        const intScatterText = [];
        const intScatterColor = [];

        // From Sweep (Gemma)
        data.integral_sweep.forEach(m => {{
            intScatterX.push(m.size);
            intScatterY.push(m.max_acc);
            intScatterText.push(m.model);
            intScatterColor.push('#1f77b4'); 
        }});

        // From MD (Pass/Fail)
        data.integral_models.forEach(m => {{
            if(m.size > 0) {{
                intScatterX.push(m.size);
                intScatterY.push(m.score);
                intScatterText.push(m.model);
                intScatterColor.push('#ff7f0e'); 
            }}
        }});

        const traceIntScatter = {{
            x: intScatterX,
            y: intScatterY,
            mode: 'markers+text',
            text: intScatterText,
            textposition: 'top center',
            marker: {{ size: 10, color: intScatterColor }}
        }};

        Plotly.newPlot('int_scatter', [traceIntScatter], {{
            title: 'Integral Test: Parameter Size vs Performance',
            xaxis: {{ title: 'Parameter Size (B)', type: 'log' }},
            yaxis: {{ title: 'Score / Max Accuracy (%)', range: [-5, 115] }}
        }});

    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated HTML at {OUTPUT_HTML_PATH}")

if __name__ == "__main__":
    p_data = parse_physical_reasoning(PHYSICAL_REASONING_PATH)
    i_json = parse_integral_json(INTEGRAL_JSON_PATH)
    i_md = parse_integral_md(INTEGRAL_MD_PATH)
    
    generate_html(p_data, i_json, i_md)