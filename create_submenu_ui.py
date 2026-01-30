
import os
import re

FILES = [
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\fps-game.html",
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\electron\game\fps-game.html"
]

ORIGINAL_HTML_BLOCK = """
    <div id="startScreen">
        <!-- Hidden file input for profile picture -->
        <input type="file" id="profilePictureInput" accept="image/*" style="display: none;">

        <div class="menu-content">
            <div style="margin-bottom: 20px;">
                <input type="text" id="usernameInput" placeholder="SOLDIER NAME" maxlength="12" class="menu-input"
                    style="background: transparent; border: none; border-bottom: 2px solid rgba(255,255,255,0.3); font-size: 18px; padding: 10px 0; width: 100%; color: white; font-family: 'Rajdhani', sans-serif; letter-spacing: 2px;">
            </div>

            <div class="menu-button-group">
                <button id="hostButton" class="menu-button">DEPLOY (1v1 HOST)</button>
                <button id="joinButton" class="menu-button">JOIN SERVER (1v1)</button>
                <button id="host2v2Button" class="menu-button">SQUAD DEPLOY (2v2 HOST)</button>
                <button id="join2v2Button" class="menu-button">JOIN SQUAD (2v2)</button>
                <button id="startButton" class="menu-button">CAMPAIGN (VS AI)</button>
                <button id="keybindsButton" onclick="openKeybindsModal()" class="menu-button">⚙ OPTIONS</button>
            </div>

            <!-- Map Selection -->
            <div class="map-selector">
                <div class="map-selector-label">⚔ SELECT ARENA</div>
                <div class="map-options">
                    <div class="map-option selected" data-map="default" onclick="selectMap('default')">
                        <div class="map-option-name">WAREHOUSE</div>
                        <div class="map-option-desc">Classic Arena</div>
                    </div>
                    <div class="map-option" data-map="map1" onclick="selectMap('map1')">
                        <div class="map-option-name">ARENA</div>
                        <div class="map-option-desc">Unity Export</div>
                    </div>
                </div>
            </div>

            <!-- Skin Selection -->
            <div class="skin-selector">
                <div class="skin-selector-label">👤 SELECT SKIN</div>
                <div class="skin-options">
                    <div class="skin-option selected" data-skin="soldier" onclick="selectSkin('soldier')">
                        <div class="skin-option-icon">🔫</div>
                        <div class="skin-option-name">SOLDIER</div>
                        <div class="skin-option-desc">Combat Ready</div>
                    </div>
                    <div class="skin-option" data-skin="briefcase" onclick="selectSkin('briefcase')">
                        <div class="skin-option-icon">💼</div>
                        <div class="skin-option-name">EXECUTIVE</div>
                        <div class="skin-option-desc">Business Casual</div>
                    </div>
                    <div class="skin-option" data-skin="skeleton" onclick="selectSkin('skeleton')">
                        <div class="skin-option-icon">💀</div>
                        <div class="skin-option-name">SKELETON</div>
                        <div class="skin-option-desc">Spooky Bones</div>
                    </div>
                    <div class="skin-option" data-skin="zombie" onclick="selectSkin('zombie')">
                        <div class="skin-option-icon">🧟</div>
                        <div class="skin-option-name">ZOMBIE</div>
                        <div class="skin-option-desc">Brain Eater</div>
                    </div>
                </div>
                <button id="emoteButton" class="emote-button" onclick="playEmote()">
                    💃 DANCE (E)
                </button>
            </div>

            <div id="multiplayerSetup"
                style="display: none; margin-top: 20px; border-left: 2px solid #ffa500; padding-left: 20px;">
                <div id="hostInfo" style="display: none;">
                    <div class="menu-label"
                        style="color: #ffa500; font-family: 'Rajdhani', sans-serif; font-size: 12px;">SERVER ID</div>
                    <input type="text" id="roomId" readonly class="menu-input menu-input-readonly"
                        style="background: transparent; border: none; font-size: 14px; letter-spacing: 1.5px; color: white; font-family: 'Rajdhani', sans-serif; padding: 5px 0; word-break: break-all;">
                    <button id="startGameButton" class="menu-button" style="color: #ffa500; margin-top: 10px;">LAUNCH
                        MISSION</button>
                </div>
                <div id="joinInfo" style="display: none;">
                    <div class="menu-label"
                        style="color: #ffa500; font-family: 'Rajdhani', sans-serif; font-size: 12px;">ENTER SERVER ID
                    </div>
                    <input type="text" id="joinRoomId" placeholder="SERVER ID" class="menu-input"
                        style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.3); font-size: 14px; letter-spacing: 1.5px; color: white; margin-bottom: 10px; font-family: 'Rajdhani', sans-serif;">
                    <div class="menu-button-group">
                        <button id="connectButton" class="menu-button">CONNECT</button>
                        <button id="cancelButton" class="menu-button" style="color: #ff3b30;">ABORT</button>
                    </div>
                </div>
            </div>

            <!-- Separate Status Display -->
            <div id="waitingText"
                style="display: none; color: rgba(255, 255, 255, 0.6); font-size: 12px; margin-top: 20px; font-family: 'Rajdhani', sans-serif; border-top: 1px solid rgba(255, 165, 0, 0.3); padding-top: 15px;">
                WAITING FOR OPPONENT...</div>

            <!-- Hidden controls and crosshair for cleaner look, can be moved to options later if needed -->
            <div class="controls" style="display: none;">
                <strong>CONTROLS:</strong><br>
                ZQSD - Move | Mouse - Look | Left Click - Shoot | R - Reload<br>
                1, 2, 3 - Switch Weapons | F - Toggle DOF | ESC - Pause<br>
            </div>

        </div>
    </div>
"""

