import json

# This will define all the controls 

CONTROL_FILE = "controls.json"

def loadControls():

    '''Loads the user's saved keybinds'''

    try:

        # Opens the configured JSON file at the start of the game
        with open(CONTROL_FILE, "r") as file:
            return json.load(file)

    # If the JSON file cannot be found, these values will be loaded instead
    except FileNotFoundError:

        print("File not found, default controls used")

        return {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "dash": "Shift_L",
            "shootLeft": "j",
            "shootDown": "k",
            "shootUp": "i",
            "shootRight": "l",
            "interact" : "f",
            "bossKey": "Escape",
            "pause": "p"
            }