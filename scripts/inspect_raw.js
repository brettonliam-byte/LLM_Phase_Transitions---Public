const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const filename = 'OL3file.xlsx';
const filePath = path.join(__dirname, filename);

if (!fs.existsSync(filePath)) {
    console.log("File not found");
    process.exit(1);
}

const workbook = XLSX.readFile(filePath);
const sheetName = "G12B"; // Inspect G12B as it's a mid-sized model
const worksheet = workbook.Sheets[sheetName];
const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

console.log(`--- Samples from ${filename} / ${sheetName} ---`);

// Print the first 5 non-empty cells from the first column (Temp 0)
let count = 0;
for (let r = 0; r < rows.length; r++) {
    const val = rows[r][0]; // Column 0
    if (val) {
        console.log(`[Row ${r}]: ${JSON.stringify(val)}`);
        count++;
    }
    if (count >= 5) break;
}