NEW_HTML_BLOCK = """
    <div id="startScreen">
        
        <!-- HIDDEN LOGIC BUTTONS (Proxies for existing game logic) -->
        <div style="display: none;">
            <!-- These maintain original IDs so game logic works -->
            <button id="hostButton">LOGIC_HOST</button>
            <button id="joinButton">LOGIC_JOIN</button>
            <button id="host2v2Button">LOGIC_HOST2V2</button>
            <button id="join2v2Button">LOGIC_JOIN2V2</button>
            <button id="startButton">LOGIC_START_AI</button>
            
            <input type="file" id="profilePictureInput" accept="image/*">
        </div>

        <div class="menu-content">
            <div style="margin-bottom: 20px;">
                <input type="text" id="usernameInput" placeholder="SOLDIER NAME" maxlength="12" class="menu-input"
                    style="background: transparent; border: none; border-bottom: 2px solid rgba(255,255,255,0.3); font-size: 18px; padding: 10px 0; width: 100%; color: white; font-family: 'Rajdhani', sans-serif; letter-spacing: 2px;">
            </div>

            <!-- VISIBLE UI BUTTONS -->
            <div class="menu-button-group" id="mainMenuButtons">
                <button id="btnUI_Host" class="menu-button" onclick="openArenaSelect('host')">DEPLOY (1v1 HOST)</button>
                <button id="btnUI_Join" class="menu-button" onclick="triggerLegacyClick('joinButton')">JOIN SERVER (1v1)</button>
                <button id="btnUI_Host2" class="menu-button" onclick="openArenaSelect('host2')">SQUAD DEPLOY (2v2 HOST)</button>
                <button id="btnUI_Join2" class="menu-button" onclick="triggerLegacyClick('join2v2Button')">JOIN SQUAD (2v2)</button>
                <button id="btnUI_AI" class="menu-button" onclick="openArenaSelect('ai')">CAMPAIGN (VS AI)</button>
                <button id="btnUI_Locker" class="menu-button locker-btn" onclick="openLockerModal()" style="border-left: 3px solid #00ccff; margin-top: 10px;">🎒 OPERATOR LOCKER</button>
                <button id="keybindsButton" onclick="openKeybindsModal()" class="menu-button">⚙ OPTIONS</button>
            </div>

            <div id="multiplayerSetup"
                style="display: none; margin-top: 20px; border-left: 2px solid #ffa500; padding-left: 20px;">
                <div id="hostInfo" style="display: none;">
                    <div class="menu-label"
                        style="color: #ffa500; font-family: 'Rajdhani', sans-serif; font-size: 12px;">SERVER ID</div>
                    <input type="text" id="roomId" readonly class="menu-input menu-input-readonly"
                        style="background: transparent; border: none; font-size: 14px; letter-spacing: 1.5px; color: white; font-family: 'Rajdhani', sans-serif; padding: 5px 0; word-break: break-all;">
                    <button id="startGameButton" class="menu-button" style="color: #ffa500; margin-top: 10px;">LAUNCH
                        MISSION</button>
                </div>
                <div id="joinInfo" style="display: none;">
                    <div class="menu-label"
                        style="color: #ffa500; font-family: 'Rajdhani', sans-serif; font-size: 12px;">ENTER SERVER ID
                    </div>
                    <input type="text" id="joinRoomId" placeholder="SERVER ID" class="menu-input"
                        style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.3); font-size: 14px; letter-spacing: 1.5px; color: white; margin-bottom: 10px; font-family: 'Rajdhani', sans-serif;">
                    <div class="menu-button-group">
                        <button id="connectButton" class="menu-button">CONNECT</button>
                        <button id="cancelButton" class="menu-button" style="color: #ff3b30;" onclick="showMainMenu()">ABORT</button>
                    </div>
                </div>
            </div>

            <!-- Separate Status Display -->
            <div id="waitingText"
                style="display: none; color: rgba(255, 255, 255, 0.6); font-size: 12px; margin-top: 20px; font-family: 'Rajdhani', sans-serif; border-top: 1px solid rgba(255, 165, 0, 0.3); padding-top: 15px;">
                WAITING FOR OPPONENT...</div>

            <div class="controls" style="display: none;">
                <strong>CONTROLS:</strong><br>
                ZQSD - Move | Mouse - Look | Left Click - Shoot | R - Reload<br>
                1, 2, 3 - Switch Weapons | F - Toggle DOF | ESC - Pause<br>
            </div>
            
        </div>

        <!-- NEW: ARENA SELECT MODAL (Hidden Submenu) -->
        <div id="arenaSelectModal" class="submenu-modal" style="display: none;">
             <div class="submenu-content">
                <div class="submenu-header">
                    <button class="close-submenu" onclick="closeSubmenus()">×</button>
                    <span>SELECT ARENA</span>
                </div>
                
                <div class="map-selector" style="margin: 0; padding: 0; border: none; background: transparent;">
                    <!-- Reusing existing map options structure/classes so CSS works -->
                    <div class="map-options" style="justify-content: center; gap: 15px;">
                        <div class="map-option selected" data-map="default" onclick="selectMapAndLaunch('default')">
                            <div class="map-option-name" style="font-size: 14px;">WAREHOUSE</div>
                            <div class="map-option-desc">Classic Arena</div>
                        </div>
                        <div class="map-option" data-map="map1" onclick="selectMapAndLaunch('map1')">
                            <div class="map-option-name" style="font-size: 14px;">ARENA</div>
                            <div class="map-option-desc">Unity Export</div>
                        </div>
                    </div>
                </div>
             </div>
        </div>

        <!-- NEW: LOCKER MODAL (Hidden Submenu) -->
        <div id="lockerModal" class="submenu-modal" style="display: none;">
             <div class="submenu-content" style="width: 400px;">
                <div class="submenu-header">
                     <button class="close-submenu" onclick="closeSubmenus()">×</button>
                    <span style="color: #00ccff;">OPERATOR LOCKER</span>
                </div>
                
                <div class="skin-selector" style="margin: 0; padding: 0; border: none; background: transparent;">
                    <div class="skin-options" style="justify-content: center; gap: 15px;">
                        <div class="skin-option selected" data-skin="soldier" onclick="selectSkin('soldier')">
                            <div class="skin-option-icon">🔫</div>
                            <div class="skin-option-name">SOLDIER</div>
                        </div>
                        <div class="skin-option" data-skin="briefcase" onclick="selectSkin('briefcase')">
                            <div class="skin-option-icon">💼</div>
                            <div class="skin-option-name">EXECUTIVE</div>
                        </div>
                        <div class="skin-option" data-skin="skeleton" onclick="selectSkin('skeleton')">
                            <div class="skin-option-icon">💀</div>
                            <div class="skin-option-name">SKELETON</div>
                        </div>
                        <div class="skin-option" data-skin="zombie" onclick="selectSkin('zombie')">
                            <div class="skin-option-icon">🧟</div>
                            <div class="skin-option-name">ZOMBIE</div>
                        </div>
                    </div>
                     <button id="emoteButton" class="emote-button" onclick="playEmote()" style="margin-top: 15px; width: 100%;">
                        💃 DANCE (E)
                    </button>
                    <button class="menu-button" onclick="closeSubmenus()" style="margin-top: 10px; border-color: #00ccff; text-align: center;">CONFIRM LOADOUT</button>
                </div>
             </div>
        </div>
    </div>
    
    <!-- INJECTED STYLES FOR SUBMENUS & POSITIONING -->
    <style>
        /* 1. Slide menu closer to center */
        #startScreen {
            padding-left: 450px !important; /* Visual shift */
        }
        
        /* 2. Submenu Modal Styling (Floating Panels) */
        .submenu-modal {
            position: absolute; /* relative to #startScreen (fixed) */
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7); /* Dim background */
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            backdrop-filter: blur(5px);
            padding-left: 450px; /* Match menu offset so it centers nicely relative to view */
        }
        
        .submenu-content {
            background: rgba(15, 20, 25, 0.95);
            border: 1px solid rgba(255,255,255,0.1);
            border-top: 4px solid #ffa500;
            padding: 20px;
            border-radius: 4px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            transform: skewX(-2deg);
            min-width: 300px;
            animation: popIn 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        @keyframes popIn { from { transform: skewX(-2deg) scale(0.9); opacity: 0; } to { transform: skewX(-2deg) scale(1); opacity: 1; } }
        
        .submenu-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
        }
        
        .submenu-header span {
            font-family: 'Rajdhani', sans-serif;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #ffa500;
        }
        
        .close-submenu {
            background: none;
            border: none;
            color: #888;
            font-size: 24px;
            cursor: pointer;
            line-height: 1;
        }
        .close-submenu:hover { color: #fff; }
        
        /* Additional override for Map Option to look bigger in modal */
        .submenu-content .map-option {
            width: 120px;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    </style>
    
    <script>
        // UI STATE LOGIC
        let pendingMode = null; // 'ai', 'host', 'host2'
        
        function openArenaSelect(mode) {
            pendingMode = mode;
            document.getElementById('arenaSelectModal').style.display = 'flex';
        }
        
        function openLockerModal() {
            document.getElementById('lockerModal').style.display = 'flex';
        }
        
        function closeSubmenus() {
            document.getElementById('arenaSelectModal').style.display = 'none';
            document.getElementById('lockerModal').style.display = 'none';
        }
        
        function triggerLegacyClick(id) {
            document.getElementById(id).click();
            // If it's a join button, existing logic handles showing multiplayerSetup
            // But we need to make sure our UI doesn't conflict
            if(id.includes('join')) {
                document.getElementById('mainMenuButtons').style.display = 'none';
                // Wait for existing logic to show #multiplayerSetup -> #joinInfo
                setTimeout(() => {
                   document.getElementById('multiplayerSetup').style.display = 'block';
                   document.getElementById('joinInfo').style.display = 'block';
                }, 50);
            }
        }
        
        function showMainMenu() {
             document.getElementById('multiplayerSetup').style.display = 'none';
             document.getElementById('mainMenuButtons').style.display = 'flex';
        }
        
        function selectMapAndLaunch(mapName) {
            // 1. Select the map (updates global var)
            if(window.selectMap) window.selectMap(mapName);
            
            // 2. Visual update
             document.querySelectorAll('.map-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            const selectedOption = document.querySelector(`.map-option[data-map="${mapName}"]`);
            if (selectedOption) selectedOption.classList.add('selected');
            
            // 3. Launch based on pending mode
            closeSubmenus();
            console.log("Launching mode:", pendingMode);
            
            if (pendingMode === 'ai') {
                document.getElementById('startButton').click();
            } else if (pendingMode === 'host') {
                document.getElementById('hostButton').click();
                // Host button logic shows Host Info, we need to hide main buttons
                document.getElementById('mainMenuButtons').style.display = 'none';
            } else if (pendingMode === 'host2') {
                document.getElementById('host2v2Button').click();
                document.getElementById('mainMenuButtons').style.display = 'none';
            }
        }
    </script>
"""

# Helper to normalize whitespace for fuzzy matching
def normalize(s):
    return re.sub(r'\s+', ' ', s).strip()

def apply_update():
    # Detect the block in the file
    # The existing block starts with <div id="startScreen"> and ends with </div>...<!-- MUSIC PLAYER
    
    # We will use a simpler regex to catch the block.
    pattern = r'(<div id="startScreen">)([\s\S]*?)(</div>\s+<!-- MUSIC PLAYER)'
    
    for file_path in FILES:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if re.search(pattern, content):
            new_content = re.sub(pattern, NEW_HTML_BLOCK.strip() + "\n\n    <!-- MUSIC PLAYER", content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Could not find startScreen block in {file_path}")

if __name__ == "__main__":
    apply_update()
