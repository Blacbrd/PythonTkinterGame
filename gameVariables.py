import math
# Since I am dealing with multiple files, I have to make a global counter for multiple variables
class GameVariables:

    '''Main file for game states, remembers important variables'''

    def __init__(self):

        self.keyPressed = {}
        self.dashFlag = False

        self.coordinateArray = []

        self.dialogueActive = False
        self.dialogueIndex = 0
        self.dialogueLabel = None
        self.allowDialogue = True

        # This will store all the active cheat-codes
        self.activeCheatCodeArray = []

        # Active cheat codes
        self.invincible = False
        self.invisible = False
        self.hardMode = False
        self.freindlyEnemies = False
        self.fastProjectile = False
        self.brainRot = False

        # Keeps the player's score
        self.score = 0
        self.highestScore = 0

        # This will be used when the user loads a game
        self.enemyLocations = []

        # This will be the difficulty of the game
        self.difficulty = "easy"
    
    def getInvincible(self):

        '''Getter'''

        return self.invincible
    
    def setInvincible(self, boolean):
        
        '''Setter'''

        self.invincible = boolean
    
    def getInvisible(self):

        '''Getter'''

        return self.invisible
    
    def setInvisible(self, boolean):

        '''Setter'''

        self.invisible = boolean
    
    def getHardMode(self):

        '''Getter'''

        return self.hardMode

    def setHardMode(self, boolean):

        '''Setter'''

        self.hardMode = boolean
    
    def getFriendlyEnemies(self):

        '''Getter'''

        return self.freindlyEnemies
    
    def setFriendlyEnemies(self, boolean):

        '''Setter'''

        self.freindlyEnemies = boolean
    
    def getFastProjectile(self):

        '''Getter'''

        return self.fastProjectile
    
    def setFastProjectile(self, boolean):

        '''Setter'''

        self.fastProjectile = boolean
    
    def getBrainRot(self):

        '''Getter'''

        return self.brainRot
    
    def setBrainRot(self, boolean):

        '''Setter'''

        self.brainRot = boolean

    def getActiveCheatCodeArray(self):

        '''Getter'''

        return self.activeCheatCodeArray
    
    def removeFromActiveCheatCodeArray(self, toRemove):

        '''Removes item from cheat code array'''

        self.activeCheatCodeArray.remove(toRemove)

    def getKeyPressed(self):

        '''Getter'''

        return self.keyPressed
    
    def addToKeyPressed(self, item):

        '''Adds item to key pressed array'''

        self.keyPressed[item] = True

    def removeFromKeyPressed(self, item):

        '''Remove item from key press array'''

        del self.keyPressed[item]

    def getDashFlag(self):

        '''Getter'''

        return self.dashFlag
    
    def setDashFlag(self, flag):

        '''Setter'''

        self.dashFlag = flag
    
    def getCoordinateArray(self):

        '''Getter'''

        return self.coordinateArray
    
    def addToCoordinateArray(self, array):

        '''Adds item to coordinate array'''

        self.coordinateArray.append(array)
    
    # Will implement later, when enemies move, will need to update specific items
    def removeFromCoordinateArray(self, toRemove):

        '''Removes item from coordinate array'''

        self.coordinateArray.remove(toRemove)

    def clearCoordinateArray(self):

        '''Clears coordinate array, removes all items'''

        self.coordinateArray = []
    
    def getDialogueActive(self):

        '''Getter'''

        return self.dialogueActive
    
    def setDialogueActive(self, boolean):

        '''Setter'''

        self.dialogueActive = boolean
    
    def getDialogueIndex(self):

        '''Getter'''

        return self.dialogueIndex
    
    def setDialogueIndex(self, index):

        '''Setter'''

        self.dialogueIndex = index
    
    def getDialogueLabel(self):

        '''Getter'''

        return self.dialogueLabel
    
    def setDialogueLabel(self, label):

        '''Setter'''

        self.dialogueLabel = label
    
    def getAllowDialogue(self):

        '''Getter'''

        return self.allowDialogue
    
    def setAllowDialogue(self, boolean):

        '''Setter'''

        self.allowDialogue = boolean
    
    def addToActiveCheatCodeArray(self, cheatCode):

        '''Adds cheat code to active cheatcodes'''

        self.activeCheatCodeArray.append(cheatCode)
    
    def incrementScore(self):
        
        '''Increments score by 1'''

        self.score += 1
    
    def setScore(self, score):

        '''Setter'''

        self.score = score
    
    def getScore(self):

        '''Getter'''

        return self.score
    
    def setHighestScore(self, highScore):

        '''Setter'''

        self.highestScore = highScore
    
    def getHighestScore(self):

        '''Getter'''

        return self.highestScore
    
    def getDifficulty(self):

        '''Getter'''

        return self.difficulty
    
    def setDifficulty(self, difficulty):

        '''Setter'''
        
        self.difficulty = difficulty
    
    def createWallCollision(self):

        '''Creates collisions for walls'''
        
        for i in range(0, 16):

            # Top wall
            self.addToCoordinateArray([i*64, 0, "wall"])

            # Bottom wall
            self.addToCoordinateArray([i*64, 960, "wall"])

            # Left wall
            self.addToCoordinateArray([0, i*64, "wall"])

            # Right wall
            self.addToCoordinateArray([960, i*64, "wall"])
    
    def isPositive(self, num):

        '''This will return whether the number is positive or not. Will return 0 if number is 0'''

        if math.copysign(1, num) == 1:
            return 1 if num != 0 else 0
        
        else:
            return -1
