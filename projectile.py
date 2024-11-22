from PIL import Image, ImageTk

class Projectile:

    def __init__(self, object, canvas, direction, directionString, enemyProjectile, gameVariables):
        
        # Projectile starting point at player or enemy
        self.x, self.y = object.getX()+16, object.getY()+16

        self.canvas = canvas
        self.direction = direction
        self.enemyProjectile = enemyProjectile
        self.gameVariables = gameVariables

        # LATER ON, WHEN I WANT DIAGONAL MOVEMENT, I'LL CHANGE THIS
        if self.gameVariables.getFastProjectile():
            self.velocityX = 35
            self.velocityY = 35
        else:
            self.velocityX = 5
            self.velocityY = 5

        self.radius = 5 # TEMP VALUE

        # Enemies will use a different sprite to avoid confusion

        if self.gameVariables.getBrainRot():
            PROJECTILE_SPRITE, PROJECTILE_SPRITE_ENEMY = "Images/myNewCharacter.png", "Images/myNewCharacter.png"
        else:
            PROJECTILE_SPRITE = "Images/fireball.png"
            PROJECTILE_SPRITE_ENEMY = "Images/fireballEnemy.png"

        if self.enemyProjectile:
            self.projectileImage = Image.open(PROJECTILE_SPRITE_ENEMY)
        else:
            self.projectileImage = Image.open(PROJECTILE_SPRITE)

        self.projectileImage = self.projectileImage.resize((32, 32))
        self.image = ImageTk.PhotoImage(self.projectileImage)
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw")
        
        # Sets the direction of the sprite
        self.projectileSpriteOrientation(directionString)

        # When projectile is called, it will be activated
        self.isActive = True
    
    def move(self):
        
        # If projectile isn't active, it can't be moved
        if not self.isActive:
            return
        
        # This will be the new position of the projectile
        positionX = self.direction[0] * self.velocityX
        positionY = self.direction[1] * self.velocityY

        # Update projectile position
        self.x += positionX
        self.y += positionY

        self.canvas.move(self.sprite, positionX, positionY)

    def collision(self):

        # If projectile isn't active, it can't be moved
        if not self.isActive:
            return
        
        for array in self.gameVariables.getCoordinateArray():

            # If the projectile is in the cell
            if (self.x >= array[0] and self.x < array[0] + 64) and (self.y >= array[1] and self.y < array[1] + 64):

                if (array[2] == "wall"):
                    self.deleteProjectile(False, False, array)
                    return
                elif array[2] == "enemy" and not self.enemyProjectile:
                    self.deleteProjectile(True, False, array)
                    return
                elif array[2] == "player" and self.enemyProjectile:
                    self.deleteProjectile(False, True, array)
        
        self.move()

    def deleteProjectile(self, enemyHitFlag, playerHitFlag, array):
        
        if enemyHitFlag:

            # Grabs the enemy object at that coordinate and removes 1 off its HP            
            enemy = array[3]
            enemy.enemyHit()
        
        if playerHitFlag:
            player = array[3]
            player.takeDamage()
        
        self.isActive = False
        self.canvas.delete(self.sprite)

    def getIsActive(self):
        return self.isActive

    # This will choose which way the projectile is facing
    def projectileSpriteOrientation(self, direction):

        match direction:

            case "left":
                self.image = self.projectileImage.transpose(Image.FLIP_LEFT_RIGHT)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "up":
                self.image = self.projectileImage.rotate(90, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "down":
                self.image = self.projectileImage.rotate(-90, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "rightdown":
                self.image = self.projectileImage.rotate(45, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "rightup":
                self.image = self.projectileImage.rotate(-45, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "leftdown":
                self.image = self.projectileImage.transpose(Image.FLIP_LEFT_RIGHT)
                self.image = self.projectileImage.rotate(45, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)
            
            case "leftup":
                self.image = self.projectileImage.transpose(Image.FLIP_LEFT_RIGHT)
                self.image = self.projectileImage.rotate(-45, expand=True)
                self.image = ImageTk.PhotoImage(self.image)

                self.canvas.itemconfig(self.sprite, image=self.image)


            
            # Do nothing if input not recognised, or is "right"
            case _:
                pass