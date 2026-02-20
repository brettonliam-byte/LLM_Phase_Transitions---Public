const XLSX = require('xlsx');
const path = require('path');

const filename = 'OL3file.xlsx';
const workbook = XLSX.readFile(path.join(__dirname, filename));
const sheetName = "G12B";
const worksheet = workbook.Sheets[sheetName];
const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

console.log(`--- Grid View ${filename} / ${sheetName} ---`);
// Print top 10 rows, first 5 columns
for (let r = 0; r < Math.min(rows.length, 10); r++) {
    const row = rows[r];
    const slice = row.slice(0, 5).map(cell => {
        const s = String(cell);
        return s.length > 20 ? s.substring(0, 17) + "..." : s;
    });
    console.log(`Row ${r}: [${slice.join(", ")}]`);
}
