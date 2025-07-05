from dolphin import event, gui, controller, savestate, memory
from constants import SAVE_STATE_FILE
import random

marioLives = 0x80354E93


wii_dic = {
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


reset = True


def read_memory(address):
    return memory.read_u8(address)
    print(f"Read memory at {address}: {value}")

while True:
    await event.frameadvance()
    wii_dic = {
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

    if reset:
        savestate.load_from_file(SAVE_STATE_FILE)
        reset = False
    # draw on screen
    number = random.randint(0, 4)
    # print to console
    if number == 0:
        wii_dic["A"] = True
    elif number == 1:
        wii_dic["Left"] = True
    elif number == 2:
        wii_dic["Right"] = True
    elif number == 3:
        wii_dic['Left'] = True
        wii_dic["A"] = True
    elif number == 4:
        wii_dic["Right"] = True
        wii_dic["A"] = True
    
    controller.set_wiimote_buttons(0, wii_dic)
    if read_memory(marioLives) < 5:
        reset = True
        print("Resetting game due to low lives")


