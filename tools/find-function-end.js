/* eslint-disable no-console */
// Usage: node tools/find-function-end.js fps-game.html initGame

const fs = require('fs');

function lineOfIndex(text, idx) {
  let line = 1;
  for (let i = 0; i < idx; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
}

function findFunctionStart(text, name) {
  const re = new RegExp(`function\\s+${name}\\s*\\(\\s*\\)\\s*\\{`);
  const m = re.exec(text);
  if (!m) return null;
  return { index: m.index, braceIndex: m.index + m[0].length - 1 };
}

function findMatchingBrace(text, openBraceIndex) {
  let i = openBraceIndex;
  let depth = 0;
  let inS = false, inD = false, inT = false;
  let inLineComment = false, inBlockComment = false;

  for (; i < text.length; i++) {
    const c = text[i];
    const n = text[i + 1];

    if (inLineComment) {
      if (c === '\n') inLineComment = false;
      continue;
    }
    if (inBlockComment) {
      if (c === '*' && n === '/') {
        inBlockComment = false;
        i++;
      }
      continue;
    }

    if (!inS && !inD && !inT) {
      if (c === '/' && n === '/') { inLineComment = true; i++; continue; }
      if (c === '/' && n === '*') { inBlockComment = true; i++; continue; }
    }

    if (inS) {
      if (c === '\\') { i++; continue; }
      if (c === "'") inS = false;
      continue;
    }
    if (inD) {
      if (c === '\\') { i++; continue; }
      if (c === '"') inD = false;
      continue;
    }
    if (inT) {
      if (c === '\\') { i++; continue; }
      if (c === '`') { inT = false; continue; }
      // NOTE: we do NOT fully parse ${} in templates; braces inside ${} will still be counted,
      // which is fine for locating structural mismatches in this codebase.
      continue;
    }

    if (c === "'") { inS = true; continue; }
    if (c === '"') { inD = true; continue; }
    if (c === '`') { inT = true; continue; }

    if (c === '{') {
      depth++;
    } else if (c === '}') {
      depth--;
      if (depth === 0) return i;
      if (depth < 0) return i; // went negative
    }
  }

  return null;
}

function main() {
  const file = process.argv[2];
  const name = process.argv[3] || 'initGame';
  if (!file) {
    console.error('Usage: node tools/find-function-end.js <html-file> <functionName>');
    process.exit(2);
  }
  const text = fs.readFileSync(file, 'utf8');
  const start = findFunctionStart(text, name);
  if (!start) {
    console.error(`Function ${name} not found`);
    process.exit(1);
  }
  const startLine = lineOfIndex(text, start.index);
  const braceLine = lineOfIndex(text, start.braceIndex);
  console.log(`Found function ${name} at line ${startLine} (opening { at line ${braceLine})`);

  const endIdx = findMatchingBrace(text, start.braceIndex);
  if (endIdx == null) {
    console.error('No matching closing brace found');
    process.exit(1);
  }
  const endLine = lineOfIndex(text, endIdx);
  console.log(`Matching } at line ${endLine}`);
}

main();
