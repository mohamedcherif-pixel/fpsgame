#!/usr/bin/env node
/*
  Inspect GLB (glTF 2.0 binary) files and list animation clips.
  No external dependencies.

  Usage:
    node tools/inspect-glb-animations.js path/to/file.glb
    node tools/inspect-glb-animations.js path/to/folder
    node tools/inspect-glb-animations.js --all
*/

const fs = require('fs');
const path = require('path');

function isDirectory(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

function listGlbFiles(rootDir) {
  const out = [];
  const stack = [rootDir];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const ent of entries) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) stack.push(full);
      else if (ent.isFile() && ent.name.toLowerCase().endsWith('.glb')) out.push(full);
    }
  }
  out.sort((a, b) => a.localeCompare(b));
  return out;
}

function readUInt32LE(buf, offset) {
  return buf.readUInt32LE(offset);
}

function parseGlb(buffer) {
  // GLB header: magic(4) version(4) length(4)
  const magic = buffer.toString('ascii', 0, 4);
  if (magic !== 'glTF') throw new Error(`Not a GLB (magic=${JSON.stringify(magic)})`);

  const version = readUInt32LE(buffer, 4);
  if (version !== 2) throw new Error(`Unsupported GLB version: ${version}`);

  const totalLength = readUInt32LE(buffer, 8);
  if (totalLength !== buffer.length) {
    // Some exporters lie; tolerate if buffer is larger.
    if (totalLength > buffer.length) throw new Error(`Truncated GLB: header length=${totalLength}, file length=${buffer.length}`);
  }

  let offset = 12;
  let jsonChunk = null;
  let binChunk = Buffer.alloc(0);

  while (offset + 8 <= buffer.length) {
    const chunkLength = readUInt32LE(buffer, offset);
    const chunkType = buffer.toString('ascii', offset + 4, offset + 8);
    const chunkStart = offset + 8;
    const chunkEnd = chunkStart + chunkLength;
    if (chunkEnd > buffer.length) throw new Error('Invalid chunk length (out of bounds)');

    const chunkData = buffer.subarray(chunkStart, chunkEnd);
    if (chunkType === 'JSON') {
      jsonChunk = chunkData;
    } else if (chunkType === 'BIN\u0000') {
      binChunk = chunkData;
    }
    offset = chunkEnd;
  }

  if (!jsonChunk) throw new Error('Missing JSON chunk');
  const gltf = JSON.parse(jsonChunk.toString('utf8'));
  return { gltf, bin: binChunk };
}

function getBufferViewRange(gltf, bufferViewIndex) {
  const bv = gltf.bufferViews?.[bufferViewIndex];
  if (!bv) throw new Error(`Missing bufferView[${bufferViewIndex}]`);
  const byteOffset = bv.byteOffset ?? 0;
  const byteLength = bv.byteLength;
  const byteStride = bv.byteStride ?? null;
  const bufferIndex = bv.buffer ?? 0;
  return { byteOffset, byteLength, byteStride, bufferIndex };
}

function accessorComponentSize(componentType) {
  switch (componentType) {
    case 5126: // FLOAT
      return 4;
    case 5125: // UNSIGNED_INT
    case 5124: // INT
      return 4;
    case 5123: // UNSIGNED_SHORT
    case 5122: // SHORT
      return 2;
    case 5121: // UNSIGNED_BYTE
    case 5120: // BYTE
      return 1;
    default:
      throw new Error(`Unsupported componentType: ${componentType}`);
  }
}

function accessorTypeComponents(type) {
  switch (type) {
    case 'SCALAR':
      return 1;
    case 'VEC2':
      return 2;
    case 'VEC3':
      return 3;
    case 'VEC4':
      return 4;
    case 'MAT2':
      return 4;
    case 'MAT3':
      return 9;
    case 'MAT4':
      return 16;
    default:
      throw new Error(`Unsupported accessor type: ${type}`);
  }
}

