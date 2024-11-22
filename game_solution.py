import tkinter as tk

# All of these are imports from my files
from mainMenu import MainMenu
from gameVariables import GameVariables

# This will be my main Tkinter object
window = tk.Tk()
window.title("No Eye Deer")

# Instantiate gameVariables object
gameVariables = GameVariables()

def main():

    '''Starts the game'''

    # Instantiates main menu class and opens a Tkinter window
    MainMenu(window, gameVariables)
    window.mainloop()

if __name__ == "__main__":
    main()