const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const filename = 'OLQWEN34B.xlsx';
const targetClean = "i think therefore i am";
const targetNormalized = "ithinkthereforeiam";
const originKeywords = ["descartes", "cogito", "rene", "rené", "latin", "philosopher"];

function normalize(str) {
    if (!str) return "";
    return String(str).toLowerCase().replace(/[^a-z]/g, "");
}

function clean(str) {
    if (!str) return "";
    return String(str).toLowerCase().replace(/[^a-z ]/g, "").replace(/\s+/g, " ").trim();
}

function checkOrigin(str) {
    if (!str) return false;
    const lower = String(str).toLowerCase();
    return originKeywords.some(keyword => lower.includes(keyword));
}

const filePath = path.join(__dirname, filename);
if (!fs.existsSync(filePath)) {
    console.log("File not found");
    process.exit(1);
}

const workbook = XLSX.readFile(filePath);
const sheetName = workbook.SheetNames[0]; // Assuming first sheet
const worksheet = workbook.Sheets[sheetName];
const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

// Assuming structure: Header row (Temp 0, 0.1...) -> Data Rows
// Or is it like OL4file where row 0 is data?
// Let's assume standard header row 0 with temps.

// Check row 0. If it contains "Temperature" or numbers, it's a header.
// If it contains long text, it's data.
// Based on 17.11.25.nb export: Export["OLQWEN34B.xlsx", "Q34B" -> Q34BT, "XLSX"]
// Q34BT is Transpose[Q34B].
// Q34B = Table[Table[...], {temps}] -> Shape: Temps x Reps.
// Transpose -> Shape: Reps x Temps.
// So Columns are Temperatures. Rows are Repetitions.
// This matches the other files.

// Determine if row 0 is header.
const firstCell = rows[0][0];
let startRow = 1;
let temps = [];

// Heuristic: If first cell is a number or "Temperature", it's a header.
// If it's a long string, it's data (and we have no header row in the file).
// 17.11.25.nb used temps = Range[0, 2, 0.1]; (21 temps).
// So we expect ~21 columns.

if (typeof firstCell === 'string' && firstCell.length > 20) {
    // Likely data. No header.
    startRow = 0;
    // Generate labels 0, 0.1, ...
    for(let i=0; i<=20; i++) temps.push((i/10).toFixed(1));
} else {
    // Likely header.
    startRow = 1;
    // Extract temps from header (skipping index col if present?)
    // Let's assume standard behavior: Col 0 is index/label, Cols 1..N are temps?
    // Or just Cols 0..N are temps?
    // Let's default to generating labels 0..2.0 (0.1 step) as per notebook
    for(let i=0; i<=20; i++) temps.push((i/10).toFixed(1));
}

const columnStats = [];

// Iterate columns (Temperatures)
// Note: We need to determine if there is an index column.
// In 17.11.25.nb: Q34BT is just the data. No explicit headers added in Export unless "Q34B" -> Q34BT adds "Q34B" as a sheet name?
// The notebook code: Export["OLQWEN34B.xlsx", "Q34B" -> Q34BT, "XLSX"]
// This puts Q34BT into a sheet named "Q34B".
// Usually Export[... list of lists ...] creates a pure grid.
// So Col 0 = Temp 0. Col 1 = Temp 0.1.
// Let's check max width.
let maxWidth = 0;
rows.forEach(r => { if(r) maxWidth = Math.max(maxWidth, r.length); });

// If maxWidth is approx 21, then Col 0 is Temp 0.
// If maxWidth is approx 22, then Col 0 might be index.
const hasIndexCol = (maxWidth > 21);
const colOffset = hasIndexCol ? 1 : 0;

for (let t = 0; t < temps.length; t++) {
    const colIndex = t + colOffset;
    let correct = 0;
    let spacingIssue = 0;
    let originRecognized = 0;
    let total = 0;

    for (let r = startRow; r < rows.length; r++) {
        if (!rows[r]) continue;
        const val = rows[r][colIndex];
        
        // Skip empty cells if rep count varies
        if (val === undefined || val === null) continue;
        
        total++;
        const valNorm = normalize(val);
        const valClean = clean(val);

        let isCorrect = false;

        if (valNorm.includes(targetNormalized)) {
            if (valClean.includes(targetClean)) {
                correct++;
                isCorrect = true;
            } else {
                spacingIssue++;
                isCorrect = true; // Still counts as a "solve" of the cipher, just bad formatting
            }
        }

        // Check origin recognition regardless of correctness (though usually correlated)
        if (checkOrigin(val)) {
            originRecognized++;
        }
    }

    columnStats.push({ 
        temp: temps[t], 
        correct, 
        spacingIssue, 
        originRecognized,
        total 
    });
}

const result = { "OLQWEN34B.xlsx": { "Qwen3:4b": columnStats } };
fs.writeFileSync('qwen_data.json', JSON.stringify(result, null, 2));
console.log("Analysis complete.");
