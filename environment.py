from dolphin import event, gui, controller, savestate, memory
from controller import Controller
from constants import MARIO_LIVES_ADDR, SAVE_STATE_FILE
import random


class MarioEnvironment:
    def __init__(self):
        self.actions = ["left", "right", "jump", "jump_left", "jump_right", "nothing"]
        self.controller = Controller()

    def reset(self):
        """TODO: Reset the game using savestates"""
        savestate.load_from_file(SAVE_STATE_FILE)

    def step(self, action):
        """TODO: Execute the action in the game"""
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

        self.controller.apply_buttons()

        # Check if Mario is dead
        done = self.check_death()

        return done


    def get_frame(self):
        """TODO: Capture the current frame from the game"""
        pass

    def check_death(self):
        """Check if Mario is dead by reading memory"""
        mario_lives = memory.read_u8(MARIO_LIVES_ADDR)
        return mario_lives < 5

    def sample_action(self):
        """TODO (TEMP): Sample a random action from the action space"""
        return random.choice(self.actions)