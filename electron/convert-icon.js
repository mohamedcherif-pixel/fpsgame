const sharp = require('sharp');
const toIco = require('to-ico');
const fs = require('fs');
const path = require('path');

async function convertToIcon() {
    const inputPath = path.join(__dirname, '..', 'gamephoto.jpg');
    const pngPath = path.join(__dirname, 'icon.png');
    const icoPath = path.join(__dirname, 'icon.ico');

    console.log('Converting gamephoto.jpg to icon formats...');

    try {
        // Read the JPG and convert to PNG (256x256 for high quality icon)
        await sharp(inputPath)
            .resize(256, 256)
            .png()
            .toFile(pngPath);
        console.log('✅ Created icon.png (256x256)');

        // Create multiple sizes for ICO
        const sizes = [16, 32, 48, 64, 128, 256];
        const pngBuffers = await Promise.all(
            sizes.map(size => 
                sharp(inputPath)
                    .resize(size, size)
                    .png()
                    .toBuffer()
            )
        );
        
        // Convert to ICO
        const icoBuffer = await toIco(pngBuffers);
        fs.writeFileSync(icoPath, icoBuffer);
        console.log('✅ Created icon.ico (multi-size)');

        console.log('\n✅ Icon conversion complete!');
        console.log('Files created:');
        console.log('  - electron/icon.png');
        console.log('  - electron/icon.ico');
    } catch (error) {
        console.error('Error converting icon:', error);
        process.exit(1);
    }
}

convertToIcon();
