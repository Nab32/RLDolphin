print("Script Started!")
from dolphin import event
import sys
import os
import traceback
import inspect
import time
from pathlib import Path


currentFrame = 0
skipFrame = 3
currentState = []
totalStates = []
totalSteps = 120

# 1. Get the script directory (where main.py is)
script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(r"C:\Python312\Lib\site-packages")

# 2. Add current directory to Python path so we can import our own modules
sys.path.append(script_directory)

# 3. Load shared Python libraries (for numpy, PIL, etc.)
shared_site_path = Path(script_directory) / "shared_site.txt"
if shared_site_path.exists() and shared_site_path.is_file():
    with open(shared_site_path, 'r', encoding='utf-8') as file:
        site_path = file.read().strip()
        sys.path.append(site_path)

# 4. Safe imports
try:
    import random
    from environment import MarioEnvironment
    from controller import Controller
except Exception as e:
    print("Error during imports:")
    traceback.print_exc()
    raise Exception("Script aborted")

# 5. Main script logic
controller = Controller()
env = MarioEnvironment(controller)

# Launch the game and wait for it to be ready
await event.frameadvance()
env.reset()

frame_count = 0
MAX_FRAMES = 5  # Limit to 5 frames

def show_limited_frames(width: int, height: int, data: bytes):
    # Convert raw bytes to NumPy array
    rgb_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))

    img = Image.fromarray(rgb_array, mode='RGB').convert('L')

    currentState.append(img)

#event.on_framedrawn(show_limited_frames)

# Main loop
for _ in range(50):
    await event.frameadvance()

while True:
    await event.frameadvance()
    
    action = env.sample_action()
    done = await env.step(action)
    
    currentFrame+=1  # Reset step after each action
    print(currentFrame)
    if currentFrame >= totalSteps:
        print("Reached maximum steps, resetting environment...")
        env.random_state()
        env.reset()
        currentFrame = 0
    if done:
        # Take a random state from the total states
        env.random_state()

        print("Mario is dead, resetting environment...")
        env.reset()
    
    