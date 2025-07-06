from dolphin import event, gui, controller, savestate, memory
from controller import Controller
from constants import MARIO_LIVES_ADDR, SAVE_STATE_FILE, SKIP_FRAMES, MARIO_POSITION_ADDR
from PIL import Image
import numpy as np
import random


class MarioEnvironment:
    def __init__(self, controller):
        self.actions = ["left", "right", "jump", "jump_left", "jump_right", "nothing"]
        self.controller = controller
        self.currentState = []
        self.totalStates = []
        self.marioPosition = 760
        self.totalReward = 0

    def reset(self):
        """TODO: Reset the game using savestates"""
        self.totalStates = []
        self.currentState = []
        self.marioPosition = 760
        self.totalReward = 0
        savestate.load_from_file(SAVE_STATE_FILE)

    async def step(self, action):
        """TODO: Execute the action in the game"""
        # Take the action
        self.take_action(action)

        for _ in range(0, SKIP_FRAMES):
            # Advance the game frame

            self.controller.apply_buttons()

            width, height, data = await event.framedrawn()

            
            img = self.get_frame(width, height, data)
            self.currentState.append(img)

        self.totalStates.append([self.currentState[:], action])
        self.currentState = []
        # Check if Mario is dead
        reward = self.compute_reward()
        self.totalReward += reward

        done = self.check_death()
        if done:
            self.totalReward -= 10;
        
        return done


    def random_state(self):
        randomState = random.choice(self.totalStates)
        for img in randomState[0]:
            img.show()

    def take_action(self, action):
        """Execute the action in the game"""
        self.controller.reset_buttons()

        if action == "left":
            self.controller.set_button("Left", True)
        elif action == "right":
            self.controller.set_button("Right", True)
        elif action == "jump":
            self.controller.set_button("A", True)
        elif action == "jump_left":
            self.controller.set_button("Left", True)
            self.controller.set_button("A", True)
        elif action == "jump_right":
            self.controller.set_button("Right", True)
            self.controller.set_button("A", True)
        elif action == "nothing":
            self.controller.reset_buttons()


    def get_frame(self, width, height, data):
        """TODO: Capture the current frame from the game"""

        rgb_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
        image = Image.fromarray(rgb_array, mode='RGB')

        # Convert to grayscale
        gray_image = image.convert('L')

        # Resize to desired input shape for the model
        resized_image = gray_image.resize((224, 224), Image.BILINEAR)
        
        return resized_image


    def compute_reward(self):
        newMarioPosition = memory.read_f32(MARIO_POSITION_ADDR)
        reward = (newMarioPosition - self.marioPosition) * 0.1
        self.marioPosition = newMarioPosition
        return reward


    def check_death(self):
        """Check if Mario is dead by reading memory"""
        mario_lives = memory.read_u8(MARIO_LIVES_ADDR)
        return mario_lives < 5

    def sample_action(self):
        """TODO (TEMP): Sample a random action from the action space"""
        return random.choice(self.actions)