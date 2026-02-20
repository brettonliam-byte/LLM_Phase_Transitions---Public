import csv
import re
import json
import os

# Input and Output paths
INPUT_FILE = r"C:\Users\Liam\Documents\Github\LLM_Phase_Transitions\experiments\Gemini3Analysis of Physical Reasoning 3.txt"
OUTPUT_FILE = r"C:\Users\Liam\Documents\Github\LLM_Phase_Transitions\results_viz\cable_shape_performance.html"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

data = []

# Regex to find parameter size (e.g., "32B", "671B", "1T")
size_pattern = re.compile(r"(\d+(?:\.\d+)?)(B|T)")

def parse_size(text):
    match = size_pattern.search(text)
    if match:
        val = float(match.group(1))
        unit = match.group(2)
        if unit == 'T':
            val *= 1000
        return val
    return None

def categorize_shape(shape):
    shape = shape.lower().strip()
    if "straight line" in shape:
        if "vertical" in shape: return "Standard Error" 
        return "Correct"
    
    if any(x in shape for x in ["curved", "asym", "mod", "dynamic", "complex", "concave", "hockey"]):
        return "Close/Plausible"
    
    if any(x in shape for x in ["catenary", "parabola", "vertical"]):
        return "Standard Error"
    
    if any(x in shape for x in ["tractrix", "sine", "wave"]):
        return "Hallucination"
    
    return "Standard Error"

# Read the file
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
    for line in lines:
        if not line.strip() or line.startswith("Model,Shape"):
            continue
            
        parts = list(csv.reader([line]))[0]
        if len(parts) < 3:
            continue
            
        model_name = parts[0].strip()
        shape_pred = parts[1].strip()
        desc = parts[2].strip()
        
        if "gemma3 (4b, 12b, 27b)" in model_name:
            sizes = [4, 12, 27]
            for s in sizes:
                data.append({
                    "model": f"gemma3-{s}b",
                    "shape": shape_pred,
                    "category": categorize_shape(shape_pred),
                    "size": s,
                    "desc": desc,
                    "arch": "Dense"
                })
            continue

        size = parse_size(desc)
        if not size:
            size = parse_size(model_name)
        
        arch = "Unknown"
        if "MoE" in desc: arch = "MoE"
        elif "Dense" in desc: arch = "Dense"
        elif "Hybrid" in desc: arch = "Hybrid"
        
        if size:
            data.append({
                "model": model_name,
                "shape": shape_pred,
                "category": categorize_shape(shape_pred),
                "size": size,
                "desc": desc,
                "arch": arch
            })

# HTML Construction (Part 1: Header & CSS)
html_part1 = """<!DOCTYPE html>
<html>
<head>
    <title>LLM Physical Reasoning: Cable Shape Task</title>
    <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background-color: #f4f4f9; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .chart-container { position: relative; height: 600px; width: 100%; }
        .description { margin-top: 20px; padding: 15px; background: #eef; border-left: 5px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cable Shape Prediction vs. Model Scale</h1>
        <div class="chart-container">
            <canvas id="performanceChart"></canvas>
        </div>
        <div class="description">
            <h3>Analysis Categories:</h3>
            <ul>
                <li><strong>Correct (Straight Line):</strong> The model correctly derived that the constant force vectors result in a straight line.</li>
                <li><strong>Close/Plausible:</strong> The model recognized both forces but failed the mathematical simplification.</li>
                <li><strong>Standard Error:</strong> The model defaulted to common textbook answers (Catenary, Parabola).</li>
                <li><strong>Hallucination:</strong> The model predicted mathematically unrelated shapes.</li>
            </ul>
        </div>
    </div>
"""

# HTML Construction (Part 2: Script)
html_part2 = """
    <script>
        const rawData = """ + json.dumps(data) + """;

        const yCategories = ["Hallucination", "Standard Error", "Close/Plausible", "Correct"];
        const yMap = {
            "Hallucination": 0,
            "Standard Error": 1,
            "Close/Plausible": 2,
            "Correct": 3
        };

        const datasets = [];
        const architectures = ["Dense", "MoE", "Hybrid", "Unknown"];
        const colors = {
            "Dense": "#36a2eb",
            "MoE": "#ff6384",
            "Hybrid": "#4bc0c0",
            "Unknown": "#9966ff"
        };

        architectures.forEach(arch => {
            const archData = rawData.filter(d => d.arch === arch).map(d => ({
                x: d.size,
                y: yMap[d.category],
                r: 8,
                model: d.model,
                desc: d.desc,
                shape: d.shape
            }));

            if (archData.length > 0) {
                datasets.push({
                    label: arch,
                    data: archData,
                    backgroundColor: colors[arch],
                    borderColor: colors[arch],
                    borderWidth: 1
                });
            }
        });

        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {
            type: 'bubble',
            data: { datasets: datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'logarithmic',
                        title: { display: true, text: 'Parameter Count (Billions) - Log Scale' },
                        min: 0.5,
                        max: 1500
                    },
                    y: {
                        type: 'linear',
                        title: { display: true, text: 'Reasoning Quality' },
                        min: -0.5,
                        max: 3.5,
                        ticks: {
                            callback: function(value, index, values) {
                                return yCategories[value];
                            },
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const point = context.raw;
                                return `${point.model} (${point.x}B): ${point.shape}`;
                            },
                            afterLabel: function(context) {
                                const point = context.raw;
                                const words = point.desc.split(' ');
                                let lines = [];
                                let line = '';
                                words.forEach(word => {
                                    if ((line + word).length > 60) {
                                        lines.push(line);
                                        line = word + ' ';
                                    } else {
                                        line += word + ' ';
                                    }
                                });
                                lines.push(line);
                                return lines;
                            }
                        }
                    },
                    legend: { position: 'top' },
                    title: { display: true, text: 'Physical Reasoning: Cable Shape Task' }
                }
            }
        });
    </script>
</body>
</html>
"""

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_part1 + html_part2)

print(f"Successfully generated visualization at: {OUTPUT_FILE}")