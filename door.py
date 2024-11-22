from PIL import Image, ImageTk

class Door:

    def __init__(self, window, canvas, gameVariables):
        # This is where the door will be, 3 cells right from the NPC
        self.x, self.y = 704, 320

        self.window = window
        self.canvas = canvas

        self.gameVariables = gameVariables

        if self.gameVariables.getBrainRot():
            DOOR_SPRITE = "Images/myNewCharacter.png"
        else:
            DOOR_SPRITE = "Images/door.png"

        # This will be the npc's sprite, 64x64
        self.doorImage = Image.open(DOOR_SPRITE)
        self.doorImage = self.doorImage.resize((64, 64))
        self.image = ImageTk.PhotoImage(self.doorImage)
    
        self.window.image = self.image
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw", tags="MainMenu")
    
    def getX(self):

        '''Gets door x coordinate'''

        return self.x
    
    def getY(self):

        '''Gets door y coordinate'''

        return self.y
    
    def setVisible(self, visible):

        '''The door will appear if this is true'''

        self.visible = visible
        
    def getVisible(self):
        
        '''Gets whether the door is visible or not'''
        
        return self.visible
    
    def getSprite(self):
        
        '''Gets the door's sprite'''

        return self.sprite