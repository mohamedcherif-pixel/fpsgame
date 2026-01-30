
import os
import re

FILES = [
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\fps-game.html",
    r"c:\Users\cheri\OneDrive\Desktop\fpsgame\electron\game\fps-game.html"
]

FRAGMENT_FILE = r"c:\Users\cheri\OneDrive\Desktop\fpsgame\startScreen.fragment"

def revert_ui():
    # 1. Read the FRAGMENT
    if not os.path.exists(FRAGMENT_FILE):
        print("Fragment file not found!")
        return

    with open(FRAGMENT_FILE, 'r', encoding='utf-8') as f:
        fragment_content = f.read()

    # Extract the pure startScreen block from fragment
    # We look for <div id="startScreen"> ... </div> (and spacer) before <!-- MUSIC PLAYER
    # Note: The fragment contains the whole relevant section.
    
    # Let's match carefully from the fragment
    fragment_match = re.search(r'(<div id="startScreen">[\s\S]*?)(<!-- MUSIC PLAYER)', fragment_content)
    if not fragment_match:
        print("Could not parse startScreen block from fragment file.")
        # Fallback: maybe the fragment ends differently?
        # The fragment read previously showed it ended with <div class="mp-artwork-section">
        # So <!-- MUSIC PLAYER --> is definitely in there.
        print("Debug: Fragment content length:", len(fragment_content))
        return

    original_html_block = fragment_match.group(1)
    print(f"Extracted original block. Length: {len(original_html_block)}")

    # 2. Apply to files
    for file_path in FILES:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find the *modified* block
        # It starts with <div id="startScreen">
        # It ends with <!-- MUSIC PLAYER
        # This will capture the whole new UI + styles + scripts
        
        pattern = r'(<div id="startScreen">[\s\S]*?)(<!-- MUSIC PLAYER)'
        
        if re.search(pattern, content):
            # Replace group 1 with original_html_block
            new_content = re.sub(pattern, lambda m: original_html_block + m.group(2), content, count=1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Reverted {file_path}")
        else:
            print(f"Could not find modified block in {file_path}")

if __name__ == "__main__":
    revert_ui()
