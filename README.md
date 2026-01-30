# TAYA7 SAYEB - FPS Multiplayer Game

A browser and desktop FPS (First Person Shooter) game built with Three.js, featuring real-time multiplayer via WebRTC (PeerJS) and Socket.IO.

---

## 📁 Project Structure

```
fpsgame/
├── electron/                    # Electron desktop app
│   ├── dist/                    # Build output directory
│   ├── game/                    # Game files for Electron
│   │   ├── fps-game.html        # Main game file (9400+ lines)
│   │   ├── diesound.mp3         # Death sound effect
│   │   ├── gun/                 # Weapon sounds
│   │   │   ├── ak47.mp3
│   │   │   ├── awp.mp3
│   │   │   └── deagle.mp3
│   │   ├── hitmark.png          # Hit marker image
│   │   ├── RifleIdle.fbx/.glb   # Weapon 3D model
│   │   ├── T_PostalDude.png     # Character texture
│   │   └── Speaker_Icon.svg.png # Audio icon
│   ├── main.js                  # Electron main process
│   ├── preload.js               # Electron preload script
│   ├── package.json             # Electron dependencies
│   ├── BUILD_INSTRUCTIONS.md    # Build instructions
│   └── node_modules/            # Electron dependencies
│
├── fps-game.html                # Browser version (synced from electron/game/)
├── diesound.mp3                 # Death sound (root copy)
├── gun/                         # Weapon sounds (root copy)
│   ├── ak47.mp3
│   ├── awp.mp3
│   ├── deagle.mp3
│   └── hitmark.png
│
├── server.js                    # Socket.IO server for 2v2 mode
├── package.json                 # Server dependencies
├── node_modules/                # Server dependencies
│
├── RifleIdle.fbx               # 3D model backup
├── T_PostalDude.png            # Texture backup
├── SETUP_SERVER.txt            # Server setup instructions
└── .git/                        # Git repository
```

---

## 🎮 Game Features

### Core Gameplay
- **First Person Shooter** with WASD movement, mouse look, jumping, crouching
- **Multiple Weapons**: AK-47, AWP, Deagle (with unique sounds and stats)
- **Health System**: 100 HP, damage indicators, death and respawn
- **Hit Detection**: Raycasting with headshot multiplier

### Multiplayer Modes
1. **1v1 PeerJS** - Direct WebRTC connection (peer-to-peer, no server needed)
2. **2v2 Socket.IO** - Server-based team matchmaking
3. **AI Practice** - Play against bots

### Progression System
- **Level System**: XP gained from kills, level rings displayed on character
- **Statistics**: Kills, deaths, headshots tracked in localStorage
- **Profile Pictures**: Upload custom avatar or auto-generate from initials

### UI/HUD Elements
- **CS2-Style Scoreboard**: Minimal top bar showing avatars and scores
- **Health Display**: 3D inverse tilt effect following mouse movement
- **Kill Feed**: Shows recent kills with weapon icons
- **Crosshair**: Dynamic spread indicator
- **Squad List**: Pre-game lobby showing all players with levels and avatars

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Electron** | 28.3.3 | Desktop app wrapper |
| **Three.js** | r128 | 3D rendering engine |
| **PeerJS** | 1.4.7 | WebRTC peer-to-peer connections |
| **Socket.IO** | 4.5.4 | Server-based multiplayer |
| **Express** | 4.18.2 | HTTP server for Socket.IO |
| **Web Audio API** | Native | 3D positional audio |

---

## 🚀 Running the Game

### Option 1: Browser Version
Simply open `fps-game.html` in a web browser (Chrome recommended).

### Option 2: Electron Desktop App
```powershell
cd electron
npm install
npm start
```

