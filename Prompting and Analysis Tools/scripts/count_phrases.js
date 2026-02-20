const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'COTGemma');
const files = fs.readdirSync(dir);

files.forEach(file => {
    const content = fs.readFileSync(path.join(dir, file), 'utf8');
    const encodedPhrase = "N ymnsp ymjwjktwj N fr";
    const count = (content.match(new RegExp(encodedPhrase, "g")) || []).length;
    console.log(`${file}: ${count} occurrences of encoded phrase.`);
    
    // Also check for "I think therefore I am"
    const target = "I think therefore I am";
    // Case insensitive match
    const solveCount = (content.match(new RegExp(target, "gi")) || []).length;
    console.log(`${file}: ${solveCount} occurrences of target phrase.`);
});
