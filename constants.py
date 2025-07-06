MARIO_LIVES_ADDR = 0x80354E93


SAVE_STATE_FILE = r"C:\Users\nabil\OneDrive\Documents\wii-rl\RLDolphin\savestates\savestate1.sav"

SKIP_FRAMES = 4

MARIO_POSITION_ADDR = 0x815E4260  # Example address, replace with actual address for Mario's position

ACTIONS = [
    [],                     # 0: Nothing
    ["A"],                  # 1: Jump
    ["Left"],               # 2: Move left
    ["Right"],              # 3: Move right
    ["A", "Left"],          # 4: Jump left
    ["A", "Right"],         # 5: Jump right
    ["Left", "B"],          # 6: Move left faster
    ["Right", "B"],         # 7: Move right faster
]