import sys , time ,os ,ctypes ,msvcrt
from beyondmem import MemFurqan , enable_vt

try:
    import keyboard  # hotkeys
except ImportError:
    print("Error: The 'keyboard' module is not installed. Please install it using 'pip install keyboard'.")
    sys.exit(1)
import shutil #centered text

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False
    
if not is_admin():
    script = os.path.abspath(__file__)
    params = f'"{script}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)

COLS , ROWS = 135 , 40
def _setup_console():
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            os.system(f"mode con cols={COLS} lines={ROWS}")
            k = ctypes.windll.kernel32
            k.GetStdHandle.restype = ctypes.c_void_p
            k.GetConsoleMode.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
            k.SetConsoleMode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            hc = k.GetStdHandle(-11)
            m = ctypes.c_ulong()
            k.GetConsoleMode(hc, ctypes.byref(m))
            k.SetConsoleMode(hc, m.value | 0x0007)
            k.SetConsoleTitleW("1964  |  Aimbot Engine  |  v11")
            
            hwnd = k.GetConsoleWindow()
            if hwnd:
                u32 = ctypes.windll.user32
                style = u32.GetWindowLongW(hwnd, -16)
                style &= ~0x00010000 # WS_MAXIMIZEBOX
                style &= ~0x00040000 # WS_SIZEBOX
                u32.SetWindowLongW(hwnd, -16, style)
        except:
            pass

_setup_console()

class C:
    R = '\033[91m'  # Red
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    C = '\033[96m'  # Cyan
    X = '\033[0m'   # Reset Color

