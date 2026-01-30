
import os
import re

FILES = [
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\fps-game.html",
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\electron\game\fps-game.html"
]

NEW_UI_HTML = """
    <div id="startScreen">
        <!-- HIDDEN LEGACY CONTROLS (Preserves existing game logic listeners) -->
        <div id="legacy-controls" style="display: none;">
            <button id="hostButton">Legacy Host</button>
            <button id="joinButton">Legacy Join</button>
            <button id="host2v2Button">Legacy Host 2v2</button>
            <button id="join2v2Button">Legacy Join 2v2</button>
            <button id="startButton">Legacy Start AI</button>
            <button id="startGameButton">Legacy Launch</button>
            <button id="connectButton">Legacy Connect</button>
            <button id="cancelButton">Legacy Cancel</button>
        </div>

        <!-- HIDDEN INPUTS (Logic reads these) -->
        <input type="file" id="profilePictureInput" accept="image/*" style="display: none;">

        <!-- NEW MAIN MENU CONTAINER -->
        <div class="menu-content" id="mainMenuContainer">
            <div class="menu-header">
                <h1>FPS GAME</h1>
                <div class="menu-subtitle">TACTICAL FRAMEWORK</div>
            </div>

            <!-- Profile Section -->
            <div class="menu-profile-section">
                <input type="text" id="usernameInput" placeholder="SOLDIER NAME" maxlength="12" class="menu-input user-input-styled">
            </div>

            <!-- Main Buttons -->
            <div class="menu-button-group tactical-group" id="primaryMenuButtons">
                <button class="menu-button tactical-btn" onclick="openArenaSelect('ai')">
                    <span class="btn-icon">💀</span> CAMPAIGN (VS AI)
                </button>
                
                <div class="btn-row">
                    <button class="menu-button tactical-btn half-width" onclick="openArenaSelect('host_1v1')">
                        <span class="btn-icon">📡</span> DEPLOY (HOST)
                    </button>
                    <button class="menu-button tactical-btn half-width" onclick="showJoinMenu()">
                        <span class="btn-icon">🔗</span> JOIN
                    </button>
                </div>
                 
                <div class="btn-row">
                    <button class="menu-button tactical-btn half-width" onclick="openArenaSelect('host_2v2')">
                       <span class="btn-icon">👥</span> SQUAD HOST
                    </button>
                     <button class="menu-button tactical-btn half-width" onclick="showJoinMenu()">
                       <span class="btn-icon">➕</span> SQUAD JOIN
                    </button>
                </div>

                <div class="menu-divider"></div>

                <button class="menu-button tactical-btn locker-btn" onclick="openLocker()">
                    <span class="btn-icon">🎒</span> OPERATOR LOCKER
                </button>
                
                <button id="keybindsButton" onclick="openKeybindsModal()" class="menu-button tactical-btn">
                     <span class="btn-icon">⚙</span> OPTIONS
                </button>
            </div>
            
            <!-- JOIN MENU (Replaces buttons) -->
             <div id="joinMenuOverlay" style="display: none;" class="tactical-group">
                 <div class="menu-label">CONNECTION UPLINK</div>
                 <input type="text" id="joinRoomId" placeholder="ENTER SERVER ID" class="menu-input user-input-styled">
                 <div class="btn-row">
                    <button class="menu-button tactical-btn confirm-btn" onclick="proxyJoin()">CONNECT</button>
                    <button class="menu-button tactical-btn cancel-btn" onclick="hideJoinMenu()">BACK</button>
                 </div>
             </div>
             
             <!-- HOST STATUS -->
            <div id="hostStatusOverlay" style="display: none;" class="tactical-group">
                <div class="menu-label">HOSTING SERVER</div>
                <input type="text" id="roomId" readonly class="menu-input user-input-styled readonly">
                <!-- Logic updates 'waitingText' -->
                <div id="waitingText" class="status-text">WAITING FOR OPFOR...</div>
                
                <button class="menu-button tactical-btn confirm-btn" onclick="proxyStartGame()" id="visibleStartGameBtn" style="display:none; margin-top: 10px;">LAUNCH MISSION</button>
                <button class="menu-button tactical-btn cancel-btn" onclick="location.reload()" style="margin-top: 5px;">ABORT MISSION</button>
            </div>
            
             <!-- Hidden Legacy Elements targets for logic -->
             <div id="multiplayerSetup" style="display: none;">
                 <div id="hostInfo"></div>
                 <div id="joinInfo"></div>
             </div>

            <div class="controls" style="display: none;">
                <strong>CONTROLS:</strong><br>
                ZQSD - Move | Mouse - Look | Left Click - Shoot | R - Reload<br>
                1, 2, 3 - Switch Weapons | F - Toggle DOF | ESC - Pause<br>
            </div>
        </div>

        <!-- MODAL: ARENA SELECT -->
        <div id="arenaSelectorModal" class="modal-overlay">
             <div class="modal-content tactical-card">
                <div class="card-header">
                    <h2>MISSION SELECT</h2>
                    <div class="card-subtitle">CHOOSE DEPLOYMENT ZONE</div>
                </div>
                
                <div class="map-grid">
                    <div class="map-card selected" onclick="selectMapGUI(this, 'default')">
                       <div class="map-preview default-map"></div>
                        <div class="map-name">WAREHOUSE</div>
                    </div>
                    <div class="map-card" onclick="selectMapGUI(this, 'map1')">
                        <div class="map-preview map1-map"></div>
                        <div class="map-name">ARENA</div>
                    </div>
                </div>
                
                <div class="card-actions">
                    <button id="confirmDeployBtn" class="action-btn deploy-btn" onclick="executeDeploy()">INITIATE DROP</button>
                    <button onclick="closeArenaSelect()" class="action-btn close-btn">CANCEL</button>
                </div>
             </div>
        </div>

        <!-- MODAL: LOCKER -->
        <div id="lockerModal" class="modal-overlay">
             <div class="modal-content tactical-card locker-card">
                <div class="card-header">
                    <h2>OPERATOR LOCKER</h2>
                    <div class="card-subtitle">CUSTOMIZE LOADOUT</div>
                </div>
                
                <div class="skin-grid">
                    <div class="skin-card selected" onclick="selectSkinGUI(this, 'soldier')">
                        <div class="skin-icon">🔫</div>
                        <div class="skin-name">SOLDIER</div>
                    </div>
                    <div class="skin-card" onclick="selectSkinGUI(this, 'briefcase')">
                        <div class="skin-icon">💼</div>
                        <div class="skin-name">EXECUTIVE</div>
                    </div>
                    <div class="skin-card" onclick="selectSkinGUI(this, 'skeleton')">
                        <div class="skin-icon">💀</div>
                        <div class="skin-name">SKELETON</div>
                    </div>
                    <div class="skin-card" onclick="selectSkinGUI(this, 'zombie')">
                        <div class="skin-icon">🧟</div>
                        <div class="skin-name">ZOMBIE</div>
                    </div>
                </div>
                
                <div class="card-actions">
                    <button onclick="closeLocker()" class="action-btn confirm-btn">CONFIRM LOADOUT</button>
                </div>
             </div>
        </div>
    </div>

    <!-- INJECTED UI ASSETS -->
    <style>
        /* NEW UI STYLES */
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap');
        
        #startScreen {
            background: radial-gradient(circle at center, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%);
            padding-left: 0 !important; /* Reset legacy padding */
            justify-content: center;
            align-items: center; 
            /* Center the menu now, closer to character which is usually center-screen */
        }
        
        .menu-content {
            background: rgba(12, 16, 20, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid #ffa500;
            padding: 30px;
            width: 380px;
            transform: skewX(-2deg);
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            /* Position relative to left side but not stuck to edge */
            margin-right: 300px; /* Push bit left to show character */
        }
        
        .menu-header {
            margin-bottom: 25px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
        }
        
        .menu-header h1 {
            color: #fff;
            font-size: 32px;
            margin: 0;
            letter-spacing: 4px;
            text-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
        }
        
        .menu-subtitle {
            color: #ffa500;
            font-size: 10px;
            letter-spacing: 4px;
            font-weight: 700;
        }
        
        .user-input-styled {
            background: rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            padding: 12px !important;
            font-size: 16px !important;
            color: #fff !important;
            font-weight: 600 !important;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .user-input-styled:focus {
            border-color: #ffa500 !important;
            box-shadow: 0 0 15px rgba(255,165,0,0.2);
        }

        .menu-button-group.tactical-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 20px;
        }
        
        .btn-row {
            display: flex;
            gap: 8px;
        }
        
        .tactical-btn {
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 0%, transparent 100%);
            border: 1px solid rgba(255,255,255,0.1);
            color: #ccc;
            padding: 12px 16px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
            text-shadow: none;
        }
        
        .tactical-btn:hover {
            background: rgba(255, 165, 0, 0.1);
            border-color: #ffa500;
            color: #fff;
            padding-left: 20px;
            box-shadow: 0 0 20px rgba(255,165,0,0.1);
        }
        
        .tactical-btn .btn-icon {
            margin-right: 10px;
            font-size: 14px;
            filter: grayscale(1);
        }
         .tactical-btn:hover .btn-icon {
            filter: grayscale(0);
        }
        
        .tactical-btn.half-width {
            flex: 1;
            justify-content: center;
        }
        .tactical-btn.half-width:hover {
            padding-left: 12px; /* disable slide for half width */
            transform: translateY(-2px);
        }
        
        .locker-btn {
            border-color: rgba(0, 200, 255, 0.3);
        }
        .locker-btn:hover {
            background: rgba(0, 200, 255, 0.1);
            border-color: #00ccff;
            box-shadow: 0 0 20px rgba(0, 200, 255,0.1);
        }
        
        .menu-divider {
            height: 1px;
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
        }
        
        /* MODALS */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(5px);
            z-index: 5000;
            display: none;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.3s ease;
        }
        
        .tactical-card {
            background: #0f1216;
            border: 1px solid #333;
            border-top: 4px solid #ffa500;
            width: 800px;
            max-width: 90%;
            padding: 0;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
        }
        
        .card-header {
            padding: 20px 30px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            background: linear-gradient(90deg, rgba(255,165,0,0.05), transparent);
        }
        
        .card-header h2 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 32px;
            margin: 0;
            color: #fff;
            letter-spacing: 2px;
        }
        .card-subtitle {
            color: #ffa500;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 2px;
            font-size: 12px;
            font-weight: 700;
        }
        
        .map-grid, .skin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            max-height: 60vh;
            overflow-y: auto;
        }
        
        .map-card, .skin-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        
        .map-card:hover, .skin-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.06);
            border-color: rgba(255,255,255,0.3);
        }
        
        .map-card.selected, .skin-card.selected {
            border-color: #ffa500;
            background: rgba(255,165,0,0.05);
            box-shadow: 0 0 20px rgba(255,165,0,0.15);
        }
        
        .locker-card .skin-card.selected {
             border-color: #00ccff;
             background: rgba(0,200,255,0.05);
             box-shadow: 0 0 20px rgba(0,200,255,0.15);
        }
        
        .map-preview {
            height: 120px;
            width: 100%;
            background-size: cover;
            background-position: center;
            opacity: 0.7;
        }
        .default-map { background: linear-gradient(135deg, #222, #111); } 
        /* TODO: Add real screenshots */
        
        .map-name, .skin-name {
            padding: 10px;
            text-align: center;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            color: #ccc;
            letter-spacing: 1px;
        }
        .selected .map-name { color: #ffa500; }
        .selected .skin-name { color: #00ccff; }
        
        .skin-icon {
            font-size: 48px;
            text-align: center;
            padding: 20px 0;
            filter: drop-shadow(0 0 10px rgba(0,0,0,0.5));
        }
        
        .card-actions {
            padding: 20px 30px;
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: flex-end;
            gap: 15px;
            background: rgba(0,0,0,0.2);
        }
        
        .action-btn {
            padding: 12px 30px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .deploy-btn, .confirm-btn {
            background: #ffa500;
            color: #000;
            clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
        }
        .deploy-btn:hover, .confirm-btn:hover {
            background: #ffc255;
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255,165,0,0.4);
        }
        
        .locker-card .confirm-btn {
            background: #00ccff;
        }
        .locker-card .confirm-btn:hover {
            background: #33ddff;
            box-shadow: 0 0 20px rgba(0,200,255,0.4);
        }
        
        .close-btn, .cancel-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            color: #888;
        }
        .close-btn:hover, .cancel-btn:hover {
            border-color: #fff;
            color: #fff;
        }
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .status-text {
            color: #aaa;
            font-family: 'Rajdhani', sans-serif;
            text-align: center;
            margin: 15px 0;
            letter-spacing: 1px;
            font-size: 14px;
        }
    </style>
    
    <script>
        // NEW UI LOGIC
        let pendingGameMode = null;
        
        function openArenaSelect(mode) {
            pendingGameMode = mode;
            document.getElementById('arenaSelectorModal').style.display = 'flex';
        }
        
        function closeArenaSelect() {
            document.getElementById('arenaSelectorModal').style.display = 'none';
        }
        
        function openLocker() {
            document.getElementById('lockerModal').style.display = 'flex';
        }
        
        function closeLocker() {
            document.getElementById('lockerModal').style.display = 'none';
        }
        
        function selectMapGUI(el, mapName) {
            // Call original game logic
            if(window.selectMap) window.selectMap(mapName);
            
            // Visual update
            document.querySelectorAll('.map-card').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
        }
        
        function selectSkinGUI(el, skinName) {
            // Call original game logic
            if(window.selectSkin) window.selectSkin(skinName);
            
            // Visual update
            document.querySelectorAll('.skin-card').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
        }
        
        function executeDeploy() {
            closeArenaSelect();
            closeLocker();
            
            console.log("Executing deploy for mode:", pendingGameMode);
            
            if (pendingGameMode === 'ai') {
                document.getElementById('startButton').click();
            } else if (pendingGameMode === 'host_1v1') {
                document.getElementById('hostButton').click();
                showHostStatus();
            } else if (pendingGameMode === 'host_2v2') {
                document.getElementById('host2v2Button').click();
                showHostStatus();
            }
        }
        
        function showJoinMenu() {
            document.getElementById('primaryMenuButtons').style.display = 'none';
            document.getElementById('joinMenuOverlay').style.display = 'flex';
        }
        
        function hideJoinMenu() {
            document.getElementById('joinMenuOverlay').style.display = 'none';
            document.getElementById('primaryMenuButtons').style.display = 'flex';
        }
        
        function proxyJoin() {
            // Copy input value to legacy joinID?
            // The legacy code reads from 'joinRoomId'.
            // My new UI uses ID 'joinRoomId' as well in the visible overlay.
            // Since ID must be unique, I must ensure the legacy one is REMOVED or RENAMED?
            // Wait, the legacy HTML I kept has `legacy-controls`, but the Join Input was inside `multiplayerSetup` -> `joinInfo`.
            // In my new HTML `joinMenuOverlay` HAS `joinRoomId`.
            // The legacy `setupMultiplayerButtons` attaches listener to `connectButton` (legacy).
            // inside that listener: `const roomId = document.getElementById('joinRoomId').value;`
            // So as long as my visible input has id `joinRoomId`, the legacy button click will find it.
            
            document.getElementById('connectButton').click();
        }
        
        function showHostStatus() {
            document.getElementById('primaryMenuButtons').style.display = 'none';
            document.getElementById('hostStatusOverlay').style.display = 'flex';
            
            // Watch for start game button visibility (legacy code shows it when player connects)
            const legacyStartBtn = document.getElementById('startGameButton');
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                        if (legacyStartBtn.style.display !== 'none') {
                             document.getElementById('visibleStartGameBtn').style.display = 'block';
                             document.getElementById('waitingText').style.display = 'none'; // hide waiting text
                        }
                    }
                });
            });
            
            observer.observe(legacyStartBtn, { attributes: true });
        }
        
        function proxyStartGame() {
            document.getElementById('startGameButton').click();
        }
    </script>
"""

for file_path in FILES:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to match the startScreen div and its content
        # We look for <div id="startScreen"> ... </div>
        # But there are nested divs. 
        # A safer way to find the End is to look for the next major block: <div id="musicPlayer"
        
        pattern = r'(<div id="startScreen">)([\s\S]*?)(</div>\s+<!-- MUSIC PLAYER)'
        
        # Check if match exists
        if re.search(pattern, content):
            # Replace
            # We want to replace group 2 (content) but also include our new appended style/script before the music player
            
            def replacement(match):
                return NEW_UI_HTML.strip() + "\n\n    <!-- MUSIC PLAYER"
            
            # We need to construct a regex that captures everything up to music player to be safe about closing div
            # Actually, let's just use the exact start and end Markers from the file read earlier
            # Start: <div id="startScreen">
            # End: </div> followed by <!-- MUSIC PLAYER -->
            
            new_content = re.sub(r'<div id="startScreen">[\s\S]*?</div>\s+<!-- MUSIC PLAYER', 
                                 NEW_UI_HTML.strip() + "\n\n    <!-- MUSIC PLAYER", 
                                 content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Could not find startScreen block in {file_path}")
