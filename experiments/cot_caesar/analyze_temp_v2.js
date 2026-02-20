const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const outputReport = path.join(__dirname, 'Temperature_Analysis.md');
const outputJson = path.join(__dirname, 'temp_data.json');

const files = {
    '1b': 'OLTable1.txt',
    '4b': 'OLTable4.txt',
    '12b': 'OLTable12.txt',
    '27b': 'OLTable27.txt'
};

const target = "ithinkthereforeiam";

function normalize(str) {
    if (!str) return "";
    return str.toLowerCase().replace(/[^a-z]/g, "");
}

function analyzeFile(filePath, modelName) {
    if (!fs.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        return null;
    }

    const content = fs.readFileSync(filePath, 'utf8');
    // Split by tab. Filter empty strings in case of trailing tabs.
    const segments = content.split('\t').filter(s => s.trim().length > 0);
    
    console.log(`Model ${modelName}: Found ${segments.length} transcripts.`);

    // Expected: 21 temperatures * 50 reps = 1050.
    // Or 20 * 50 = 1000.
    // We will assume the structure is blocks of 50.
    
    const results = {}; // temp -> { correct, total }

    segments.forEach((segment, index) => {
        // Determine temperature
        // 0-49 -> 0.0, 50-99 -> 0.1, etc.
        const tempIndex = Math.floor(index / 50);
        const temp = (tempIndex * 0.1).toFixed(1);

        if (!results[temp]) {
            results[temp] = { correct: 0, total: 0 };
        }

        const normalized = normalize(segment);
        const isCorrect = normalized.includes(target);

        results[temp].total++;
        if (isCorrect) {
            results[temp].correct++;
        }
    });

    return results;
}

const allResults = {};

for (const [model, fileName] of Object.entries(files)) {
    const filePath = path.join(dataDir, fileName);
    allResults[model] = analyzeFile(filePath, model);
}

// Generate Markdown Report
let mdContent = "# Caesar Cipher CoT Analysis by Temperature\n\n";
mdContent += "Target Phrase: \"I think therefore I am\"\n\n";

for (const model of ['1b', '4b', '12b', '27b']) {
    const data = allResults[model];
    if (!data) continue;

    mdContent += `## Model: Gemma 3 ${model.toUpperCase()}\n\n`;
    mdContent += "| Temperature | Solve Rate (%) | Correct / Total |\n";
    mdContent += "|---|---|---|\n";

    const temps = Object.keys(data).sort((a, b) => parseFloat(a) - parseFloat(b));
    
    temps.forEach(temp => {
        const { correct, total } = data[temp];
        const rate = ((correct / total) * 100).toFixed(1);
        mdContent += `| ${temp} | ${rate}% | ${correct}/${total} |\n`;
    });
    mdContent += "\n";
}

fs.writeFileSync(outputReport, mdContent);
fs.writeFileSync(outputJson, JSON.stringify(allResults, null, 2));

console.log("Analysis complete. Report written to Temperature_Analysis.md");
