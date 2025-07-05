from dolphin import controller


class Controller:
    def __init__(self):
        self.wiimote_buttons = {
            "A": False,
            "B": False,
            "One": False,
            "Two": False,
            "Plus": False,
            "Minus": False,
            "Home": False,
            "Up": False,
            "Down": False,
            "Left": False,
            "Right": False
        }


    def reset_buttons(self):
        """Reset all buttons to False."""
        for button in self.wiimote_buttons:
            self.wiimote_buttons[button] = False

    def set_button(self, button, state):
        """Set the state of a specific button."""
        if button in self.wiimote_buttons:
            self.wiimote_buttons[button] = state
        else:
            raise ValueError(f"Button {button} not recognized.")
    
    def apply_buttons(self):
        """Apply the current button states to the Wiimote."""
        controller.set_wiimote_buttons(0, self.wiimote_buttons)