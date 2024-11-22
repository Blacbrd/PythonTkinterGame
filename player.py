from PIL import Image, ImageTk

class Player:

    '''This is the main object that the user controls'''

    def __init__(self, canvas, gameVariables, savedGame):

        self.canvas = canvas
        self.gameVariables = gameVariables
        self.savedGame = savedGame

        # This is the player's starting position, which will be in the middle of the screen
        # NOTE: This won't look like the center as it is a grid layout, so the player will occupy the bottom right center square
        self.x, self.y = 512, 512

        # Adds initial position of the player to the coordinate array
        self.gameVariables.addToCoordinateArray([self.x, self.y, "player", self])
        
        if self.gameVariables.getBrainRot():
            PLAYER_SPRITE = "Images/myNewCharacter.png"
        else:
            PLAYER_SPRITE = "Images/deer.png"
        
        if self.gameVariables.getInvisible():
            PLAYER_SPRITE = "Images/invisible.png"

        # This will be the player's sprite, 64x64
        self.playerImage = Image.open(PLAYER_SPRITE)
        self.playerImage = self.playerImage.resize((64, 64))
        self.image = ImageTk.PhotoImage(self.playerImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw", tag="Player")

        # This will be the player's starting health
        self.health = 3
        
        # This will be the image that shows when the player is hurt
        self.hurtImage = None
        self.hurtSprite = None

        # This will be the player's starting XP
        self.xp = 100

        # This will be how many times the player has lost
        if self.savedGame != None:
            self.deathCounter = savedGame["deathCounter"]

            # This is to prevent players from reseting to get health back
            self.health = savedGame["playerHealth"]

            # No longer saved game
            self.savedGame = None
        else:
            self.deathCounter = 0

            # This will be the player's starting health
            self.health = 3

        # This will be the player's movement speed
        self.velocity = 64
    
    def getX(self):

        '''Getter'''

        return self.x
    
    def getY(self):

        '''Getter'''

        return self.y
    
    def setX(self, x):

        '''Setter'''

        self.x = x
    
    def setY(self, y):

        '''Setter'''

        self.y = y
    
    def getDeathCounter(self):

        '''Setter'''

        return self.deathCounter
    
    def setDeathCounter(self, number):

        '''Setter'''

        self.deathCounter = number
    
    def setPlayerDeath(self, playerDeath):

        '''Setter'''

        self.playerDeath = playerDeath
    
    def getSprite(self):
        
        '''Getter'''

        return self.sprite
    
    def setHealth(self, health):

        '''Setter'''

        self.health = health
    
    def getHealth(self):

        '''Getter'''

        return self.health
    
    # This flips the player sprite from left and right depending on which way they're facing
    def flipSprite(self, direction):

        '''Flips sprite direction depending on user input'''
        
        if direction == "Left":
            self.image = self.playerImage.transpose(Image.FLIP_LEFT_RIGHT)
            self.image = ImageTk.PhotoImage(self.image)

            self.canvas.itemconfig(self.sprite, image=self.image)
        
        else:

            self.image = ImageTk.PhotoImage(self.playerImage)

            self.canvas.itemconfig(self.sprite, image=self.image)

    def move(self, horizontal, vertical):

        '''Moves the player image across the screen'''

        # Remove previous instance of player
        self.gameVariables.removeFromCoordinateArray([self.x, self.y, "player", self])

        # This is by how much the player will move, if the up arrow is pressed, they will move -64 y pixels
        self.x += horizontal * self.velocity
        self.y += vertical * self.velocity

        # Updates frame
        self.canvas.move(self.sprite, horizontal * self.velocity, vertical * self.velocity)

        # Add new position to coordinate array
        self.gameVariables.addToCoordinateArray([self.x, self.y, "player", self])

        self.canvas.tag_raise(self.sprite)

    # If array[2] is door, then the player can go over it
    def collision(self, horizontal, vertical, coordinateArray):

        '''Checks if the player is colliding with anything'''
        
        tempPlayerX = self.x
        tempPlayerY = self.y

        tempPlayerX += horizontal * self.velocity
        tempPlayerY += vertical * self.velocity

        # Will iterate through each array of the coordinate array
        for array in coordinateArray:

            if tempPlayerX == array[0] and tempPlayerY == array[1] and array[2] != "door" and array[2] != "player":

                # If the player is 2 away from a wall or enemy, they will still dash but only move 1 block
                if abs(horizontal) == 2 or abs(vertical) == 2:

                    self.move(self.gameVariables.isPositive(horizontal), self.gameVariables.isPositive(vertical))

                    return

                return
        
        # If the player is dashing
        if abs(horizontal) == 2 or abs(vertical) == 2:
            
            for array in coordinateArray:
                
                # Check if there is a collision right in front of the player, if there is, do not allow dash
                if tempPlayerX - (self.velocity * self.gameVariables.isPositive(horizontal)) == array[0] and tempPlayerY - (self.velocity * self.gameVariables.isPositive(vertical)) == array[1] and array[2] != "door" and array[2] != "player":

                    return

        self.move(horizontal, vertical)
    
    def takeDamage(self):

        '''If the user is hit, remove hp. If hp 0, then the player dies'''

        if self.gameVariables.getInvincible():
            return
        
        self.health -= 1

        if self.health == 2:
            self.hurtImage = "Images/health2.png"
        elif self.health == 1:
            self.hurtImage = "Images/health1.png"
        
        if self.health != 0:
            self.hurtImageOpen = Image.open(self.hurtImage)
            self.hurtImageOpen = self.hurtImageOpen.resize((1024, 1024))
            self.hurtImageOpen = ImageTk.PhotoImage(self.hurtImageOpen)
            self.hurtSprite = self.canvas.create_image(0, 0, image=self.hurtImageOpen, anchor="nw", tag="Hurt")
            self.canvas.after(500, self.deleteHealthScreen)

        if self.health == 0:
            self.playerDeath.showDeath()
    
    def resetPosition(self):

        '''Moves the player back to the center of the screen'''

        self.gameVariables.removeFromCoordinateArray([self.x, self.y, "player", self])
        self.canvas.delete(self.sprite)

        self.x, self.y = 512, 512

        self.gameVariables.addToCoordinateArray([self.x, self.y, "player", self])

        if self.gameVariables.getBrainRot():
            PLAYER_SPRITE = "Images/myNewCharacter.png"
        else:
            PLAYER_SPRITE = "Images/deer.png"
        
        if self.gameVariables.getInvisible():
            PLAYER_SPRITE = "Images/invisible.png"
        
        self.playerImage = Image.open(PLAYER_SPRITE)
        self.playerImage = self.playerImage.resize((64, 64))
        self.image = ImageTk.PhotoImage(self.playerImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw")
    
    def deleteHealthScreen(self):

        '''Removes heart overlay'''

        if self.hurtSprite:
            self.canvas.delete(self.hurtSprite)