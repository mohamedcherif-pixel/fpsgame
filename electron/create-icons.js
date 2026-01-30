const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const toIco = require('to-ico');

async function createInstallerAssets() {
    const inputPath = path.join(__dirname, '..', 'gamephoto.jpg');
    const buildDir = path.join(__dirname, 'build');
    
    // Ensure build directory exists
    if (!fs.existsSync(buildDir)) {
        fs.mkdirSync(buildDir, { recursive: true });
    }

    console.log('🎨 Creating professional installer assets...\n');
    console.log('Source image:', inputPath);
    console.log('File exists:', fs.existsSync(inputPath));

    try {
        // Read source image info
        const metadata = await sharp(inputPath).metadata();
        console.log('Source image size:', metadata.width, 'x', metadata.height);
        console.log('Source format:', metadata.format);
        console.log('');

        // 1. Create icon.png (256x256)
        const pngPath = path.join(__dirname, 'icon.png');
        await sharp(inputPath)
            .resize(256, 256, {
                fit: 'cover',
                position: 'centre'
            })
            .flatten({ background: { r: 255, g: 255, b: 255 } })
            .png({ compressionLevel: 9 })
            .toFile(pngPath);
        console.log('✅ Created icon.png (256x256)');

        // 2. Create icon.ico (multi-size for Windows)
        const icoPath = path.join(__dirname, 'icon.ico');
        const sizes = [16, 32, 48, 64, 128, 256];
        const pngBuffers = [];
        
        for (const size of sizes) {
            const buffer = await sharp(inputPath)
                .resize(size, size, {
                    fit: 'cover',
                    position: 'centre'
                })
                .flatten({ background: { r: 255, g: 255, b: 255 } })
                .png()
                .toBuffer();
            pngBuffers.push(buffer);
        }
        
        const icoBuffer = await toIco(pngBuffers);
        fs.writeFileSync(icoPath, icoBuffer);
        console.log('✅ Created icon.ico (multi-size: 16, 32, 48, 64, 128, 256)');

        // 3. Create installer sidebar image (164x314 - NSIS wizard sidebar) as PNG first then we skip BMP
        const sidebarPath = path.join(buildDir, 'installerSidebar.bmp');
        // Sharp doesn't support BMP, so create as PNG and NSIS will handle it
        const sidebarPngPath = path.join(buildDir, 'installerSidebar.png');
        await sharp(inputPath)
            .resize(164, 314, { 
                fit: 'cover',
                position: 'centre'
            })
            .flatten({ background: { r: 0, g: 0, b: 0 } })
            .png()
            .toFile(sidebarPngPath);
        console.log('✅ Created installerSidebar.png (164x314)');

        // 4. Copy icons to build folder too
        fs.copyFileSync(pngPath, path.join(buildDir, 'icon.png'));
        fs.copyFileSync(icoPath, path.join(buildDir, 'icon.ico'));
        console.log('✅ Copied icons to build folder');

        console.log('\n✅ All installer assets created successfully!');
        console.log('\nNow run: npm run build:win');

    } catch (error) {
        console.error('Error creating assets:', error);
        process.exit(1);
    }
}

createInstallerAssets();
