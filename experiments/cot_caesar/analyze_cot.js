const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'COTGemma');
const outputJson = 'cot_data.json';
const targetNormalized = "ithinkthereforeiam";

function normalize(str) {
    if (!str) return "";
    return String(str).toLowerCase().replace(/[^a-z]/g, "");
}

// Map filenames to model names
const fileMap = {
    'OLTable1.txt': 'G1B',
    'OLTable4.txt': 'G4B',
    'OLTable12.txt': 'G12B',
    'OLTable27.txt': 'G27B'
};

const results = {};

// We assume 1050 responses total.
// 21 temps (0 to 2.0), 50 reps each.
const totalReps = 1050;
const repsPerTemp = 50;

fs.readdirSync(dir).forEach(file => {
    if (!fileMap[file]) return;
    const model = fileMap[file];
    const content = fs.readFileSync(path.join(dir, file), 'utf8');
    const totalLen = content.length;
    
    // Find all matches
    const regex = /I\s*think\s*therefore\s*I\s*am/gi;
    let match;
    
    // Initialize stats
    // Temps: 0, 0.1 ... 2.0 (21 steps)
    const tempStats = {};
    for(let i=0; i<=20; i++) {
        const t = (i/10).toFixed(1);
        tempStats[t] = { correct: 0, total: 50 };
    }

    while ((match = regex.exec(content)) !== null) {
        const pos = match.index;
        // Estimate response index
        const estimatedIndex = (pos / totalLen) * totalReps;
        
        // Map to temp
        // Index 0-49 -> Temp 0
        // Index 50-99 -> Temp 0.1
        const tempIndex = Math.floor(estimatedIndex / repsPerTemp);
        
        // Clamp index to 0-20
        const clampedIndex = Math.min(Math.max(tempIndex, 0), 20);
        const t = (clampedIndex / 10).toFixed(1);
        
        if (tempStats[t]) {
            tempStats[t].correct++;
        }
    }
    
    // Convert to array format for graph
    const dataPoints = [];
    for(let i=0; i<=20; i++) {
        const t = (i/10).toFixed(1);
        dataPoints.push({
            temp: t,
            correct: tempStats[t].correct,
            total: tempStats[t].total
        });
    }
    
    results[model] = dataPoints;
});

// Wrap in file structure for consistency
const finalData = { "COTGemma": results };

fs.writeFileSync(outputJson, JSON.stringify(finalData, null, 2));
console.log("COT Analysis complete.");