### Option 3: Build Executable
```powershell
cd electron
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

### Running the Multiplayer Server (for 2v2 mode)
```powershell
# In root directory
npm install
npm start
# Server runs on http://localhost:3000
```

---

## 📜 Key Code Sections (fps-game.html)

### Main Systems

| System | Location | Description |
|--------|----------|-------------|
| `LevelSystem` | ~line 5450 | XP/level tracking, localStorage persistence |
| `ProfilePicture` | ~line 5480 | Avatar upload, storage, display |
| `loadSounds()` | ~line 5567 | Audio file loading (weapons, death) |
| `updateCS2Scoreboard()` | ~line 8180 | Top scoreboard UI |
| `updateSquadListPanel()` | ~line 5348 | Lobby player list |

### Multiplayer Functions

| Function | Description |
|----------|-------------|
| `connectToPlayer()` | PeerJS WebRTC connection |
| `handleNetworkData()` | Process incoming multiplayer messages |
| `sendToOther()` | Send data to connected peer |
| `syncOtherPlayerPosition()` | Update other player's position |

### Combat Functions

| Function | Description |
|----------|-------------|
| `shoot()` | Handle weapon firing, hit detection |
| `takeDamage()` | Process incoming damage |
| `playerDied()` | Handle local player death |
| `otherPlayerDied()` | Handle remote player death |
| `respawn()` | Reset player after death |

### Network Message Types

| Type | Purpose |
|------|---------|
| `position` | Player position/rotation sync |
| `hit` | Damage notification |
| `death` | Death notification |
| `respawn` | Respawn notification |
| `lobbyJoined` | Player joined lobby |
| `hostInfo` | Host sends info to client |
| `gameStart` | Game starting signal |

---

## 💾 Data Storage (localStorage)

| Key | Data |
|-----|------|
| `taya7_player_data` | `{ level, xp, xpToNext, totalXp, kills, deaths, headshots }` |
| `taya7_profile_picture` | Base64 encoded avatar image |
| `playerName` | Username string |

---

## 🎨 Visual Features

- **Level Ring**: Colored ring around character based on level (bronze→silver→gold→platinum→diamond)
- **Hover Tooltip**: Shows XP progress when hovering level indicator
- **3D Health HUD**: Health display with inverse 3D tilt effect
- **Hit Markers**: Visual feedback on successful hits
- **Kill Feed**: Recent kills with weapon icons

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| W/A/S/D | Move |
| Mouse | Look around |
| Left Click | Shoot |
| Space | Jump |
| Ctrl | Crouch |
| R | Reload |
| 1/2/3 | Switch weapons |
| Tab | Show scoreboard |
| Escape | Pause menu |
| F11 | Toggle fullscreen |

---

## 🐛 Known Issues & Fixes Applied

1. **Death Sound Not Playing**: Fixed by calling `loadSounds()` after function definition
2. **LevelSystem Undefined**: Fixed by adding `window.LevelSystem = LevelSystem`
3. **AudioContext Errors**: Added null checks before accessing `audioContext.currentTime`
4. **Respawn Not Synced**: Added 'respawn' message type and handler
5. **Squad List During Gameplay**: Hidden when game starts with `gameState.started` check
6. **WebRTC Audio Crash**: Fixed with Electron flags disabling audio input

---

## 📝 Development Notes

### Syncing Browser and Electron Versions
After editing `electron/game/fps-game.html`, sync to root:
```powershell
Copy-Item "electron\game\fps-game.html" "fps-game.html" -Force
```

### Electron Audio Flags (main.js)
```javascript
app.commandLine.appendSwitch('disable-audio-input');
app.commandLine.appendSwitch('use-fake-device-for-media-stream');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
```

### Server Deployment
The Socket.IO server can be deployed to:
- Glitch.com
- Heroku
- Render.com
- Any Node.js hosting

---

## 📊 File Sizes

| File | Size | Purpose |
|------|------|---------|
| `fps-game.html` | ~400KB | All game code (9400+ lines) |
| `diesound.mp3` | ~50KB | Death sound |
| `ak47.mp3` | ~30KB | AK-47 sound |
| `awp.mp3` | ~40KB | AWP sound |
| `deagle.mp3` | ~25KB | Deagle sound |

---

## 🔧 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      TAYA7 SAYEB FPS GAME                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Three.js  │    │   PeerJS    │    │  Socket.IO  │         │
│  │  (Render)   │    │  (1v1 P2P)  │    │  (2v2 Server)│         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │                                    │
│                    ┌───────┴───────┐                           │
│                    │  Game State   │                           │
│                    │   Manager     │                           │
│                    └───────┬───────┘                           │
│                            │                                    │
│         ┌─────────┬────────┼────────┬─────────┐                │
│         │         │        │        │         │                │
│    ┌────┴────┐┌───┴───┐┌───┴───┐┌───┴───┐┌────┴────┐          │
│    │ Player  ││Combat ││ Level ││Profile││  Audio  │          │
│    │ Control ││System ││System ││Picture││ System  │          │
│    └─────────┘└───────┘└───────┘└───────┘└─────────┘          │
│                                                                 │
│                    ┌───────────────┐                           │
│                    │  localStorage │                           │
│                    │  (Persistence)│                           │
│                    └───────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📞 Support

For issues or questions, check:
1. DevTools console (F12) for errors
2. Electron DevTools (auto-opens in dev mode)
3. Server logs for multiplayer issues

---

*Last updated: Session with comprehensive death/respawn fixes, CS2 scoreboard, level system, and profile pictures.*
