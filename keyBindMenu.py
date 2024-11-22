import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class KeyBindMenu:

    '''Menu that allows the user to change their key binds to a specific key'''

    def __init__(self, window, gameVariables, mainMenuFlag):
        
        self.window = window
        self.gameVariables = gameVariables
        self.controlsFile = "controls.json"
        self.mainMenuFlag = mainMenuFlag

        self.keybinds = self.loadControls()

        self.frame = tk.Frame(self.window, width=1024, height=1024)
        self.frame.pack()

        self.title = tk.Label(self.frame, text="Key Bindings", font=("Arial", 24))
        self.title.pack(pady=20)

        self.keybindLabels = []
        self.createKeybindDisplay()

        if mainMenuFlag:
            self.backButton = tk.Button(self.frame, text="Back to Menu", command=self.backToMainMenu)
            self.backButton.pack(pady=10)
        else:
            self.backButton = tk.Button(self.frame, text="Close", command=self.exitKeyBindMenu)
            self.backButton.pack(pady=10)
    
    def loadControls(self):

        '''Loads controls stored in the controls file.'''
        
        # Opens controls.json file
        try:
            with open(self.controlsFile, "r") as file:
                return json.load(file)
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Keybinds file not found!")
            return {}
    
    def saveControls(self):

        '''If the user inputs new key binds, they are saved to a JSON file'''
        
        with open(self.controlsFile, 'w') as file:
            json.dump(self.keybinds, file, indent=4)
    
    def createKeybindDisplay(self):

        '''Creates the GUI for the key binds.'''
        
        # Will loop through each action and the key mapped to it, for example (up, w)
        for action, key in self.keybinds.items():
            
            frame = tk.Frame(self.frame)
            frame.pack(pady=5, fill="x")

            label = tk.Label(frame, text=action.capitalize(), font=("Arial", 14), width=20, anchor="w")
            label.pack(side="left", padx=10)

            keyLabel = tk.Label(frame, text=key, font=("Arial", 14), width=10, anchor="center", relief="ridge")
            keyLabel.pack(side="left", padx=10)

            # Adds the action and keyLabel to the screen
            self.keybindLabels.append((action, keyLabel))

            button = tk.Button(frame, text="Change", command=lambda a=action: self.changeKey(a))
            button.pack(side="right", padx=10)
    
    def changeKey(self, action):

        '''Allows the user to change a keybind to another valid key'''
        
        # Will show a box prompting the user to enter what keybind they want to put in
        newKeybind = simpledialog.askstring("Change Key", f"Enter new key for '{action}':")

        if not newKeybind:
            return
            
        # Checks if what the user has inputted is valid
        valid = self.keyValidation(newKeybind)
        if valid:

            # In the dictionary we grabbed from the json file, update the key
            self.keybinds[action] = newKeybind
            self.updateKeybindMenu()
            self.saveControls()
        else:
            messagebox.showerror("Invalid Key", f"'{newKeybind}' is not a valid key!")
    
    def keyValidation(self, newKeybind):

        '''Validates user input.'''

        if len(newKeybind) < 0:
            return False
        
        validKeysArray = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Up', 'Down', 'Left', 'Right',
    'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Control-b', 'Escape']
        
        if newKeybind not in validKeysArray:
            return False
        
        # This is to check for already existing keybinds
        for action, key in self.keybinds.items():

            if newKeybind == key:
                return False

        return True


    def updateKeybindMenu(self):

        '''If new keybind added, the menu is updated'''

        # Since a new key has been added, change the displayed key in the menu
        for action, label in self.keybindLabels:
            label.config(text=self.keybinds[action])

    def backToMainMenu(self):

        '''Takes the user back to the main menu'''
        
        self.frame.destroy()

        # Reinitialize the MainMenu
        # Import here so that no circular import is generated
        from mainMenu import MainMenu
        MainMenu(self.window, self.gameVariables)

    def exitKeyBindMenu(self):

        '''Closes the window'''

        self.window.destroy()