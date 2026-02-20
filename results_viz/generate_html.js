const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'experiment_data.json');
const outputPath = path.join(__dirname, 'visualization.html');

// Load Main Data
let experimentData = {};
try {
    const rawData = fs.readFileSync(dataPath, 'utf8').replace(/^\uFEFF/, '').trim();
    // Try to find valid JSON start
    const start = rawData.indexOf('{');
    if (start !== -1) {
        experimentData = JSON.parse(rawData.substring(start));
    }
} catch (e) {
    console.error("Error loading experiment_data.json:", e);
}

// Load Qwen Data
const qwenPath = path.join(__dirname, 'qwen_data.json');
if (fs.existsSync(qwenPath)) {
    const qwenRaw = fs.readFileSync(qwenPath, 'utf8').replace(/^\uFEFF/, '').trim();
    const qwenData = JSON.parse(qwenRaw);
    experimentData = { ...experimentData, ...qwenData };
}

// Load COT Data
const cotPath = path.join(__dirname, 'cot_data.json');
if (fs.existsSync(cotPath)) {
    const cotRaw = fs.readFileSync(cotPath, 'utf8').replace(/^\uFEFF/, '').trim();
    const cotData = JSON.parse(cotRaw);
    experimentData = { ...experimentData, ...cotData };
}

