const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const files = ['OL3file.xlsx', 'OL4file.xlsx'];
// Target: "I think therefore I am"
// Normalized: "ithinkthereforeiam"
const target = "ithinkthereforeiam";

function normalize(str) {
    if (!str) return "";
    // If it's not a string, try to convert (e.g. number/boolean), though unlikely for this task
    const s = String(str);
    return s.toLowerCase().replace(/[^a-z]/g, "");
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
        // 'header: 1' returns an array of arrays
        const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        if (rows.length === 0) return;

        // The notebook logic was: Table[Table[..., {reps}], {temps}]
        // Inner table is rows (reps), Outer table is temps.
        // Result is {{t1r1, t1r2...}, {t2r1, t2r2...}}
        // Then Transpose was called?
        // Let's check the notebook code in Gemma3_Temp_Caesar.md:
        // G1B = Table[Table[... reps=25], {i, temps}]; 
        // G1BT = Transpose[G1B];
        // Export[..., "G1B" -> G1BT]
        
        // If G1B is { {T0_R1, T0_R2...}, {T0.2_R1...} } (Shape: N_Temps x N_Reps)
        // Then Transpose(G1B) is { {T0_R1, T0.2_R1...}, {T0_R2, T0.2_R2...} } (Shape: N_Reps x N_Temps)
        // Wait.
        // If I have 11 temperatures and 25 reps.
        // G1B is list of 11 lists, each length 25.
        // Transpose makes it list of 25 lists, each length 11.
        // So in Excel:
        // Rows are Repetitions (1 to 25).
        // Columns are Temperatures (0 to 2).
        
        // So reading row by row gives us a slice across temperatures for a specific repetition #.
        // We want to aggregate by COLUMN to get stats for a specific temperature.
        
        // Find max width to determine number of columns (temperatures)
        let maxWidth = 0;
        rows.forEach(row => maxWidth = Math.max(maxWidth, row.length));

        const columnStats = [];
        for (let c = 0; c < maxWidth; c++) {
            let correct = 0;
            let total = 0;
            for (let r = 0; r < rows.length; r++) {
                // Check if cell exists
                if (rows[r] && rows[r][c] !== undefined) {
                    const val = rows[r][c];
                    total++;
                    if (normalize(val).includes(target)) {
                        correct++;
                    }
                }
            }
            columnStats.push({ colIndex: c, correct, total });
        }

        fileResults[sheetName] = columnStats;
    });

    results[filename] = fileResults;
});

console.log(JSON.stringify(results, null, 2));
