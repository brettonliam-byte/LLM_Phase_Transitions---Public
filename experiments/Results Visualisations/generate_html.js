const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'experiment_data.json');
const outputPath = path.join(__dirname, 'visualization.html');

// Load Main Data
let experimentData = {};
try {
    const rawData = fs.readFileSync(dataPath, 'utf8').replace(/^\uFEFF/, '').trim();
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
        p { color: #444; line-height: 1.6; }
        .text-section { background: #fff; padding: 20px; margin-bottom: 30px; border-radius: 8px; border-left: 5px solid #0d6efd; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Deciphering Experiment</h1>
        
        <div class="text-section">
            <h3>Preamble</h3>
            <p>The gemma3 family of dense LLMs were posed a task to decipher a phrase encoded via a substitution cipher. The phrase 'I think therefore I am' becomes: '9 20 8 9 14 11 20 8 5 18 5 6 15 18 5 9 1 13'. The models were then tasked with deciphering the same message encoded via a Caesar cipher with a rotation of 5: 'I think therefore I am' becomes: 'N ymnsp ymjwjktwj N fr'. </p>
        </div>

        <div class="chart-container">
            <h2>Substitution Cipher: Success Rate (Perfect Solves)</h2>
            <p>A correct answer was at first deemed to be one which matched the format of the original phrase, i.e. the spaces between words had to be in the correct places (though capitalisations were ignored). </p>
            <canvas id="subPerfectChart"></canvas>
        </div>

        <div class="text-section">
            <h3>Scaling Laws in Substitution</h3>
            <p>The perfect solve metric shows a performance threshold. Below 12B parameters, models almost never produce a perfectly formatted and decoded string. However, the jump from 12B to 27B represents a large leap in reliability while both smaller models fail to format correctly. The solve rate of the 12 billion parameter model fluctuated around a 40-50% success rate with increasing temperature while the 27 billion parameter version had a decline in solve rate with increasing temperature.</p>
        </div>

        <div class="chart-container">
            <h2>Substitution Cipher: Effective Success (Perfect + Close Solves)</h2>
            <p>The marking criteria for a correct solve was relaxed to include all responses in which all the numbers had been correctly substituted to their original letters, disregarding omitted and/or omitted spaces.</p>
            <canvas id="subEffectiveChart"></canvas>
        </div>

        <div class="text-section">
            <h3>Substitution Cipher: Latent Capabilities of Smaller Models</h3>
            <p>By relaxing the marking criteria, we see that the smaller models can correctly perform the decoding of the letters, but fail to correctly apply letter spacings. The two larger models achieve a near 100% success rate under this criteria, showing that the temperature effect on their responses was to alter the abilities of the models to insert spaces and not their ability to decipher the message. The 4 billion parameter model exhibits a decline in solve rate with increasing temperature akin to the 27 billion parameter counterpart under the stricter marking criteria.</p>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Gemma3 Performance (Zero-Shot)</h2>
            <p>The added layer of complexity to the cipher proved too difficult for any of the models to solve correctly, save for only two instances by the 12 billion parameter model.</p>
            <canvas id="caesarChart"></canvas>
        </div>

        <div class="text-section">
            <h3>Caesar Cipher Difficulty and Prompt Engineering</h3>
            <p>As part of the prompting process, the phrase: 'return the decoded message only' was appended to the initial prompt for every iteration to reduce the likelihood of data handling errors during the exporting process. During the prompting process, such phrases can limit models' ability to form a chain-of-thought (CoT) for problem solving, effectively 'thinking out loud'. To investigate the effects of this added phrase, the experiment was carried out a second time without the constraint.</p>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Zero-Shot vs Chain-of-Thought (CoT)</h2>
            <p>Removing the prompt constraint allows G12B and G27B to reason (CoT), improving their performance compared to the previous experiment that employed the constraint.</p>
            <canvas id="cotChart"></canvas>
        </div>

        <div class="text-section">
            <h3>Analysis: The Impact of Reasoned Thought</h3>
            <p>Allowing the two larger models to apply a CoT to the problem increases their performance, while the performance has improved for both models, the solve rate is far lower than for the substitution cipher as expected for a more difficult problem. Both larger models display an oscillation in solve rate with increasing temperature.</p>
        </div>

        <div class="chart-container">
            <h2>Caesar Cipher: Qwen vs Gemma</h2>
            <p>Qwen3 4B was tasked with solving the Caesar cipher using the same prompt constraint to return the solution only.</p>
            <canvas id="qwenChart"></canvas>
        </div>

        <div class="text-section">
            <h3>Model Type Suitablility to Differing Tasks</h3>
            <p>The qwen3 model despite its small size proved far more capable of solving the Caesar cipher correctly than the gemma3 models tested, the performance declines steeply from a near-perfect solve rate to a solve rate near zero as temperature increases from 0 to 1.</p>
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
        const cotSet = getDataset('COTGemma', p => (p.correct / p.total) * 100, { suffix: ' (CoT)' });
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
console.log("HTML restoration complete.");
