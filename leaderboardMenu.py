import tkinter as tk
from PIL import Image, ImageTk
import json

class LeaderboardMenu:

    '''Shows the top 10 best players that have registered their names with the leaderboard'''

    def __init__(self, window, gameVariables, mainMenuFlag):

        self.window = window
        self.gameVariables = gameVariables
        self.mainMenuFlag = mainMenuFlag

        self.frame = tk.Frame(self.window, width=1024, height=1024)
        self.frame.pack()

        # Load leaderboard data from the JSON file
        try:

            with open("leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)

        except FileNotFoundError:
            self.leaderboard = {"names": []}

    def createLeaderboardDisplay(self):
        
        '''Creates leader board GUI'''

        self.window.title("Leaderboard")
        self.window.geometry("1024x1024")

        # Add a title label
        title_label = tk.Label(self.frame, text="Leaderboard", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Access the leaderboard array
        leaderboardArray = self.leaderboard["names"]

        # Display each entry with numbering using enumerate
        for index, (score, name) in enumerate(leaderboardArray, start=1):

            # Create a label for each leaderboard entry
            nameScoreLabel = tk.Label(
                self.frame,
                text=f"{index}. {name} : {score}",
                font=("Arial", 14)
            )

            nameScoreLabel.pack(anchor="center", padx=20)
        
        if self.mainMenuFlag:
            mainMenuButton = tk.Button(self.frame, text="Main Menu", font=("Arial", 12), command=self.returnToMainMenu)
            mainMenuButton.pack(pady=20)
        else:
            mainMenuButton = tk.Button(self.frame, text="Close", font=("Arial", 12), command=self.exitLeaderBoardMenu)
            mainMenuButton.pack(pady=20)
    
    def returnToMainMenu(self):
        
        '''Allows user to go back to main menu'''

        self.frame.destroy()

        # Reinitialize the MainMenu
        # Import here so that no circular import is generated
        from mainMenu import MainMenu
        MainMenu(self.window, self.gameVariables)
    
    def exitLeaderBoardMenu(self):
        
        '''Closes window'''

        self.window.destroy()