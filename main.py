print("Script Started!")
from dolphin import event, memory
import sys
import asyncio
import os
import traceback
import struct
import inspect
from constants import MARIO_POSITION_ADDR, AI_PATH
from pathlib import Path


currentStep = 0
currentState = []
totalStates = []
totalSteps = 120

# 1. Get the script directory (where main.py is)
script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(r"C:\Python312\Lib\site-packages")

# Update PATH for DLLs (critical for torch extensions)
torch_lib_path = r"C:\Python312\Lib\site-packages\torch\lib"
os.environ["PATH"] = torch_lib_path + ";" + os.environ.get("PATH", "")

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
    import socket
    import pickle
except Exception as e:
    print("Error during imports:")
    traceback.print_exc()
    raise Exception("Script aborted")

# 5. Main script logic
controller = Controller()
env = MarioEnvironment(controller)

HOST = '127.0.0.1'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = server.accept()
    print(f"Connected by {addr}")
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)

def send_msg(sock, obj):
    data = pickle.dumps(obj)
    length = struct.pack('!I', len(data))
    sock.sendall(length + data)

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_msg(sock):
    raw_len = recvall(sock, 4)
    if not raw_len:
        return None
    msg_len = struct.unpack('!I', raw_len)[0]
    data = recvall(sock, msg_len)
    if not data:
        return None
    return pickle.loads(data)



async def main_loop():
    episode = 1

    maxReward = 0

    await event.frameadvance()

    state = await env.reset()

    # Main loop
    for _ in range(50):
        await event.frameadvance()

    while True:
        await event.frameadvance()

        state = await env.reset()
        total_reward = 0
        done = False
        stuck_counter = 0

        while not done and stuck_counter < 150:
            await event.frameadvance()
            send_msg(conn, state)

            action = recv_msg(conn)
            next_state, reward, done = await env.step(action)
            
            if total_reward > maxReward:
                maxReward = total_reward
                print(f"New max reward: {maxReward}")
            else:
                stuck_counter += 1

            if stuck_counter >= 150:
                print("Stuck for too long, resetting environment.")
                reward -= 10
                done = True

            send_msg(conn, next_state)
            send_msg(conn, reward)
            send_msg(conn, done)

            total_reward += reward
            state = next_state


        episode += 1
        maxReward = 0
        print(f"Episode {episode} finished with total reward: {total_reward}")

            
await main_loop()