def clear_console():
    # Clears the console window (works on windows)
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    """
    Calculates the width of the console, subtracts the length of the text,
    and returns a string with perfect spaces on the left to center it!
    """
    # 1. Get the current width of the user's terminal window
    terminal_width = shutil.get_terminal_size().columns
    
    # 2. To get the REAL length of our text, we must remove the hidden color codes
    # Otherwise a color code like \033[92m makes the computer think the word is 5 letters longer!
    import re
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    text_length = len(clean_text)
    
    # 3. Calculate left padding needed
    # Formula: (total width - text width) / 2
    padding = max(0, (terminal_width - text_length) // 2)
    
    # 4. Return the spaces + the original colored text!
    return (" " * padding) + text

def print_ui(mem_attached):
    clear_console()    
    
    # 1. We split the banner so we can center each line individually
    banner_lines = [
        "  _____           _           _      __   ___ ",
        " |  __ \         (_)         | |    / /  / _ \\",
        " | |__) | __ ___  _  ___  ___| |_  / /_ | | | |",
        " |  ___/ '__/ _ \| |/ _ \/ __| __|| '_ \| | | |",
        " | |   | | | (_) | |  __/ (__| |_ | (_) | |_| |",
        " |_|   |_|  \___/| |\___|\___|\__| \___/ \___/ ",
        "                _/ |                          ",
        "               |__/                           "
    ]
    
    # Print Empty lines at the top to push it down towards the middle vertically
    print("\n" * 2) 
    # Center and print the ASCII Art
    for line in banner_lines:
        print(center_text(f"{C.C}{line}{C.X}"))
        
    print(center_text(f"{C.Y}1964 LEARNING PROJECT{C.X}"))
    print(center_text(f"{C.C}=================================================={C.X}"))
    
    if not mem_attached:
        print(center_text(f"{C.R}Waiting for game: {PROCESS}...{C.X}"))
        print(center_text(f"{C.C}=================================================={C.X}"))
        return 
    print(center_text(f"{C.G}Connected to PID: {MemFurqan().the_proc_id}{C.X}"))
    print(center_text(f"{C.C}--------------------------------------------------{C.X}"))
    
    print(center_text(f" {C.Y}[ACTION]{C.X} Inject Aimbot    (Press: {C.Y}F{C.X})"))
    
    print(center_text(f"{C.C}--------------------------------------------------{C.X}"))
    
    for name, data in HACKS.items():
        status = f"{C.G}[ON ]{C.X}" if data["enabled"] else f"{C.R}[OFF]{C.X}"
        key = data['key'].upper()
        # Formatting so the table stays neat
        hack_string = f" {status} {name:<15} (Press: {C.Y}{key}{C.X})"
        print(center_text(hack_string))
        
    print(center_text(f"{C.C}=================================================={C.X}"))
    print(center_text(f"Press {C.R}Q{C.X} to exit."))
    print("\nLogs:")

def toggle_memory_hack(mem, hack_name):
    """
    This function handles turning any AOB memory hack ON or OFF.
    """
    hack = HACKS[hack_name]
    hack["enabled"] = not hack["enabled"]
    
    # Refresh the UI so it shows [ON] immediately
    print_ui(mem_attached=True)
    
    if hack["enabled"]:
        patch = hack["patched_aob"]
        print(f"{C.Y}[*] Scanning for {hack_name}...{C.X}")
        
        # Scan for the original bytes
        found = mem.AoBScan(0x10000, 0x7FFFFFEFFFF, hack["original_aob"])
        if found:
            for addr in found:
                # Need to convert the patch string to bytes before writing
                # For beyondmem, you might have a helper, but if aob strings are space-separated:
                patch_bytes = bytes.fromhex(patch.replace(" ", ""))
                mem._write_raw(addr, patch_bytes)
            print(f"{C.G}[+] Enabled {hack_name} (Patched {len(found)} addresses)!{C.X}")
        else:
            print(f"{C.R}[-] Could not find memory for {hack_name}!{C.X}")
            # Revert UI status if failed
            hack["enabled"] = False 
    else:
        # Turn OFF (Restore original code)
        orig = hack["original_aob"]
        patch = hack["patched_aob"]
        print(f"{C.Y}[*] Restoring {hack_name}...{C.X}")
        
        # We need to scan for the PATCHED bytes to find where we wrote them!
        found = mem.AoBScan(0x10000, 0x7FFFFFEFFFF, patch)
        if found:
            for addr in found:
                orig_bytes = bytes.fromhex(orig.replace(" ", ""))
                mem._write_raw(addr, orig_bytes)
            print(f"{C.Y}[-] Disabled {hack_name}. Restored original memory!{C.X}")

#CONFIGURATION 
PROCESS = "HD-Player"
AIMBOT_AOB =( "FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    "?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? "
    "?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? "
    "?? ?? ?? ?? ?? "
    "00 00 00 00 00 00 00 00 00 00 00 00 A5 43")

HACKS = {
    # You can add as many memory hacks as you want right here!
    "Speed Hack": {
        "key": "s",
        "enabled": False,
        "original_aob": "01 00 00 00 02 2B 07 3D",
        "patched_aob":  "01 00 00 00 02 2B 65 3D"
    },
    "No Recoil": {
        "key": "r",
        "enabled": False,
        "original_aob": "Your AOB HERE",
        "patched_aob":  "Your AOB HERE"
    }
}

TARGET_OFFSET = 0x80   #BODY
WRITE_OFFSET = 0x7C    #HEAD

def inject_aimbot(mem):
    print_ui(mem_attached=True)
    print(f"{C.Y}[*] Scanning for entities...{C.X}")
    
    found = mem.AoBScan(0x10000, 0x7FFFFFEFFFF, AIMBOT_AOB)
    if not found:
         print(f"{C.R}[-] No entities found{C.X}")
         return
               
    count = 0
    for base in found:
        try:
             target_addr = base + WRITE_OFFSET
             source_addr = base + TARGET_OFFSET

             val_bytes = mem.read_bytes(source_addr, 4)
             if val_bytes:
                 if mem._write_raw(target_addr, val_bytes):
                     count += 1   
        except:                         
             continue
             
    if count > 0:
        print(f"{C.G}[+] Applied aimbot to {count} entities{C.X}" )
    else:
        print(f"{C.R}[-] Failed to apply aimbot.{C.X}")

def main():
    enable_vt()
    mem = MemFurqan()

    print_ui(mem_attached=False)

    # Keep trying to attach until the game opens
    while not mem.open_process_by_name(PROCESS):
        time.sleep(1)
        if keyboard.is_pressed('q'):
            sys.exit(0)

    # Once attached, show the main dashboard
    print_ui(mem_attached=True)

    # ### [NEW] Bind the Aimbot function to the 'F' key globally ###
    keyboard.on_press_key('f', lambda _: inject_aimbot(mem), suppress=False)

    # ### [NEW] Bind all the memory hacks dynamically based on the Dictionary! ###
    for name, data in HACKS.items():
        keyboard.on_press_key(data['key'], lambda _, n=name: toggle_memory_hack(mem, n), suppress=False)

    # Now we just need to keep the script running and looking for 'q'
    while True:
        if keyboard.is_pressed('q'):
            print(f"\n{C.R}Exiting... Goodbye!{C.X}")
            time.sleep(1)
            sys.exit(0)
            
        time.sleep(0.1)
        
if __name__ == "__main__":
    main()


          


