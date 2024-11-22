import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from musicManager import playMusic, stopMusic
import json

TRANSPARENT_BACKGROUND = "Images/transparentBlackBackground.png"

class PauseMenu:

    '''Freezes the game and lets the user take a chill pill'''

    def __init__(self, window, canvas, player, gameVariables, startingArea):
        self.window = window
        self.canvas = canvas
        self.player = player
        self.gameVariables = gameVariables
        self.startingArea = startingArea

        # Flag to see if game is paused or not
        self.paused = False

        # This shows whether the game is allowed to be paused
        self.allowPause = True

        # Load the transparent background image
        self.backgroundImage = Image.open(TRANSPARENT_BACKGROUND)
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)

        # Placeholder for the pause overlay items
        self.transparentBackground = None
        self.pauseTextLabel = None
        self.scoreTextLabel = None
        self.buttonWindowRebind = None
        self.buttonWindowMenu = None
        self.buttonWindowSave = None

        # Projectile manager set later to avoid circular dependency
        self.projectileManager = None

        # Enemy manager set later as it does not exist at the start of the game
        self.enemyManager = None

    def togglePause(self, event, player, gameVariables):

        '''If paused, unpaused and vise versa'''

        if not self.allowPause:
            return

        if not self.paused:
            # stopMusic()
            self.showPause()
        else:
            # playMusic("Sounds\\oldBird.wav")
            self.quitPause(player, gameVariables)

    def setAllowPause(self, boolean):

        '''If this is false, the player cannot pause'''

        self.allowPause = boolean

    def showPause(self):

        '''Shows pausse menu'''
        
        self.paused = True

        # Display the transparent background on the canvas
        self.transparentBackground = self.canvas.create_image(0, 0, image=self.backgroundImage, anchor="nw")
        
        # Display "Paused" text in the center of the screen
        self.pauseTextLabel = self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 - 50,
            text="Paused", font=("Arial", 50), fill="white"
        )

        self.scoreTextLabel= self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            text=f"Current score is {self.gameVariables.getScore()}", font=("Arial", 20), fill="white"
        )

        # Add buttons directly to the canvas
        self.rebindButton = tk.Button(
            self.window, text="Rebind Keys", command=self.changeKeys
        )
        self.buttonWindowRebind = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 50,
            window=self.rebindButton
        )

        self.saveButton= tk.Button(
            self.window, text="Save game", command=self.saveGame
        )

        self.buttonWindowSave = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 100,
            window=self.saveButton
        )

        self.mainMenu = tk.Button(
            self.window, text="Return to Main Menu", command=self.returnToMainMenu
        )

        self.buttonWindowMenu = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 150,
            window=self.mainMenu
        )
    

        # Disable movement by unbinding movement keys
        self.startingArea.removeKeyBinds()

    def quitPause(self, player, gameVariables):

        '''Quits pause menu'''

        self.paused = False

        # Remove the transparent background and pause text from the canvas
        if self.transparentBackground:
            self.canvas.delete(self.transparentBackground)
        if self.pauseTextLabel:
            self.canvas.delete(self.pauseTextLabel)
        if self.scoreTextLabel:
            self.canvas.delete(self.scoreTextLabel)
        if self.buttonWindowRebind:
            self.canvas.delete(self.buttonWindowRebind)
        if self.buttonWindowMenu:
            self.canvas.delete(self.buttonWindowMenu)
        if self.buttonWindowSave:
            self.canvas.delete(self.buttonWindowSave)

        # Rebind movement keys, and apply changes
        self.startingArea.setKeyBinds()
        
        if self.projectileManager:
            # Resumes the flying of projectiles
            self.projectileManager.resume()

        if self.enemyManager:
            self.enemyManager.resume()

    def getIsPaused(self):

        '''Getter'''

        return self.paused
    
    def setIsPaused(self, boolean):

        '''Setter'''

        self.paused = boolean
    
    # Set later as both depend on each other, removes circular import
    def setProjectileManager(self, projectileManager):
        
        '''Setter'''

        self.projectileManager = projectileManager
    
    # Has to be defined later as enemy manager isn't set until the player enters through the door
    def setEnemyManager(self, enemyManager):

        '''Setter'''

        self.enemyManager = enemyManager
    
    def changeKeys(self):

        '''Opens key bind menu'''

        self.keyBindWindow = tk.Toplevel(self.window)
        self.keyBindWindow.title("Key Bindings")
        self.keyBindWindow.geometry("1024x1024")

        # Make it so that it cant be resized
        self.keyBindWindow.resizable(False, False)

        # Opens key bind menu
        from keyBindMenu import KeyBindMenu
        KeyBindMenu(self.keyBindWindow, self.gameVariables, False)
    
    def returnToMainMenu(self):

        '''Opens main menu'''

        # Clean up the canvas (remove all elements)
        self.canvas.delete("all")

        # Remove projectile manager to stop updates
        if self.projectileManager:
            self.projectileManager = None

        # Unbind all keys to avoid conflicts
        self.startingArea.removeKeyBinds()

        # Destroy any additional elements specific to the starting area
        self.canvas.pack_forget()

        # Removes all coordinates from the coordinate array
        self.gameVariables.clearCoordinateArray()

        # Allows the player to interact with the NPC again
        self.gameVariables.setAllowDialogue(True)

        # Resets the player's score
        self.player.setDeathCounter(0)
        self.gameVariables.setHighestScore(0)
        self.gameVariables.setScore(0)

        # Recreate the main menu
        from mainMenu import MainMenu
        MainMenu(self.window, self.gameVariables)
    
    def saveGame(self):

        '''Allows user to save thier game'''

        # This will be saved to the save file
        saveDictionary = {
            "deathCounter": self.player.getDeathCounter(),
            "score": self.gameVariables.getScore(),
            "playerHealth": self.player.getHealth(),
            "highestScore": self.gameVariables.getHighestScore()
        }

        # Allows the user to write a file name to a file path. This will have JSON as a default file extension
        filePath = filedialog.asksaveasfilename(
            title="Save your game",
            defaultextension=".json",  
            filetypes=[("JSON files", "*.json")],  
            initialfile="saveFile.json"
        )

        # If the user cancels the dialog, filePath will be empty
        if not filePath:
            return

        try:

            # Write the save data to the specified file
            with open(filePath, "w") as file:
                json.dump(saveDictionary, file, indent=4)

            messagebox.showinfo("Save Successful", f"Game saved to {filePath}")

        except:
            messagebox.showerror("Error", "Could not save file")