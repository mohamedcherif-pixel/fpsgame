const { app, BrowserWindow, globalShortcut, crashReporter, dialog } = require('electron');
const { autoUpdater } = require('electron-updater');
const path = require('path');

// Configure auto-updater
autoUpdater.autoDownload = true;
autoUpdater.autoInstallOnAppQuit = true;

// Enable crash reporting
crashReporter.start({
    productName: 'TAYA7-SAYEB',
    companyName: 'TAYA7',
    submitURL: '',
    uploadToServer: false
});

// GPU flags for better WebGL compatibility
app.commandLine.appendSwitch('ignore-gpu-blacklist');
app.commandLine.appendSwitch('enable-gpu-rasterization');
app.commandLine.appendSwitch('enable-zero-copy');
app.commandLine.appendSwitch('disable-gpu-sandbox');
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('disable-software-rasterizer');

// CRITICAL: Audio fixes for WebRTC crash (sync_reader.cc issue)
// Disable audio INPUT (microphone) since we only use WebRTC for data, not voice
// Keep audio OUTPUT enabled for game sounds!
app.commandLine.appendSwitch('disable-audio-input');
// Use a fake device for media stream to prevent WebRTC audio capture conflicts
app.commandLine.appendSwitch('use-fake-device-for-media-stream');
// Disable WebRTC hardware encoding/decoding we don't need
app.commandLine.appendSwitch('disable-webrtc-hw-encoding');
app.commandLine.appendSwitch('disable-webrtc-hw-decoding');
// Autoplay policy to allow game sounds
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');

// Increase memory limits for WebGL
app.commandLine.appendSwitch('js-flags', '--max-old-space-size=4096');

// CRITICAL: Disable hardware acceleration to test if GPU is the issue
// app.disableHardwareAcceleration();

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1920,
        height: 1080,
        fullscreen: true, // Always start in fullscreen
        autoHideMenuBar: true,
        icon: path.join(__dirname, 'icon.ico'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: true,
            allowRunningInsecureContent: false,
            preload: path.join(__dirname, 'preload.js'),
            backgroundThrottling: false,
            webgl: true,
            experimentalFeatures: true
        }
    });

    // Load the game
    mainWindow.loadFile(path.join(__dirname, 'game', 'fps-game.html'));

    // Open DevTools for debugging - REMOVE IN PRODUCTION
    mainWindow.webContents.openDevTools();

    // Remove menu bar
    mainWindow.setMenuBarVisibility(false);

    // Handle page crashes
    mainWindow.webContents.on('crashed', () => {
        console.log('Page crashed, reloading...');
        mainWindow.reload();
    });

    // Handle render process gone
    mainWindow.webContents.on('render-process-gone', (event, details) => {
        console.log('=== RENDERER CRASH DETAILS ===');
        console.log('Reason:', details.reason);
        console.log('Exit Code:', details.exitCode);
        console.log('Full details:', JSON.stringify(details, null, 2));
        console.log('=============================');
        
        // Don't auto-reload to see the error
        if (details.reason === 'crashed' || details.reason === 'oom') {
            console.log('CRITICAL: Renderer crashed! Check GPU/WebGL issues.');
        }
    });

    // Handle console messages from the renderer
    mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
        if (level >= 2) { // warnings and errors
            console.log(`[Renderer ${level}]: ${message}`);
        }
    });

    // Handle fullscreen toggle with F11
    mainWindow.on('enter-full-screen', () => {
        console.log('Entered fullscreen');
    });

    mainWindow.on('leave-full-screen', () => {
        console.log('Left fullscreen');
    });

    // Handle window close
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Prevent the ESC key from exiting fullscreen (handled by game)
    mainWindow.webContents.on('before-input-event', (event, input) => {
        // Allow game to handle ESC for pause menu
        if (input.key === 'Escape') {
            // Don't prevent - let the game handle it
        }
    });
}

// App ready
app.whenReady().then(() => {
    createWindow();

    // Check for updates after window is ready
    setTimeout(() => {
        checkForUpdates();
    }, 3000); // Wait 3 seconds before checking

    // Register F11 for fullscreen toggle
    globalShortcut.register('F11', () => {
        if (mainWindow) {
            mainWindow.setFullScreen(!mainWindow.isFullScreen());
        }
    });

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// ============================================
// AUTO-UPDATE SYSTEM
// ============================================
function checkForUpdates() {
    console.log('🔄 Checking for updates...');
    autoUpdater.checkForUpdates().catch(err => {
        console.log('Update check failed:', err.message);
    });
}

// Update events
autoUpdater.on('checking-for-update', () => {
    console.log('🔍 Checking for update...');
});

autoUpdater.on('update-available', (info) => {
    console.log('📦 Update available:', info.version);
    dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Update Available',
        message: `A new version (${info.version}) is available!`,
        detail: 'Downloading update in the background...',
        buttons: ['OK']
    });
});

autoUpdater.on('update-not-available', () => {
    console.log('✅ Game is up to date!');
});

autoUpdater.on('download-progress', (progress) => {
    const percent = Math.round(progress.percent);
    console.log(`⬇️ Downloading: ${percent}%`);
    if (mainWindow) {
        mainWindow.setProgressBar(progress.percent / 100);
    }
});

autoUpdater.on('update-downloaded', (info) => {
    console.log('✅ Update downloaded:', info.version);
    if (mainWindow) {
        mainWindow.setProgressBar(-1); // Remove progress bar
    }
    
    dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Update Ready',
        message: 'Update downloaded!',
        detail: 'The game will restart to install the update.',
        buttons: ['Restart Now', 'Later']
    }).then((result) => {
        if (result.response === 0) {
            autoUpdater.quitAndInstall(false, true);
        }
    });
});

autoUpdater.on('error', (err) => {
    console.log('❌ Update error:', err.message);
});

// Quit when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Unregister shortcuts on quit
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});
