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

    try {
        // 1. Create icon.png (256x256)
        const pngPath = path.join(__dirname, 'icon.png');
        await sharp(inputPath)
            .resize(256, 256)
            .png()
            .toFile(pngPath);
        console.log('✅ Created icon.png (256x256)');

        // 2. Create icon.ico (multi-size for Windows)
        const icoPath = path.join(__dirname, 'icon.ico');
        const sizes = [16, 32, 48, 64, 128, 256];
        const pngBuffers = await Promise.all(
            sizes.map(size => 
                sharp(inputPath)
                    .resize(size, size)
                    .png()
                    .toBuffer()
            )
        );
        const icoBuffer = await toIco(pngBuffers);
        fs.writeFileSync(icoPath, icoBuffer);
        console.log('✅ Created icon.ico (multi-size)');

        // 3. Create installer sidebar image (164x314 - NSIS wizard sidebar)
        const sidebarPath = path.join(buildDir, 'installerSidebar.bmp');
        await sharp(inputPath)
            .resize(164, 314, { fit: 'cover' })
            .flatten({ background: { r: 0, g: 0, b: 0 } })
            .toFile(sidebarPath);
        console.log('✅ Created installerSidebar.bmp (164x314)');

        // 4. Create installer header image (150x57 - NSIS header)
        const headerPath = path.join(buildDir, 'installerHeader.bmp');
        await sharp(inputPath)
            .resize(150, 57, { fit: 'cover' })
            .flatten({ background: { r: 0, g: 0, b: 0 } })
            .toFile(headerPath);
        console.log('✅ Created installerHeader.bmp (150x57)');

        // 5. Create uninstaller sidebar (same as installer)
        const uninstallSidebarPath = path.join(buildDir, 'uninstallerSidebar.bmp');
        fs.copyFileSync(sidebarPath, uninstallSidebarPath);
        console.log('✅ Created uninstallerSidebar.bmp');

        // 6. Create a large banner for welcome page (493x58)
        const bannerPath = path.join(buildDir, 'installerBanner.bmp');
        
        // Create a dark gaming banner with gradient
        const bannerWidth = 493;
        const bannerHeight = 58;
        
        // Create gradient background
        const gradientSvg = `
            <svg width="${bannerWidth}" height="${bannerHeight}">
                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#16213e;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#0f3460;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect width="100%" height="100%" fill="url(#grad)"/>
                <text x="250" y="38" font-family="Arial Black" font-size="24" fill="#e94560" text-anchor="middle" font-weight="bold">TAYA7 SAYEB</text>
            </svg>
        `;
        
        await sharp(Buffer.from(gradientSvg))
            .toFile(bannerPath);
        console.log('✅ Created installerBanner.bmp (493x58)');

        console.log('\n✅ All installer assets created successfully!');
        console.log('\nFiles in build/:');
        fs.readdirSync(buildDir).forEach(file => {
            console.log(`  - ${file}`);
        });

    } catch (error) {
        console.error('Error creating assets:', error);
        process.exit(1);
    }
}

createInstallerAssets();
