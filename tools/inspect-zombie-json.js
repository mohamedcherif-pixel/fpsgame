#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const jsonPath = path.resolve(__dirname, '../zombie_animations/ONLP8KVB4954FVUSK667OC97P.json');

const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

console.log(`\n=== Zombie Animations (Three.js JSON Model) ===\n`);

if (data.animations && Array.isArray(data.animations)) {
  console.log(`Total animation clips: ${data.animations.length}\n`);
  
  data.animations.forEach((anim, idx) => {
    const name = anim.name || `animation_${idx}`;
    const fps = anim.fps || 'unknown';
    const length = anim.length || 0;
    const tracks = anim.tracks ? anim.tracks.length : 0;
    
    console.log(`[${idx}] ${name}`);
    console.log(`    FPS: ${fps}, Frames: ${length}, Tracks: ${tracks}`);
    if (anim.tracks && anim.tracks.length > 0) {
      console.log(`    Track names: ${anim.tracks.map(t => t.name).join(' | ')}`);
    }
  });
} else {
  console.log('No animations array found in the model.');
}

// Show skeletal structure
if (data.skeletons && data.skeletons.length > 0) {
  console.log(`\nSkeleton info: ${data.skeletons.length} skeleton(s)`);
  data.skeletons.forEach((skel, i) => {
    console.log(`  [${i}] Bones: ${skel.bones.length}`);
  });
}