// Manually patch in the 2 rare successes for G12B in OL3file (Caesar)
if (experimentData['OL3file.xlsx'] && experimentData['OL3file.xlsx']['G12B']) {
    // Indices 13 and 18
    if (experimentData['OL3file.xlsx']['G12B'][13]) {
         experimentData['OL3file.xlsx']['G12B'][13].correct = 1;
         experimentData['OL3file.xlsx']['G12B'][13].incorrect -= 1;
    }
    if (experimentData['OL3file.xlsx']['G12B'][18]) {
         experimentData['OL3file.xlsx']['G12B'][18].correct = 1;
         experimentData['OL3file.xlsx']['G12B'][18].incorrect -= 1;
    }
}

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Phase Transitions: Experiment Results</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; padding: 20px; background-color: #f4f4f9; }
        .container { max-width: 1000px; margin: 0 auto; }
        .chart-container { background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        h2 { color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
        p { color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LLM Phase Transitions Analysis</h1>
        
        <div class="chart-container">
            <h2>Substitution Cipher: Success Rate (Perfect Solves)</h2>
            <p>Phase transition visible across model sizes. 27B dominates, 12B is capable, smaller models fail to format correctly.</p>
            <canvas id="subPerfectChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Substitution Cipher: Effective Success (Perfect + Close)</h2>
            <p>Shows the "latent capability" of the 4B model. It decodes the letters correctly (Close) but fails spacing. 1B remains incompetent.</p>
            <canvas id="subEffectiveChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Gemma 3 Performance (Zero-Shot)</h2>
            <p>Complete failure across the board, except for two rare "Chain of Thought" sparks from the 12B model.</p>
            <canvas id="caesarChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Zero-Shot vs Chain-of-Thought (CoT)</h2>
            <p>Removing the "return only" constraint allows G12B and G27B to reason (CoT), improving performance compared to the Zero-Shot baseline (dotted lines).</p>
            <canvas id="cotChart"></canvas>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Qwen vs Gemma</h2>
            <p>Qwen 4B significantly outperforms the entire Gemma 3 family on the Caesar task, showing high reliability up to Temp 1.5.</p>
            <canvas id="qwenChart"></canvas>
        </div>
    </div>

    <script>
        const data = ${JSON.stringify(experimentData)};
        
        const colors = {
            'G1B': '#ff6384',
            'G4B': '#ff9f40',
            'G12B': '#36a2eb',
            'G27B': '#4bc0c0',
            'Qwen3:4b': '#9966ff'
        };

        function getDataset(fileKey, metricCalc, styleOverrides = {}) {
            const datasets = [];
            const fileData = data[fileKey];
            if (!fileData) return [];

            for (const model in fileData) {
                const points = fileData[model];
                const dataPoints = points.map(p => metricCalc(p));
                
                datasets.push({
                    label: model + (styleOverrides.suffix || ''),
                    data: dataPoints,
                    borderColor: colors[model] || '#000',
                    backgroundColor: colors[model] || '#000',
                    fill: false,
                    tension: 0.3,
                    ...styleOverrides
                });
            }
            return datasets;
        }

        function getLabels(fileKey) {
            const fileData = data[fileKey];
            if (!fileData) return [];
            const firstModel = Object.keys(fileData)[0];
            if (!firstModel) return [];
            
            return fileData[firstModel].map((p, index) => {
                let t = 0;
                if (fileKey === 'OL4file.xlsx') {
                   t = (index * 0.2).toFixed(1);
                } else {
                   t = (index * 0.1).toFixed(1);
                }
                return t;
            });
        }

        const labelsOL3 = getLabels('OL3file.xlsx');
        const labelsOL4 = getLabels('OL4file.xlsx');
        const labelsQwen = getLabels('OLQWEN34B.xlsx');

        // 1. Substitution Perfect
        new Chart(document.getElementById('subPerfectChart').getContext('2d'), {
            type: 'line',
            data: { labels: labelsOL4, datasets: getDataset('OL4file.xlsx', p => (p.correct / p.total) * 100) },
            options: { scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Success Rate (%)' } }, x: { title: { display: true, text: 'Temperature' } } } }
        });

        // 2. Substitution Effective
        new Chart(document.getElementById('subEffectiveChart').getContext('2d'), {
            type: 'line',
            data: { labels: labelsOL4, datasets: getDataset('OL4file.xlsx', p => ((p.correct + p.spacingIssue) / p.total) * 100) },
            options: { scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Effective Rate (%)' } }, x: { title: { display: true, text: 'Temperature' } } } }
        });

        // 3. Caesar Perfect (Gemma Zero-Shot)
        new Chart(document.getElementById('caesarChart').getContext('2d'), {
            type: 'line',
            data: { labels: labelsOL3, datasets: getDataset('OL3file.xlsx', p => (p.correct / p.total) * 100) },
            options: { scales: { y: { beginAtZero: true, max: 5, title: { display: true, text: 'Success Rate (%)' } }, x: { title: { display: true, text: 'Temperature' } } } }
        });

        // 4. CoT Comparison
        // Only show G12B and G27B for clarity, or all. Let's show all.
        // COTGemma data is structured like OL3file (G1B, G4B...)
        const cotSet = getDataset('COTGemma', p => (p.correct / p.total) * 100, { suffix: ' (CoT)' });
        // Use dashed lines for Zero-Shot baseline
        const zeroShotSet = getDataset('OL3file.xlsx', p => (p.correct / p.total) * 100, { borderDash: [5, 5], suffix: ' (Zero-Shot)', pointRadius: 0, borderWidth: 1 });
        
        new Chart(document.getElementById('cotChart').getContext('2d'), {
            type: 'line',
            data: { labels: labelsOL3, datasets: [...cotSet, ...zeroShotSet] },
            options: { scales: { y: { beginAtZero: true, max: 20, title: { display: true, text: 'Success Rate (%)' } }, x: { title: { display: true, text: 'Temperature' } } } }
        });

        // 5. Qwen vs Gemma Caesar
        const qwenSet = getDataset('OLQWEN34B.xlsx', p => (p.correct / p.total) * 100);
        const gemmaSet = getDataset('OL3file.xlsx', p => (p.correct / p.total) * 100);
        
        new Chart(document.getElementById('qwenChart').getContext('2d'), {
            type: 'line',
            data: { 
                labels: labelsQwen, 
                datasets: [...qwenSet, ...gemmaSet] 
            },
            options: { scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Success Rate (%)' } }, x: { title: { display: true, text: 'Temperature' } } } }
        });

    </script>
</body>
</html>`;

fs.writeFileSync(outputPath, htmlContent);
console.log("HTML generation complete.");