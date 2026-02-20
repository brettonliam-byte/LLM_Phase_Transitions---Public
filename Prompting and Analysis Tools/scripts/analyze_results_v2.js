const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const files = ['OL3file.xlsx', 'OL4file.xlsx'];
// Target: "I think therefore I am"
const targetClean = "i think therefore i am";
const targetNormalized = "ithinkthereforeiam";

function normalize(str) {
    if (!str) return "";
    return String(str).toLowerCase().replace(/[^a-z]/g, "");
}

function clean(str) {
    if (!str) return "";
    // Lowercase, remove non-alpha except spaces, normalize spaces
    return String(str).toLowerCase().replace(/[^a-z ]/g, "").replace(/\s+/g, " ").trim();
}

const results = {};

files.forEach(filename => {
    const filePath = path.join(__dirname, filename);
    if (!fs.existsSync(filePath)) {
        results[filename] = { error: "File not found" };
        return;
    }

    const workbook = XLSX.readFile(filePath);
    const fileResults = {};

    workbook.SheetNames.forEach(sheetName => {
        const worksheet = workbook.Sheets[sheetName];
        const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        if (rows.length < 2) return; // Need header + data

        // Row 0 is headers (Temperatures). Column 0 is Index.
        // Data starts at Row 1, Column 1.
        
        // Determine number of columns (temperatures) from Header row (Row 0)
        // Skip Col 0 ("Temperature")
        const headerRow = rows[0];
        const numTemps = headerRow.length - 1; 

        const columnStats = [];

        for (let t = 0; t < numTemps; t++) {
            const colIndex = t + 1; // Actual column index in sheet
            let correct = 0;
            let spacingIssue = 0;
            let incorrect = 0;
            let total = 0;

            for (let r = 1; r < rows.length; r++) { // Start row 1
                if (!rows[r]) continue;
                
                const val = rows[r][colIndex];
                total++;

                if (val === undefined || val === null) {
                    incorrect++;
                    continue;
                }

                const valNorm = normalize(val);
                const valClean = clean(val);

                if (valNorm.includes(targetNormalized)) {
                    // It contains the correct letters in order.
                    // Now check if it's "Clean" (correct spacing)
                    // We check if the 'clean' version contains the target with spaces.
                    if (valClean.includes(targetClean)) {
                        correct++;
                    } else {
                        // Correct letters, but spacing is off (or extra chars that were removed in clean but not norm)
                        spacingIssue++;
                    }
                } else {
                    incorrect++;
                }
            }
            
            // Get temp label from header
            const tempLabel = headerRow[colIndex];
            columnStats.push({ temp: tempLabel, correct, spacingIssue, incorrect, total });
        }

        fileResults[sheetName] = columnStats;
    });

    results[filename] = fileResults;
});

fs.writeFileSync('experiment_data.json', JSON.stringify(results, null, 2));
console.log("Data written to experiment_data.json");
