print("Script Started!")
from dolphin import event
import sys
import os
import inspect
from pathlib import Path

# 1. Get the script directory (where main.py is)
script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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

    # ✅ Import your own modules now that path is correct
    from environment import MarioEnvironment
except Exception as e:
    print("Error during imports:")
    traceback.print_exc()
    raise Exception("Script aborted")

# 5. Main script logic
env = MarioEnvironment()

while True:
    await event.frameadvance()
    action = env.sample_action()
    done = env.step(action)

    if done:
        env.reset()