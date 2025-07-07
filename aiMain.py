import socket
import pickle
from constants import AI_PATH
import struct
from PIL import Image
import numpy as np
from agent import Agent
import matplotlib.pyplot as plt


HOST = '127.0.0.1'
PORT = 9999

def visualize_state(frame):
    """
    Show a single grayscale frame of shape (210, 210).
    """
    frame = np.array(frame)
    if frame.shape != (210, 210):
        raise ValueError(f"Expected shape (210, 210), got {frame.shape}")
    
    plt.imshow(frame, cmap='gray')
    plt.axis('off')
    plt.title("Single Frame")
    plt.show()

agent = Agent()

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Connected to server at {HOST}:{PORT}")
episode = 0
currentStep = 0

agent.load("C:/Users/nabil/OneDrive/Documents/wii-rl/RLDolphin/model.pth")

while True:
    state = recv_msg(client)

    action = agent.select_action(state)

    send_msg(client, action)

    next_state = recv_msg(client)
    reward = recv_msg(client)
    done = recv_msg(client)

    agent.store_transition(state, action, reward, next_state, done)
    
    agent.train_step()

    currentStep += 1
    if done:
        episode += 1
        print(f"Episode {episode} finished with total reward: {reward}")
        if episode % 5 == 0:
            print("Saving model...")
            agent.save("C:/Users/nabil/OneDrive/Documents/wii-rl/RLDolphin/model.pth")

