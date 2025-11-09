# 🌐 FPS Game - Global Multiplayer Setup

## 🎮 PLAY FROM ANYWHERE IN THE WORLD!

The game now supports **global multiplayer** with enhanced connection handling, automatic reconnection, and connection quality monitoring!

### Quick Start:
1. **Deploy your server** (see options below - takes 5 minutes!)
2. Add your server URL to `fps-game.html` (line ~382)
3. Open `fps-game.html` in your browser
4. Click **"HOST GAME"** or **"JOIN GAME"**
5. Share the Room ID with your friend
6. **Play from anywhere in the world!** 🌍

### Features:
- ✅ **Global connectivity** - Works from any country
- ✅ **Auto-reconnection** - Automatically reconnects if connection drops
- ✅ **Connection quality indicator** - See your connection status in-game
- ✅ **Latency measurement** - Real-time ping display
- ✅ **Multiple server support** - Try multiple servers automatically
- ✅ **Enhanced error handling** - Better error messages and recovery

---

## 🚀 HOST YOUR OWN SERVER (Recommended)

### Option 1: Glitch.com (FREE & EASY)

1. Go to https://glitch.com/
2. Click **"New Project"** → **"hello-express"**
3. Delete the existing code in `server.js`
4. Copy the code from `server.js` in this folder
5. Paste it into Glitch's `server.js`
6. Click **"package.json"** and replace with:
   ```json
   {
     "name": "fps-game-server",
     "version": "1.0.0",
     "main": "server.js",
     "scripts": {
       "start": "node server.js"
     },
     "dependencies": {
       "express": "^4.18.2",
       "socket.io": "^4.5.4"
     }
   }
   ```
7. Glitch will auto-install and start your server
8. Copy your Glitch URL (e.g., `https://your-project.glitch.me`)
9. In `fps-game.html`, find line ~383 and change:
   ```javascript
   const SERVER_URL = 'https://your-project.glitch.me';
   ```
10. Done! Your game now uses your own server!

---

### Option 2: Heroku (FREE)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Open terminal in the `fpsgame` folder
3. Run:
   ```bash
   heroku login
   heroku create your-fps-server
   git init
   git add server.js package.json
   git commit -m "FPS server"
   git push heroku master
   ```
4. Copy your Heroku URL
5. Update `SERVER_URL` in `fps-game.html`

---

### Option 3: Local Server (Testing)

1. Install Node.js: https://nodejs.org/
2. Open terminal in the `fpsgame` folder
3. Run:
   ```bash
   npm install
   node server.js
   ```
4. Server runs on `http://localhost:3000`
5. Update `SERVER_URL` to `'http://localhost:3000'`
6. **Note:** Only works on your local network

---

## 🎯 HOW IT WORKS

### Architecture:
```
Player 1 (Browser)  ←→  Socket.IO Server  ←→  Player 2 (Browser)
     ↓                         ↓                      ↓
  Position Data          Relay Messages         Position Data
  Shooting Events        Room Management        Shooting Events
```

### Data Flow:
1. **Host** creates a room with random ID
2. **Guest** joins using the Room ID
3. Both players send position/shooting data to server
4. Server relays data to the other player
5. Real-time synchronization at 20 updates/sec

### Features:
- ✅ Real-time position sync
- ✅ Shooting and damage sync
- ✅ Room-based matchmaking
- ✅ Automatic disconnect handling
- ✅ Works globally (any distance)
- ✅ Low latency (< 100ms typically)

---

## 🔧 TROUBLESHOOTING

### "Connection timeout"
- Check if server is running
- Try a different server URL
- Check browser console for errors

### "Room not found"
- Make sure host created room first
- Check Room ID is correct (case-sensitive)
- Both players must use same server

### High latency
- Use a server closer to both players
- Check internet connection
- Consider hosting your own server

---

## 📊 SERVER REQUIREMENTS

- **Node.js**: 18.x or higher
- **RAM**: 256MB minimum
- **Bandwidth**: ~10KB/s per player
- **Concurrent Players**: Depends on hosting plan

---

## 🎮 GAME MODES

1. **🌐 HOST GAME** - Create online room
2. **🔗 JOIN GAME** - Join friend's room
3. **🤖 PLAY vs AI** - Offline mode

---

## 💡 TIPS

- Share Room ID via Discord, WhatsApp, etc.
- Room IDs are case-sensitive
- Server can handle multiple rooms simultaneously
- Each room supports 2 players (1v1)
- Game starts when both players connect

---

## 🆘 SUPPORT

If you have issues:
1. Check browser console (F12)
2. Verify server is running
3. Test with "PLAY vs AI" to confirm game works
4. Try different browser (Chrome recommended)

---

**Enjoy your online FPS game! 🎮🔫**
