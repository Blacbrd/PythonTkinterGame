from tkinter import messagebox, simpledialog

class CheatCodeMenu:

    '''Allows the user to write cheat codes into a simpledialog box'''

    def __init__(self, window, gameVariables):
        
        self.window = window
        self.gameVariables = gameVariables

        self.activeCheatCodes = self.gameVariables.getActiveCheatCodeArray()

    def showCheatCodeMenu(self):

        '''Allows the user to type in a cheat code. If the cheat code is invalid, an error message is shown. If cheat code already exists, remove it.'''

        # Use '\n'.join to format the array elements into a string
        cheatCodeDisplay = "\n".join(self.activeCheatCodes)

        # Display the dialog with the formatted string
        cheatCode = simpledialog.askstring(
            "Cheat code",
            f"Enter a cheat code!\nCurrent active cheat codes:\n{cheatCodeDisplay}"
        )

        if cheatCode is None:
            return
        
        cheatCode = cheatCode.lower()
        
        valid = self.validateCode(cheatCode)
        if valid:

            if cheatCode in self.gameVariables.getActiveCheatCodeArray():
                
                self.gameVariables.removeFromActiveCheatCodeArray(cheatCode)

                if cheatCode == "invisible":
                    self.gameVariables.setInvisible(False)
                elif cheatCode == "invincible":
                    self.gameVariables.setInvincible(False)
                elif cheatCode == "hardmode":
                    self.gameVariables.setHardMode(False)
                elif cheatCode == "friendly":
                    self.gameVariables.setFriendlyEnemies(False)
                elif cheatCode == "speed":
                    self.gameVariables.setFastProjectile(False)
                elif cheatCode == "brainrot":
                    self.gameVariables.setBrainRot(False)
                
                return

            self.gameVariables.addToActiveCheatCodeArray(cheatCode)

            if cheatCode == "invisible":
                self.gameVariables.setInvisible(True)
            elif cheatCode == "invincible":
                self.gameVariables.setInvincible(True)
            elif cheatCode == "hardmode":
                self.gameVariables.setHardMode(True)
            elif cheatCode == "friendly":
                self.gameVariables.setFriendlyEnemies(True)
            elif cheatCode == "speed":
                self.gameVariables.setFastProjectile(True)
            elif cheatCode == "brainrot":
                self.gameVariables.setBrainRot(True)
        
        else:
            messagebox.showerror("Invalid cheat code", f"'{cheatCode}' is not a valid cheat code!")
    
    def validateCode(self, cheatCode):

        '''Validates user's inputted cheat code.'''
        
        if len(cheatCode) < 0:
            return False
        
        validCheatCodeArray = [
            "invisible", "invincible", "hardmode", "friendly", "speed", "brainrot"
        ]

        if cheatCode not in validCheatCodeArray:
            return False
        
        return True