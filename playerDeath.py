import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
from musicManager import playMusic, stopMusic
import json

TRANSPARENT_BACKGROUND = "Images/transparentBlackBackground.png"

class PlayerDeath:

    '''Player death menu'''

    def __init__(self, window, canvas, player, gameVariables, startingArea, pauseMenu, projectileManager):
        self.window = window
        self.canvas = canvas
        self.player = player
        self.gameVariables = gameVariables
        self.startingArea = startingArea
        self.pauseMenu = pauseMenu
        self.projectileManager = projectileManager

        # Initialised later
        self.enemyManager = None

        # Flag to see if the player is dead or not
        self.show = False 

        # Load the transparent background image
        self.backgroundImage = Image.open(TRANSPARENT_BACKGROUND)
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)

        # Placeholder for the death overlay items
        self.transparentBackground = None
        self.deathTextLabel = None
        self.highScoreLabel = None

    def setEnemyManager(self, enemyManager):
        
        '''Setter'''

        self.enemyManager = enemyManager

    def showDeath(self):
        
        '''Shows death screen'''

        self.show = True

        # Makes it so that if the player is paused, it quits the pause menu, and it also doesn't allow the player to pause
        self.pauseMenu.setAllowPause(False)
        self.projectileManager.setStop(True)
        self.enemyManager.setStop(True)
        self.pauseMenu.quitPause(self.player, self.gameVariables)

        # Display the transparent background on the canvas
        self.transparentBackground = self.canvas.create_image(0, 0, image=self.backgroundImage, anchor="nw")
        
        # Display "You died!" text in the center of the screen
        self.deathTextLabel = self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            text="You died!", font=("Arial", 50), fill="white"
        )

        self.scoreTextLabel = self.canvas.create_text(
            self.canvas.winfo_width() / 2, (self.canvas.winfo_height() / 2) + 50,
            text=f"Your score is {self.gameVariables.getScore()}!", font=("Arial", 25), fill="white"
        )

        # Checks if score is bigger than highest score
        if self.gameVariables.getScore() > self.gameVariables.getHighestScore():
            self.gameVariables.setHighestScore(self.gameVariables.getScore())

            self.highScoreLabel = self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 300,
                text="(That's a new high score!!)", font=("Arial", 25), fill="white"
            )

        # Add buttons directly to the canvas
        self.tryAgainButton = tk.Button(
            self.window, text="Try Again!", command=self.tryAgain
        )
        self.tryAgainWindow = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 100,
            window=self.tryAgainButton
        )

        self.saveGameButton = tk.Button(
            self.window, text="Save Game", command=self.saveGame
        )
        self.saveGameWindow = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 150,
            window=self.saveGameButton
        )

        self.leaderBoardButton = tk.Button(
            self.window, text="Leader Board", command=self.showLeaderBoard
        )
        self.buttonWindowLeader = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 200,
            window=self.leaderBoardButton
        )

        self.mainMenu = tk.Button(
            self.window, text="Return to Main Menu", command=self.returnToMainMenu
        )
        self.buttonWindowMenu = self.canvas.create_window(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 250,
            window=self.mainMenu
        )

        # Disable movement by unbinding movement keys
        self.startingArea.removeKeyBinds()

        playerName = self.getPlayerName()

        if playerName != None:
            self.addToLeaderBoard(playerName)

    def quitDeathScreen(self):

        '''Quits death screen'''

        self.show = False

        # Remove the transparent background and pause text from the canvas
        if self.transparentBackground:
            self.canvas.delete(self.transparentBackground)
        if self.deathTextLabel:
            self.canvas.delete(self.deathTextLabel)
        if self.scoreTextLabel:
            self.canvas.delete(self.scoreTextLabel)
        if self.tryAgainWindow:
            self.canvas.delete(self.tryAgainWindow)
        if self.buttonWindowMenu:
            self.canvas.delete(self.buttonWindowMenu)
        if self.highScoreLabel:
            self.canvas.delete(self.highScoreLabel)
        if self.saveGameWindow:
            self.canvas.delete(self.saveGameWindow)
        if self.buttonWindowLeader:
            self.canvas.delete(self.buttonWindowLeader)
    
    def returnToMainMenu(self):

        '''Returns to main menu'''

        # Clean up the canvas (remove all elements)
        self.canvas.delete("all")

        self.quitDeathScreen()

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

        # Resets the user's highest score
        self.gameVariables.setHighestScore(0)
        self.gameVariables.setScore(0)

        # Recreate the main menu
        from mainMenu import MainMenu
        MainMenu(self.window, self.gameVariables)
    
    def tryAgain(self):

        '''Lets user try again'''

        self.quitDeathScreen()
        self.enemyManager.removeAllEnemies()
        self.startingArea.playAgain()
    
    def saveGame(self):

        '''Allows user to save game'''

        # Sets score to 0 and health to 3 since the player has died and wont be continuing a game
        # Increments deathCounter by 1 to take into account that the player has died
        saveDictionary = {
            "deathCounter": self.player.getDeathCounter() + 1,
            "score": 0,
            "playerHealth": 3,
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

    def getPlayerName(self):

        '''Gets users name from input'''

        # Will loop until player adds valid name
        while True:

            # Ask for player name
            playerName = simpledialog.askstring("Enter Name", "Enter your name (3 characters max):\nLeave blank if you don't want to be registered")

            # Handle cancel or empty input
            if playerName is None or playerName.strip() == "":
                return None

            # Check if input length is valid
            if len(playerName.strip()) > 3:
                messagebox.showwarning("Invalid Name", "Name must be 3 characters or less.")
                continue

            if not playerName.isalnum:
                messagebox.showwarning("Invalid Name", "Must only contain letters and numbers")
                continue
            
            # Makes name uppercase
            return playerName.upper()
    
    def addToLeaderBoard(self, playerName):
        
        try:

            with open("leaderboard.json", "r") as file:
                leaderboard = json.load(file)
        
        except FileNotFoundError:
            
            # Default empty leaderboard
            leaderboard = {"names": []}
        
        # Add player name and score to the leaderboard
        leaderboardArray = leaderboard["names"]
        leaderboardArray.append([self.gameVariables.getScore(), playerName])

        # Sort leaderboardArray so that highest score goes first
        leaderboardArray.sort(reverse=True)
        
        # Will remove anyone that isn't top 10 on the leaderboard
        while len(leaderboardArray) > 10:
            leaderboardArray.pop()
        
        leaderboard["names"] = leaderboardArray

        # Save the updated leaderboard back to the file
        try:

            with open("leaderboard.json", "w") as file:
                json.dump(leaderboard, file, indent=4)
        
        except Exception as e:
            messagebox.showerror("Error", f"There was an error saving to the leaderboard: {e}")
    
    def showLeaderBoard(self):

        self.leaderBoardWindow = tk.Toplevel(self.window)
        self.leaderBoardWindow.title("Leader Board")
        self.leaderBoardWindow.geometry("1024x1024")

        # Make it so that it cant be resized
        self.leaderBoardWindow.resizable(False, False)

        # Opens leader board
        from leaderboardMenu import LeaderboardMenu
        leaderboard = LeaderboardMenu(self.leaderBoardWindow, self.gameVariables, False)

        leaderboard.createLeaderboardDisplay()