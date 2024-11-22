import webbrowser
from enemyManager import EnemyManager
from door import Door

def moveKeyPress(event, player, gameVariables, controls):

    '''Checks whether the user is holding a key. If they are, cancel all the other subsequent inputs to prevent crazy fast movement and janky gameplay'''

    # Only registers initial press, if the key is already in the dictionary, then the player cannot move again
    if event.keysym in gameVariables.getKeyPressed() and event.keysym != controls['dash']:
        return
    
    # Add key press into the dictionary
    if event.keysym != controls['dash']:
        gameVariables.addToKeyPressed(event.keysym)

    # If the dash key is pressed, the player will be able to move 
    if event.keysym == controls['dash']:

        # Flips the dash flag
        dashFlag = gameVariables.getDashFlag()
        gameVariables.setDashFlag(not dashFlag)    

    # This will go into the json object, and return "w" for normal configuration
    # Since horizontal is 0, the player will not move horizontally
    # Since the vertical is -1, the player will move upwards as this will reduce the y coordinate (therefore going up on the screen)
    if event.keysym == controls['up']:
        player.collision(0, -2, gameVariables.getCoordinateArray()) if gameVariables.getDashFlag() else player.collision(0, -1, gameVariables.getCoordinateArray())

        # Resets the dashFlag if set to true
        if gameVariables.getDashFlag():
            gameVariables.setDashFlag(False)
    
    elif event.keysym == controls['down']:
        player.collision(0, 2, gameVariables.getCoordinateArray()) if gameVariables.getDashFlag() else player.collision(0, 1, gameVariables.getCoordinateArray())

        if gameVariables.getDashFlag():
            gameVariables.setDashFlag(False)
    
    elif event.keysym == controls['left']:
        player.collision(-2, 0, gameVariables.getCoordinateArray()) if gameVariables.getDashFlag() else player.collision(-1, 0, gameVariables.getCoordinateArray())

        if gameVariables.getDashFlag():
            gameVariables.setDashFlag(False)

        player.flipSprite("Left")
    
    elif event.keysym == controls['right']:
        player.collision(2, 0, gameVariables.getCoordinateArray()) if gameVariables.getDashFlag() else player.collision(1, 0, gameVariables.getCoordinateArray())

        if gameVariables.getDashFlag():
            gameVariables.setDashFlag(False)

        player.flipSprite("Right")

# This checks when a button has been released
def keyRelease(event, gameVariables):

    '''If the key is released, it means the player is no longer holding it, meaning that it can be pressed once more'''

    # If the key is present in keysPressed, it is deleted to allow for another input
    if event.keysym in gameVariables.getKeyPressed():
        gameVariables.removeFromKeyPressed(event.keysym)

# Minimises the window and opens a web browser
def openBossKey(event, window, pauseMenu, player, gameVariables):

    '''If your boss is coming, press this key to make it look like you're doing work!'''

    pauseMenu.togglePause(None, player, gameVariables)

    # Minimises window
    window.iconify()

    # Opens Manchester Blackboard on default browser
    webbrowser.open("https://www.manchester.ac.uk/")

def endDialogue(window, canvas, gameVariables, npc):

    '''Ends npc dialogue'''

    if gameVariables.getDialogueLabel():
        canvas.delete(gameVariables.getDialogueLabel())
    
    gameVariables.setDialogueLabel(None)
    gameVariables.setDialogueActive(False)
    npc.setDialogueActive(False)

    # Player can only talk once to the old bird
    gameVariables.setAllowDialogue(False)

    # Adds door to the scene
    door = Door(window, canvas, gameVariables)

    gameVariables.addToCoordinateArray([door.getX(), door.getY(), "door"])

def displayCurrentDialogue(canvas, npc, gameVariables, textArray):

    '''Displays npc dialogue on canvas'''

    # If not None, delete current dialogue label
    if gameVariables.getDialogueLabel():
        canvas.delete(gameVariables.getDialogueLabel())
    
    currentText = textArray[gameVariables.getDialogueIndex()]
    gameVariables.setDialogueLabel(canvas.create_text(
        npc.getX(), npc.getY() - 64,
        text=currentText, font=("Arial", 16), fill="white"
    ))

def loadGame(gameVariables, savedGame, startingArea, doorFlag):

    '''Special message for when the game is loaded'''

    gameVariables.setScore(savedGame["score"])
    gameVariables.setHighestScore(savedGame["highestScore"])

    # Only set to None once the player has entered the door
    if doorFlag:
        # No longer a saved game after this
        startingArea.setSavedGameToNone()

