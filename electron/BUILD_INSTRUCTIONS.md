# TAYA7 SAYEB - Desktop Build Instructions

## Quick Setup

1. **Navigate to the electron folder:**
   ```
   cd electron
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Copy game files:**
   - Create a `game` folder inside `electron`
   - Copy `fps-game.html` into the `game` folder
   - Copy the `gun` folder into the `game` folder

4. **Run in development mode:**
   ```
   npm start
   ```

5. **Build executable:**
   ```
   npm run build:win    # For Windows (.exe installer)
   npm run build:mac    # For macOS (.dmg)
   npm run build:linux  # For Linux (.AppImage)
   ```

## Folder Structure

```
electron/
├── package.json
├── main.js
├── preload.js
├── icon.ico          (Windows icon - 256x256)
├── icon.icns         (macOS icon)
├── icon.png          (Linux icon - 512x512)
└── game/
    ├── fps-game.html
    └── gun/
        └── (all gun model files)
```

## Adding an Icon

1. Create a 512x512 PNG image for your game icon
2. Save it as `icon.png` in the electron folder
3. For Windows: Convert to .ico format (256x256)
4. For macOS: Convert to .icns format

## Output

After building, find your installer in:
- `electron/dist/` folder
- Windows: `TAYA7 SAYEB Setup x.x.x.exe`
- macOS: `TAYA7 SAYEB-x.x.x.dmg`
- Linux: `TAYA7-SAYEB-x.x.x.AppImage`

## Notes

- The game runs in fullscreen by default
- Press F11 to toggle fullscreen
- ESC opens the pause menu (doesn't exit fullscreen)
- All multiplayer features work the same way
