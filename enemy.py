from PIL import Image, ImageTk
import random

class Enemy:

    '''This will be the thing that the player shoots at'''

    def __init__(self, window, canvas, gameVariables, enemyManager, projectileManager):
        
        self.window = window
        self.canvas = canvas
        self.gameVariables = gameVariables
        self.enemyManager = enemyManager
        self.projectileManager = projectileManager
        self.health = 5

        self.difficulty = self.gameVariables.getDifficulty()

        self.validPlacement = False
        self.validCoordinatesFlag = True

        self.stop = False

        # These are flags that determine what sort of enemy will spawn
        self.mediumFlag = False
        self.hardFlag = False

        # This loops until the enemy can be placed in a valid spot
        while not self.validPlacement:

            self.x = random.choice([64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896])
            self.y = random.choice([64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896])

            for array in gameVariables.getCoordinateArray():
                
                # If the enemy shares a spot with anything in the array, such as the player or another enemy, it cannot be spawned there
                if self.x == array[0] and self.y == array[1]:
                    self.validCoordinatesFlag = False
                    break
                
                # If the if statement is never accessed, then this flag will be True
                self.validCoordinatesFlag = True

            if self.validCoordinatesFlag:
                self.validPlacement = True

        ENEMY_SPRITE = "Images/enemy.png"
        
        if self.gameVariables.getDifficulty() == "medium":
            ENEMY_SPRITE = random.choice(["Images/enemy.png", "Images/enemyMedium.png"])

            if ENEMY_SPRITE == "Images/enemyMedium.png":
                self.mediumFlag = True
        
        if self.gameVariables.getDifficulty() == "hard":
            
            ENEMY_SPRITE = random.choice(["Images/enemy.png", "Images/enemyMedium.png", "Images/enemyHard.png"])

            if ENEMY_SPRITE == "Images/enemyMedium.png":
                self.mediumFlag = True
            elif ENEMY_SPRITE == "Images/enemyHard.png":
                self.hardFlag = True
        

        if self.gameVariables.getBrainRot():
            ENEMY_SPRITE = "Images/myNewCharacter.png"

        self.enemyImage = Image.open(ENEMY_SPRITE)
        self.enemyImage = self.enemyImage.resize((64, 64))
        self.image = ImageTk.PhotoImage(self.enemyImage)

        # This extra line allows for the drawing of images outside the 
        self.window.image = self.image
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw")

        # Object also added to array so that I can reference the enemy at that coordinate
        gameVariables.addToCoordinateArray([self.x, self.y, "enemy", self])
    
    def setStop(self, boolean):

        '''If stop is true, enemies will stop shooting'''

        self.stop = boolean

    def enemyHit(self):
        
        '''Reduces enemy hp by 1, if they reach 0 they die'''

        self.health -= 1

        # If the enemy has no more hp left, it will be deleted from the coordinate array
        if self.health == 0:
            self.gameVariables.removeFromCoordinateArray([self.x, self.y, "enemy", self])
            self.canvas.delete(self.sprite)

            self.enemyManager.incrementEnemiesKilled(self)
            self.enemyManager.decrementEnemyCount()
            self.enemyManager.spawnEnemies()
    
    def enemyShoot(self):

        '''Called every few milliseconds, makes the enemy shoot projectiles'''

        if self.gameVariables.getFriendlyEnemies():
            return

        if self.mediumFlag:
            # Randomly selects which direction the fireball will shoot from the enemy
            direction = random.choice([[1,1], [-1, 1], [1, -1], [-1, -1]])

            if direction == [1, 1]:
                stringDirection = "rightdown"
            elif direction == [-1, 1]:
                stringDirection = "leftdown"
            elif direction == [1, -1]:
                stringDirection = "rightup"
            elif direction == [-1, -1]:
                stringDirection = "leftup"

            self.projectileManager.createProjectile(self, direction, stringDirection, True)

        elif self.hardFlag:

            # Randomly selects which direction the fireball will shoot from the enemy
            direction = random.choice([[1,1], [-1, 1], [1, -1], [-1, -1], [1,0], [-1, 0], [0, 1], [0, -1]])

            if direction == [1, 1]:
                stringDirection = "rightdown"
            elif direction == [-1, 1]:
                stringDirection = "leftdown"
            elif direction == [1, -1]:
                stringDirection = "rightup"
            elif direction == [-1, -1]:
                stringDirection = "leftup"
            elif direction == [1, 0]:
                stringDirection = "right"
            elif direction == [-1, 0]:
                stringDirection = "left"
            elif direction == [0, 1]:
                stringDirection = "down"
            elif direction == [0, -1]:
                stringDirection = "up"

            self.projectileManager.createProjectile(self, direction, stringDirection, True)

        else:
            # Randomly selects which direction the fireball will shoot from the enemy
            direction = random.choice([[1,0], [-1, 0], [0, 1], [0, -1]])

            if direction == [1, 0]:
                stringDirection = "right"
            elif direction == [-1, 0]:
                stringDirection = "left"
            elif direction == [0, 1]:
                stringDirection = "down"
            elif direction == [0, -1]:
                stringDirection = "up"

            self.projectileManager.createProjectile(self, direction, stringDirection, True)
        
    def getX(self):

        '''Gets x coordinate of enemy'''

        return self.x
    
    def getY(self):
        
        '''Gets y coordinate of enemy'''

        return self.y
    
    def deleteEnemy(self):
        
        '''Deletes enemy'''

        self.gameVariables.removeFromCoordinateArray([self.x, self.y, "enemy", self])

        self.canvas.delete(self.sprite)