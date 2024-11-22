import tkinter as tk
from PIL import Image, ImageTk
import atexit


# All of these are imports from my files
from player import Player
from npc import Npc
from door import Door
from pauseMenu import PauseMenu
import movementManager
from musicManager import stopMusic, playMusic
import config
from projectileManager import ProjectileManager
from playerDeath import PlayerDeath


class StartingArea:

    def __init__(self, window, gameVariables, savedGame):

        self.window = window
        self.gameVariables = gameVariables
        self.savedGame = savedGame

        # This creates a window of size 1024x1024, and centres it on the user's screen
        width, height = 1024, 1024
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        offsetx = (screenWidth - width) // 2
        offsety = (screenHeight - height) // 2
        self.window.geometry(f"{width}x{height}+{offsetx}+{offsety-32}")

        # Initialises canvas object on screen
        # highlight thickness removes white border around canvas
        self.canvas = tk.Canvas(window, bg="white", highlightthickness=0, width=1024, height=1024)
        self.canvas.pack()

        if self.gameVariables.getBrainRot():
            BACKGROUND_IMAGE = "Images/myNewCharacter.png"
        else:
            BACKGROUND_IMAGE= "Images/startingBg.png"

        # Creates and draws canvas background
        bgImage = Image.open(BACKGROUND_IMAGE)
        bgImage = bgImage.resize((1024, 1024))
        self.bgImage = ImageTk.PhotoImage(bgImage)
        bgImageCanvas = self.canvas.create_image(0, 0, image=self.bgImage, anchor="nw")

        # Lower background image to bottom layer
        self.canvas.tag_lower(bgImageCanvas)

        # Add NPC to scene
        self.npc = Npc(self.canvas, self.gameVariables)

        self.gameVariables.createWallCollision()

        # Adds NPC coordinates to game variables
        self.gameVariables.addToCoordinateArray([self.npc.getX(), self.npc.getY(), "npc"])

        # Initialises player
        self.player = Player(self.canvas, self.gameVariables, self.savedGame)

        # Pause functionality
        self.pauseMenu = PauseMenu(self.window, self.canvas, self.player, self.gameVariables, self)

        # Initialises projectile manager to allow for projectiles
        self.projectileManager = ProjectileManager(self.canvas, self.pauseMenu, self.gameVariables)

        # Initialises playerDeath to allow for restart logic
        self.playerDeath = PlayerDeath(self.window, self.canvas, self.player, self.gameVariables, self, self.pauseMenu, self.projectileManager)
        self.player.setPlayerDeath(self.playerDeath)

        # To avoid circular dependency, set projectile manager now
        self.pauseMenu.setProjectileManager(self.projectileManager)

        # Stops previous music, then plays new music
        # stopMusic()
        # playMusic("Sounds/oldBird.wav")
        
        self.setKeyBinds()

        self.projectileManager.update()

        # Register the stopMusic function to run on exit, mostly relevant to Mac and Linux users
        atexit.register(stopMusic)

    def setKeyBinds(self):

        # Update controls
        self.controls = config.loadControls()

        # This listens to a keypress and then calls the moveKeyPress function 
        self.window.bind("<KeyPress>", lambda event: movementManager.moveKeyPress(event, self.player, self.gameVariables, self.controls))

        # This listens to a keyrelease and then calls the keyRelease function
        self.window.bind("<KeyRelease>", lambda event: movementManager.keyRelease(event, self.gameVariables))

        self.window.bind(f"<{self.controls['pause']}>", lambda event: self.pauseMenu.togglePause(event, self.player, self.gameVariables))

        # Boss key binding
        self.window.bind(f"<{self.controls['bossKey']}>", lambda event: movementManager.openBossKey(event, self.window, self.pauseMenu, self.player, self.gameVariables))

        # Interact key binding
        self.window.bind(f"<{self.controls['interact']}>", lambda event: movementManager.interact(event, self.window, self.player, self.npc, self.canvas, self.gameVariables.getCoordinateArray(), self.gameVariables, self.controls, self.projectileManager, self.pauseMenu, self.playerDeath, self.savedGame, self))

        # Projectile keybinds
        self.window.bind(f"<{self.controls['shootLeft']}>", lambda event: movementManager.shootProjectileLeft(event, self.canvas, self.player, self.projectileManager))
        self.window.bind(f"<{self.controls['shootRight']}>", lambda event: movementManager.shootProjectileRight(event, self.canvas, self.player, self.projectileManager))
        self.window.bind(f"<{self.controls['shootUp']}>", lambda event: movementManager.shootProjectileUp(event, self.canvas, self.player, self.projectileManager))
        self.window.bind(f"<{self.controls['shootDown']}>", lambda event: movementManager.shootProjectileDown(event, self.canvas, self.player, self.projectileManager))
    
    # Unbinds all keys, used for pause
    def removeKeyBinds(self):

        # Update controls
        self.controls = config.loadControls()

        self.window.unbind("<KeyPress>")
        self.window.unbind("<KeyRelease>")

        # Interact key binding
        self.window.unbind(f"<{self.controls['interact']}>")

        # Projectile keybinds
        self.window.unbind(f"<{self.controls['shootLeft']}>")
        self.window.unbind(f"<{self.controls['shootRight']}>")
        self.window.unbind(f"<{self.controls['shootUp']}>")
        self.window.unbind(f"<{self.controls['shootDown']}>")
    
    def playAgain(self):

        # Sends player to starting position
        self.player.resetPosition()

        self.player.setHealth(3)

        # Resets score back to zero
        self.gameVariables.setScore(0)

        # Increment death counter by 1
        self.player.setDeathCounter(self.player.getDeathCounter() + 1)

        # Add NPC to scene
        self.npc = Npc(self.canvas, self.gameVariables)

        # Adds NPC coordinates to game variables
        self.gameVariables.addToCoordinateArray([self.npc.getX(), self.npc.getY(), "npc"])

        # Allow the NPC to talk again
        self.gameVariables.setAllowDialogue(True)

        self.canvas.tag_raise(self.player.getSprite())
        
        # Allows the player to move
        self.setKeyBinds()

        self.projectileManager.deleteProjectiles()

        # Allows all the managers to start again
        self.pauseMenu.setAllowPause(True)
        self.projectileManager.setStop(False)
        self.pauseMenu.setIsPaused(False)

        # This allows me to resume the projectile manager
        self.projectileManager.setIsPaused(True)
        self.projectileManager.resume()
    
    def setSavedGameToNone(self):
        self.savedGame = None