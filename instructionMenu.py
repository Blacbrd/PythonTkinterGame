import tkinter as tk
from PIL import Image, ImageTk

class InstructionMenu:

    '''Menu that shows the user how to play the game'''

    def __init__(self, window, gameVariables):
        self.window = window
        self.gameVariables = gameVariables

        # Create a frame for the instruction menu
        self.frame = tk.Frame(self.window, width=1024, height=1024)
        self.frame.pack()

        # Load and display the background image
        self.instructionImage = Image.open("Images/instructionMenu.png")
        self.instructionImage = self.instructionImage.resize((1024, 1024))
        self.instructionImageTk = ImageTk.PhotoImage(self.instructionImage)

        # Add the background image to a label
        self.backgroundLabel = tk.Label(self.frame, image=self.instructionImageTk)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a button to return to the main menu
        self.mainMenuButton = tk.Button(
            self.frame,
            text="Main Menu",
            font=("Arial", 14),
            bg="black",
            fg="white",
            command=self.returnToMainMenu
        )

        # Places at the bottom of the screen
        self.mainMenuButton.place(relx=0.5, rely=0.9, anchor="center")

    def returnToMainMenu(self):
        
        '''Takes the user back to the main menu'''
        
        # Destroy the frame to return to the main menu
        self.frame.destroy()

        # Reinitialize the MainMenu
        # Import here to avoid circular imports
        from mainMenu import MainMenu
        MainMenu(self.window, self.gameVariables)