function readAccessorFloats(gltf, bin, accessorIndex) {
  const acc = gltf.accessors?.[accessorIndex];
  if (!acc) throw new Error(`Missing accessor[${accessorIndex}]`);

  const { bufferView: bufferViewIndex, byteOffset: accByteOffset = 0, componentType, count, type } = acc;
  if (bufferViewIndex == null) throw new Error(`accessor[${accessorIndex}] has no bufferView`);

  const components = accessorTypeComponents(type);
  const componentSize = accessorComponentSize(componentType);
  const elementSize = components * componentSize;

  const { byteOffset: bvOffset, byteStride, bufferIndex } = getBufferViewRange(gltf, bufferViewIndex);
  if (bufferIndex !== 0) {
    // GLB generally has one buffer; if not, we still only have BIN.
    // We'll continue, but it may be incorrect for multi-buffer GLB.
  }

  if (componentType !== 5126) {
    throw new Error(`accessor[${accessorIndex}] is not FLOAT (componentType=${componentType})`);
  }

  const stride = byteStride ?? elementSize;
  const base = bvOffset + accByteOffset;

  const out = new Float32Array(count * components);
  for (let i = 0; i < count; i++) {
    const elemOffset = base + i * stride;
    for (let c = 0; c < components; c++) {
      out[i * components + c] = bin.readFloatLE(elemOffset + c * 4);
    }
  }
  return out;
}

function summarizeAnimations({ gltf, bin }) {
  const animations = gltf.animations ?? [];
  const nodes = gltf.nodes ?? [];

  const results = [];

  for (let animIndex = 0; animIndex < animations.length; animIndex++) {
    const anim = animations[animIndex];
    const name = anim.name || `animation_${animIndex}`;
    const channels = anim.channels ?? [];
    const samplers = anim.samplers ?? [];

    let minT = Number.POSITIVE_INFINITY;
    let maxT = 0;
    let floatInputsRead = 0;

    const targetNodes = new Set();
    const targetPaths = new Set();

    for (const ch of channels) {
      const samplerIndex = ch.sampler;
      const target = ch.target;
      if (target?.node != null) targetNodes.add(target.node);
      if (target?.path) targetPaths.add(target.path);

      const sampler = samplers[samplerIndex];
      if (!sampler) continue;
      const inputAcc = sampler.input;
      if (inputAcc == null) continue;

      try {
        const times = readAccessorFloats(gltf, bin, inputAcc);
        if (times.length) {
          floatInputsRead++;
          for (let i = 0; i < times.length; i++) {
            const t = times[i];
            if (t < minT) minT = t;
            if (t > maxT) maxT = t;
          }
        }
      } catch {
        // Ignore read failures; still report animation presence.
      }
    }

    // Node names for readability
    const nodeNames = [...targetNodes].map((idx) => nodes[idx]?.name || `node_${idx}`);

    results.push({
      index: animIndex,
      name,
      channelCount: channels.length,
      samplerCount: samplers.length,
      targetNodeCount: targetNodes.size,
      targetNodes: nodeNames,
      targetPaths: [...targetPaths],
      duration: floatInputsRead ? Math.max(0, maxT - (isFinite(minT) ? minT : 0)) : null,
      minTime: floatInputsRead && isFinite(minT) ? minT : null,
      maxTime: floatInputsRead ? maxT : null,
    });
  }

  return results;
}

function inspectFile(filePath) {
  const buf = fs.readFileSync(filePath);
  const parsed = parseGlb(buf);
  const animations = summarizeAnimations(parsed);

  return {
    filePath,
    animationCount: animations.length,
    animations,
  };
}

function formatSeconds(s) {
  if (s == null || !isFinite(s)) return 'n/a';
  return `${s.toFixed(3)}s`;
}

function main() {
  const args = process.argv.slice(2);
  const workspaceRoot = path.resolve(__dirname, '..');

  let targets = [];
  if (args.includes('--all')) {
    targets = listGlbFiles(workspaceRoot);
  } else if (args.length === 0) {
    console.error('Usage: node tools/inspect-glb-animations.js <file.glb|folder|--all>');
    process.exitCode = 2;
    return;
  } else {
    const p = path.resolve(process.cwd(), args[0]);
    if (isDirectory(p)) targets = listGlbFiles(p);
    else targets = [p];
  }

  if (!targets.length) {
    console.log('No .glb files found for the given target.');
    return;
  }

  for (const filePath of targets) {
    let report;
    try {
      report = inspectFile(filePath);
    } catch (e) {
      console.log(`\n=== ${path.relative(workspaceRoot, filePath)} ===`);
      console.log(`Error: ${e.message}`);
      continue;
    }

    console.log(`\n=== ${path.relative(workspaceRoot, report.filePath)} ===`);
    console.log(`Animations: ${report.animationCount}`);
    for (const anim of report.animations) {
      console.log(
        `- [${anim.index}] ${anim.name} | duration=${formatSeconds(anim.duration)} | channels=${anim.channelCount} | samplers=${anim.samplerCount} | targets=${anim.targetNodeCount} | paths=${anim.targetPaths.join(', ') || 'n/a'}`
      );
    }
  }
}

main();
