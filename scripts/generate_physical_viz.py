import json
import re
import os
import csv
import io

# Paths
PHYSICAL_REASONING_PATH = r"LLM_Phase_Transitions/experiments/Physical test/Analysis of Physical Reasoning.txt"
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

def generate_html(phys_data):
    print("Generating HTML...")
    payload = {
        "physical": phys_data
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

    </script>
</body>
</html>
    """
    
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated HTML at {OUTPUT_HTML_PATH}")

if __name__ == "__main__":
    p_data = parse_physical_reasoning(PHYSICAL_REASONING_PATH)
    generate_html(p_data)