/* eslint-disable no-console */
// Quick syntax checker for inline JS inside an HTML file.
// Usage: node tools/check-html-js-syntax.js fps-game.html

const fs = require('fs');
const vm = require('vm');

function countLines(str) {
  // 1-based lines
  let lines = 1;
  for (let i = 0; i < str.length; i++) if (str.charCodeAt(i) === 10) lines++;
  return lines;
}

function escapeRegExp(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getLineColFromStack(stack, filenameHint) {
  const text = String(stack || '');

  // Prefer the entry that references our provided filename (vm.Script filename option).
  if (filenameHint) {
    const re = new RegExp(`${escapeRegExp(filenameHint)}:(\\d+):(\\d+)`);
    const m = text.match(re);
    if (m) return { line: Number(m[1]), col: Number(m[2]) };
    const reNoCol = new RegExp(`${escapeRegExp(filenameHint)}:(\\d+)`);
    const m2 = text.match(reNoCol);
    if (m2) return { line: Number(m2[1]), col: 1 };
  }

  // Fallback: first filename-like line/col occurrence.
  const m = text.match(/\b[^\s()]+:(\d+):(\d+)\b/);
  if (!m) return null;
  return { line: Number(m[1]), col: Number(m[2]) };
}

function extractScripts(html) {
  const scripts = [];
  const lower = html.toLowerCase();
  let i = 0;
  while (true) {
    const open = lower.indexOf('<script', i);
    if (open === -1) break;
    const openEnd = lower.indexOf('>', open);
    if (openEnd === -1) break;

    const close = lower.indexOf('</script>', openEnd + 1);
    if (close === -1) break;

    const tag = html.slice(open, openEnd + 1);
    const contentStart = openEnd + 1;
    const contentEnd = close;
    const content = html.slice(contentStart, contentEnd);

    scripts.push({ tag, content, contentStartIndex: contentStart });
    i = close + '</script>'.length;
  }
  return scripts;
}

function isLikelyJavaScript(tag) {
  // Ignore shader/json/template blocks.
  const t = tag.toLowerCase();
  const typeMatch = t.match(/type\s*=\s*['\"]([^'\"]+)['\"]/);
  if (!typeMatch) return true;
  const type = typeMatch[1];
  if (type.includes('importmap')) return false;
  if (type.includes('x-shader') || type.includes('shader')) return false;
  if (type.includes('application/json')) return false;
  if (type.includes('text/plain')) return false;
  // keep text/javascript, application/javascript, module
  return true;
}

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node tools/check-html-js-syntax.js <html-file>');
    process.exit(2);
  }
  const html = fs.readFileSync(file, 'utf8');
  const scripts = extractScripts(html);

  let errorCount = 0;
  let checked = 0;

  for (let idx = 0; idx < scripts.length; idx++) {
    const { tag, content, contentStartIndex } = scripts[idx];
    if (!isLikelyJavaScript(tag)) continue;

    const startLine = countLines(html.slice(0, contentStartIndex));
    const code = content;
    if (!code.trim()) continue;

    checked++;
    try {
      // Compile only (no execution)
      const scriptFilename = `${file}#script${idx + 1}`;
      new vm.Script(code, { filename: scriptFilename });
    } catch (err) {
      errorCount++;
      const scriptFilename = `${file}#script${idx + 1}`;
      const lc = getLineColFromStack(err.stack, scriptFilename) || { line: 1, col: 1 };
      const globalLine = startLine + lc.line - 1;
      console.log('---');
      console.log(`SyntaxError in script block #${idx + 1}`);
      console.log(`Message: ${err && err.message ? err.message : String(err)}`);
      console.log(`Location: ${file}:${globalLine}:${lc.col}`);

      // Print a small excerpt
      const lines = code.split(/\r?\n/);
      const from = Math.max(0, lc.line - 3);
      const to = Math.min(lines.length, lc.line + 2);
      for (let l = from; l < to; l++) {
        const mark = (l + 1 === lc.line) ? '>' : ' ';
        console.log(`${mark} ${String(l + 1).padStart(4)} | ${lines[l]}`);
      }
    }
  }

  console.log('===');
  console.log(`Checked JS-like <script> blocks: ${checked}`);
  console.log(`Syntax errors found: ${errorCount}`);
  process.exit(errorCount ? 1 : 0);
}

main();
