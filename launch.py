import subprocess
import time
import pyautogui

DOLPHIN_EXE = r"C:\Users\nabil\OneDrive\Desktop\dolphin0\Dolphin.exe"
ISO_PATH = r"C:\Users\nabil\OneDrive\Desktop\dolphin0\New Super Mario Bros Wii [SMNE01].wbfs"
SCRIPT_PATH = r"C:\Users\nabil\OneDrive\Documents\wii-rl\main.py"

def launch_game():
    # Step 1: Launch Dolphin with the game
    subprocess.Popen([
        DOLPHIN_EXE,
        "--script", SCRIPT_PATH,
        "-e", ISO_PATH,
    ])
    print("Launching Dolphin with NSMBW...")

if __name__ == "__main__":
    launch_game()
    print("Game launched successfully!")