# Player varialbe needs to be used for death counter later!
def iterateNpcDialoague(window, canvas, npc, player, gameVariables, textArray, savedGame, startingArea):

    '''Lets the npc speak over multiple lines'''

    if not gameVariables.getAllowDialogue():
        return
    
    # Will load save file
    if savedGame != None:
        loadGame(gameVariables, savedGame, startingArea, False)
    
    if gameVariables.getDialogueActive() == False:
        
        gameVariables.setDialogueActive(True)
        npc.setDialogueActive(True)

        # This will count how far we're into the dialogue
        gameVariables.setDialogueIndex(0)

        displayCurrentDialogue(canvas, npc, gameVariables, textArray)
    
    elif gameVariables.getDialogueIndex() < len(textArray) - 1:

        gameVariables.setDialogueIndex(gameVariables.getDialogueIndex() + 1)
        displayCurrentDialogue(canvas, npc, gameVariables, textArray)

    else:
        endDialogue(window, canvas, gameVariables, npc)

def enterDoor(window, canvas, gameVariables, player, npc, doorX, doorY, projectileManager, pauseMenu, playerDeath, savedGame, startingArea):

    '''Allows the user to start the actual game once entered'''

    # Removes NPC and Door from the scene
    gameVariables.removeFromCoordinateArray([npc.getX(), npc.getY(), "npc"])
    gameVariables.removeFromCoordinateArray([doorX, doorY, "door"])

    # Will delete every image with the "MainMenu" tag
    canvas.delete("MainMenu")

    # Removes dialogue from screen if player didn't close it
    if gameVariables.getDialogueActive():
        endDialogue(window, canvas, gameVariables, npc)

    # Will move the player 3 to the left and 3 down
    player.move(-3, 3)

    if savedGame != None:
        loadGame(gameVariables, savedGame, startingArea, True)

    enemyManager = EnemyManager(window, canvas, gameVariables, projectileManager, pauseMenu, savedGame)

    # Sets enemy manager to classes that need it
    pauseMenu.setEnemyManager(enemyManager)
    playerDeath.setEnemyManager(enemyManager)
    
    enemyManager.spawnEnemies()

def interact(event, window, player, object, canvas, coordinateArray, gameVariables, controls, projectileManager, pauseMenu, playerDeath, savedGame, startingArea):

    '''Checks if the user has interacted with anything'''

    # Will iterate through each array of the coordinate array
    for array in coordinateArray:
        
        if player.getX() == array[0] and player.getY() == array[1] and array[2] == "door":
            
            doorX = array[0]
            doorY = array[1]
            enterDoor(window, canvas, gameVariables, player, object, doorX, doorY, projectileManager, pauseMenu, playerDeath, savedGame, startingArea)
            return
        
        # This checks if the player's coordinates are directly adjacent to the NPC coordinates
        # If player is on the same x, but 1 above or below the npc, interact
        # If player is on the same y, but 1 to the left or right of the npc, interact
        if ((array[0] == player.getX() and array[1] in (player.getY() + 64, player.getY() - 64)) or 
        (array[1] == player.getY() and array[0] in (player.getX() + 64, player.getX() - 64))) and array[2] == "npc":
            
            if savedGame != None:
                textArray = object.npcDialogueSaved(player.getDeathCounter(), player.getHealth())
            else:
                textArray = object.npcDialogue(player.getDeathCounter())

            canvas.bind(f"<{controls['interact']}>", lambda event: iterateNpcDialoague(window, canvas, object, player, gameVariables, textArray, savedGame, startingArea))

            iterateNpcDialoague(window, canvas, object, player, gameVariables, textArray, savedGame, startingArea)
            return

# These will determine which way the projectile goes when the player or enemy shoots
def shootProjectileLeft(event, canvas, player, projectileManager):

    '''Shoots a projectile left'''

    direction = [-1, 0]

    # False because it will always be the player that calls this method
    projectileManager.createProjectile(player, direction, "left", False)

def shootProjectileRight(event, canvas, player, projectileManager):
    
    '''Shoots a projectile right'''
    
    direction = [1, 0]

    projectileManager.createProjectile(player, direction, "right", False)

def shootProjectileUp(event, canvas, player, projectileManager):
    
    '''Shoots a projectile up'''
    
    direction = [0, -1]

    projectileManager.createProjectile(player, direction, "up", False)

def shootProjectileDown(event, canvas, player, projectileManager):
    
    '''Shoots a projectile down'''
    
    direction = [0, 1]

    projectileManager.createProjectile(player, direction, "down", False)