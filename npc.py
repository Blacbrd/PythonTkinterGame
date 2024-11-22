from PIL import Image, ImageTk
import random

class Npc:

    '''Npc tells the user how many lives they've lost and their highest score'''

    def __init__(self, canvas, gameVariables):

        self.canvas = canvas
        self.gameVariables = gameVariables

        # This is where the NPC will be, 3 cells up from the player
        self.x, self.y = 512, 320
        
        # Will make it so that the interact is not called over and over
        self.dialogueActive = False
        
        # This will be the returned message
        self.message = ""

        if self.gameVariables.getBrainRot():
            NPC_SPRITE = "Images/myNewCharacter.png"
        else:
            NPC_SPRITE = "Images/oldBird.png"

        # This will be the npc's sprite, 64x64
        self.npcImage = Image.open(NPC_SPRITE)
        self.npcImage = self.npcImage.resize((64, 64))
        self.image = ImageTk.PhotoImage(self.npcImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw", tags="MainMenu")
    
    def getX(self):

        '''Getter'''

        return self.x
    
    def getY(self):
        
        '''Getter'''

        return self.y
    
    def npcDialogue(self, deathCounter):

        '''Chooses what the NPC will say to the player'''

        # Door will appear at the end of the bird's speech

        if deathCounter == 0:
            
            return [

                "Ahh, I see they've got another one trapped down here.",
                "Don't even worry young one,",
                "Getting out of here is as easy as taking this door!",
                "Good luck on your adventure!"
            ]

        if deathCounter == 1:
            
            return [

                "Ahh, I see that you're back here,",
                "What, you thought you could get out on your first try?",
                "Youngsters these days, thinking they can get everything with no effort.",
                "Try again, you might make it out this time!"
            ]

        randomMessage1 = [

            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "Come on, again?",
            "It's almost as if you're trying to lose on purpose",
            "I'm just messing with you, you know, of course no one will escape without practice",
            "You've got this, enter the door"
        ]

        randomMessage2 = [

            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "Death in this realm is temporary",
            "You can try and escape as many times as you want",
            "But wouldn't death be more satisfying than being stuck in this limbo?",
            "If you don't want to become mad like me, hurry up and escape!"
        ]

        randomMessage3 = [
            
            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "Angry about your last death?",
            "Use that anger to fuel your determination",
            "Make whatever sicko that put us here pay!",
            "Go get 'em, Deer"
        ]

        randomMessage4 = [

            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "You know, I've tried to beat the dungeons before",
            "For the first couple years, I tried time and time again",
            "But after a while, your body starts to give up on you",
            "I hope you don't end up like me"
        ]

        randomMessage5 = [

            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "You've died so many times,",
            "That you've probably heard me repeat myself!",
            "No need to be embarassed, it's just this game's creator was too lazy to add more messages",
            "Beat him at his own game, beat the dungeons!"
        ]

        randomMessage6 = [

            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "You've got this."
        ]

        randomMessage7 = [
            f"You've died {deathCounter} times so far...",
            f"Your highest score is {self.gameVariables.getHighestScore()}!",
            "And no, that's not a factorial by your highest score...",
            "I'm just happy that you've defeated that many enemies!",
            "Lets see how much higher you can get that number...",
            "Maybe if it becomes high enough, you'll be able to escape!"
        ]

        # If dialogue was not active, it will choose a random message
        if not self.dialogueActive:

            # Chooses a random message
            choice = random.randint(0, 6)

            match choice:

                case 0:
                    self.message = randomMessage1
                
                case 1:
                    self.message = randomMessage2
                
                case 2:
                    self.message = randomMessage3
                
                case 3:
                    self.message = randomMessage4
                
                case 4:
                    self.message = randomMessage5
                
                case 5:
                    self.message = randomMessage6
                
                case 6:
                    self.message = randomMessage7
                
                case _:
                    self.message = "There was an error in the code"
        
        return self.message
    
    def npcDialogueSaved(self, deathCounter, playerHealth):
        
        return [
            "This is a loaded game file!",
            f"You've died {deathCounter} time(s)",
            f"Your current score will be {self.gameVariables.getScore()},",
            f"Your highest score is {self.gameVariables.getHighestScore()}",
            f"And you'll start with {playerHealth} health",
            "Good luck!"
        ]
    
    def setDialogueActive(self, boolean):
        self.dialogueActive = boolean