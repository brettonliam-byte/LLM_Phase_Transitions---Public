const XLSX = require('xlsx');
const path = require('path');

const filename = 'OL3file.xlsx';
const targetNormalized = "ithinkthereforeiam";

function normalize(str) {
    if (!str) return "";
    return String(str).toLowerCase().replace(/[^a-z]/g, "");
}

const workbook = XLSX.readFile(path.join(__dirname, filename));
const sheetName = "G12B";
const worksheet = workbook.Sheets[sheetName];
const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

console.log(`Searching ${filename} sheet '${sheetName}' for target...`);

let found = 0;
for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    if (!row) continue;
    for (let c = 0; c < row.length; c++) {
        const val = row[c];
        if (!val) continue;
        const valNorm = normalize(val);
        if (valNorm.includes(targetNormalized)) {
            console.log(`MATCH FOUND at Row ${r}, Col ${c}:`);
            console.log(`Raw Content: "${val}"`);
            found++;
        }
    }
}

if (found === 0) {
    console.log("No matches found.");
} else {
    console.log(`Total matches: ${found}`);
}
