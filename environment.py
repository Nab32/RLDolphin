from dolphin import event, gui, controller, savestate, memory
from controller import Controller
from constants import MARIO_LIVES_ADDR, SAVE_STATE_FILE, SKIP_FRAMES, MARIO_POSITION_ADDR, ACTIONS
from PIL import Image
import numpy as np
import random


class MarioEnvironment:
    def __init__(self, controller):
        self.actions = ["left", "right", "jump", "jump_left", "jump_right", "nothing"]
        self.controller = controller
        self.currentState = []
        self.marioPosition = 760
        self.totalReward = 0

    async def reset(self):
        """TODO: Reset the game using savestates"""
        self.currentState = []
        self.marioPosition = 760
        self.totalReward = 0
        savestate.load_from_file(SAVE_STATE_FILE)
        for _ in range(0, 30):
            await event.frameadvance()
        for _ in range(0, SKIP_FRAMES):
            width, height, data = await event.framedrawn()

            img = self.get_frame(width, height, data)
            self.currentState.append(img)

        newState = np.stack(self.currentState, axis=0)
        self.currentState = []
        return newState

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

        # Check if Mario is dead
        reward = self.compute_reward()
        self.totalReward += reward

        done = self.check_death()
        if done:
            self.totalReward -= 10;
            reward -= 10
        
        next_state = np.stack(self.currentState, axis=0)
        self.currentState = []
        
        return next_state, reward, done

    def take_action(self, action_index):
        """Execute the action in the game"""
        self.controller.reset_buttons()

        if action_index == 0:
            self.controller.reset_buttons()
        else:
            for buttons in ACTIONS[action_index]:
                self.controller.set_button(buttons, True)



    def get_frame(self, width, height, data):
        """TODO: Capture the current frame from the game"""

        rgb_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
        image = Image.fromarray(rgb_array, mode='RGB')

        gray_image = image.convert('L').resize((210, 210), Image.BILINEAR)
        frame = np.array(gray_image, dtype=np.float32) / 255.0  # Normalize to [0, 1]
        return frame


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
        return random.randint(0, len(ACTIONS) - 1)