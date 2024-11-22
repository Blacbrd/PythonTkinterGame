import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

from musicManager import playMusic
from startingArea import StartingArea
from keyBindMenu import KeyBindMenu
from cheatCodeMenu import CheatCodeMenu
from leaderboardMenu import LeaderboardMenu
from instructionMenu import InstructionMenu
import json

class MainMenu:

    '''This is the first menu the user will see, and also where they'll have the most options to choose from'''

    def __init__(self, window, gameVariables):
        self.window = window
        self.gameVariables = gameVariables

        # This creates a window of size 1024x1024 and centers it on the user's screen
        width, height = 1024, 1024
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        offsetx = (screenWidth - width) // 2
        offsety = (screenHeight - height) // 2
        window.geometry(f"{width}x{height}+{offsetx}+{offsety-32}")

        # Load images for buttons and background
        self.backgroundImage = Image.open("Images/deerBackgroundMenu.png")
        self.backgroundImage = self.backgroundImage.resize((1024, 1024))
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)
        self.newGameImage = ImageTk.PhotoImage(Image.open("Images/newGameButton.png"))
        self.howToPlayImage = ImageTk.PhotoImage(Image.open("Images/instructionMenuButton.png"))
        self.rebindKeysImage = ImageTk.PhotoImage(Image.open("Images/rebindKeysButton.png"))
        self.cheatCodeImage = ImageTk.PhotoImage(Image.open("Images/cheatCodesButton.png"))
        self.loadGameImage = ImageTk.PhotoImage(Image.open("Images/loadGameButton.png"))
        self.leaderboardImage = ImageTk.PhotoImage(Image.open("Images/leaderBoardButton.png"))
        self.exitImage = ImageTk.PhotoImage(Image.open("Images/exitGameButton.png"))

        # Create a canvas for the background
        self.canvas = tk.Canvas(self.window, width=1024, height=1024)
        self.canvas.pack(fill="both", expand=True)

        # Add background image to the canvas
        self.canvas.create_image(0, 0, image=self.backgroundImage, anchor="nw")
        
        # Display "No Eye Deer" with a black backdrop at (512, 200)
        textX = 512
        textY = 100

        # bbox wil return the (x1, y1, x2, y2), top left to bottom right of the text
        textWidth = self.canvas.bbox(self.canvas.create_text(textX, textY, text="No Eye Deer", font=("Arial", 50)))

        # Width of the text bounding box (x2 - x1)
        textWidth = textWidth[2] - textWidth[0]  

        # The rectangle will be slightly larger than the text to provide padding
        padding = 20

        # Create black backdrop rectangle
        self.canvas.create_rectangle(
            textX - textWidth // 2 - padding, textY - 25 - padding,
            textX + textWidth // 2 + padding, textY + 25 + padding,
            fill="black", outline="black"
        )

        # Create the text on top of the rectangle
        self.mainMenuTextLabel = self.canvas.create_text(
            textX, textY,
            text="No Eye Deer", font=("Arial", 50), fill="white"
        )

        # Add buttons with images
        self.newGameButton = tk.Button(
            self.window, image=self.newGameImage, command=self.newGame, borderwidth=0
        )
        self.newGameButton.place(relx=0.5, rely=0.2, anchor="center")

        self.howToPlayButton = tk.Button(
            self.window, image=self.howToPlayImage, command=self.displayInstructions, borderwidth=0
        )
        self.howToPlayButton.place(relx=0.5, rely=0.3, anchor="center")

        self.rebindKeysButton = tk.Button(
            self.window, image=self.rebindKeysImage, command=self.changeKeys, borderwidth=0
        )
        self.rebindKeysButton.place(relx=0.5, rely=0.4, anchor="center")

        self.cheatCodeButton = tk.Button(
            self.window, image=self.cheatCodeImage, command=self.cheatCodes, borderwidth=0
        )
        self.cheatCodeButton.place(relx=0.5, rely=0.5, anchor="center")

        self.loadGameButton = tk.Button(
            self.window, image=self.loadGameImage, command=self.loadGame, borderwidth=0
        )
        self.loadGameButton.place(relx=0.5, rely=0.6, anchor="center")

        self.leaderboardButton = tk.Button(
            self.window, image=self.leaderboardImage, command=self.leaderboard, borderwidth=0
        )
        self.leaderboardButton.place(relx=0.5, rely=0.7, anchor="center")

        self.exitButton = tk.Button(
            self.window, image=self.exitImage, command=self.exitGame, borderwidth=0
        )
        self.exitButton.place(relx=0.5, rely=0.8, anchor="center")

    # Opens first game screen
    def newGame(self):

        '''Opens the first playable screen'''

        # Remove the main menu
        self.quitMenu()

        # Moves onto the next screen
        StartingArea(self.window, self.gameVariables, None)

    def changeKeys(self):
        
        '''Opens key bind menu'''

        # Remove main menu
        self.quitMenu()

        # Opens key bind menu, starting from main menu so menu flag is true
        KeyBindMenu(self.window, self.gameVariables, True)

    def loadGame(self):

        '''Loads game from a JSON file'''

        # Opens controls.json file
        try:
            filePath = filedialog.askopenfilename(title="Choose save file", filetypes=[("JSON files", "*.json")])
            with open(filePath, "r") as file:
                self.savedGame = json.load(file)
        except:
            messagebox.showerror("Error", "Save file not found!")
            return

        valid = self.validateSaveFile()

        if not valid:
            messagebox.showerror("Error", "Invalid save file, most likely due to incorrect key value pairs.")
            return

        # Remove main menu
        self.quitMenu()

        StartingArea(self.window, self.gameVariables, self.savedGame)

    def cheatCodes(self):

        '''Opens cheat code menu'''

        cheatCodeMenu = CheatCodeMenu(self.window, self.gameVariables)
        cheatCodeMenu.showCheatCodeMenu()

    # Quits game
    def exitGame(self):

        '''Closes window'''

        self.window.quit()

    def validateSaveFile(self):

        '''Validates if the file selected by the user can be used as a save file'''

        # Validate keys of the dictionary by checking if they allign with this array
        expectedKeys = ["deathCounter", "score", "playerHealth", "highestScore"]

        for key, value in self.savedGame.items():

            if key not in expectedKeys:
                return False
            
            if key in expectedKeys:
                expectedKeys.remove(key)

        # If all keys haven't been covered, return False
        if len(expectedKeys) != 0:
            return False

        return True

    def leaderboard(self):

        '''Opens the leaderboard menu'''

        # Remove current frame
        self.quitMenu()

        leaderboardMenu = LeaderboardMenu(self.window, self.gameVariables, True)
        leaderboardMenu.createLeaderboardDisplay()
    
    def quitMenu(self):

        '''Deletes all the buttons and canvas'''

        self.canvas.destroy()

        self.newGameButton.destroy()
        self.howToPlayButton.destroy()
        self.rebindKeysButton.destroy()
        self.cheatCodeButton.destroy()
        self.loadGameButton.destroy()
        self.leaderboardButton.destroy()
        self.exitButton.destroy()
        self.canvas.destroy()

    def displayInstructions(self):

        '''Opens instruction menu'''
        
        # Remove current frame
        self.quitMenu()

        InstructionMenu(self.window, self.gameVariables)