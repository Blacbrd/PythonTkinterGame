from enemy import Enemy

class EnemyManager:

    '''Manages enemies, such as how many should spawn and where they should spawn'''

    def __init__(self, window, canvas, gameVariables, projectileManager, pauseMenu, savedGame):
        
        self.window = window
        self.canvas = canvas
        self.gameVariables = gameVariables
        self.projectileManager = projectileManager
        self.pauseMenu = pauseMenu
        self.savedGame = savedGame
        
        self.paused = False
        self.enemyArray = []

        # Takes into account how many enemies there are on the screen. If there's less than a certain amount, spawn new enemy
        self.enemyCount = 0

        # Maximum amount of enemies
        self.maximumEnemyCount = 1

        # Tracks how many enemies have been killed
        self.enemiesKilled = 1

        # This tells the enemy manager to stop shooting projectiles
        self.stop = False

        # If there is a saved game, load the correct amount of enemies
        if self.savedGame != None:
            self.enemiesKilled = self.gameVariables.getScore()
            
            # sets the amount of enemies accordingly
            if self.enemiesKilled >= 100:
                self.maximumEnemyCount = 16
            elif self.enemiesKilled >= 64:
                self.maximumEnemyCount = 12
            elif self.enemiesKilled >= 48:
                self.maximumEnemyCount = 10
            elif self.enemiesKilled >= 32:
                self.maximumEnemyCount = 5
            elif self.enemiesKilled >= 20:
                self.gameVariables.setDifficulty("hard")
                self.maximumEnemyCount = 4
            elif self.enemiesKilled >= 16:
                self.maximumEnemyCount = 4
            elif self.enemiesKilled >= 7:
                self.gameVariables.setDifficulty("medium")
                self.maximumEnemyCount = 3
            elif self.enemiesKilled >= 3:
                self.maximumEnemyCount = 2
            
            self.savedGame = None

        self.enemyShootManager()

    def setStop(self, boolean):

        '''If stoop, enemy doesn't shoot'''

        self.stop = boolean

    def spawnEnemies(self):

        '''In charge of spawning enemies into the game'''
        
        while self.maximumEnemyCount > self.enemyCount:

            enemy = Enemy(self.window, self.canvas, self.gameVariables, self, self.projectileManager)
            self.enemyArray.append(enemy)

            self.enemyCount += 1
        
        if self.gameVariables.getHardMode():
            self.maximumEnemyCount = 16
            return

        # This checks if the player has killed a certain amount of enemies
        # If they have, increase the difficulty by adding an extra enemy
        # sets the amount of enemies accordingly
        if self.enemiesKilled >= 100:
            self.maximumEnemyCount = 16
        elif self.enemiesKilled >= 64:
            self.maximumEnemyCount = 12
        elif self.enemiesKilled >= 48:
            self.maximumEnemyCount = 10
        elif self.enemiesKilled >= 32:
            self.maximumEnemyCount = 5
        elif self.enemiesKilled >= 20:
            self.gameVariables.setDifficulty("hard")
            self.maximumEnemyCount = 4
        elif self.enemiesKilled >= 16:
            self.maximumEnemyCount = 4
        elif self.enemiesKilled >= 7:
            self.gameVariables.setDifficulty("medium")
            self.maximumEnemyCount = 3
        elif self.enemiesKilled >= 3:
            self.maximumEnemyCount = 2
    
    def incrementEnemiesKilled(self, enemy):

        '''Ups users score by 1 and enemies killed by 1'''

        self.enemiesKilled += 1
        self.gameVariables.incrementScore()
        self.enemyArray.remove(enemy)
    
    def decrementEnemyCount(self):

        '''If an enemy is defeated, count goes down by 1'''

        self.enemyCount -= 1
    
    def enemyShootManager(self):

        '''Enemy shoot manager'''

        if self.stop:
            return

        # If paused, freeze projectiles
        if self.pauseMenu.getIsPaused() or self.paused:
            self.paused = True
            return

        for enemy in self.enemyArray:
            enemy.enemyShoot()
        
        if self.gameVariables.getFastProjectile():
            time = 100
        else:
            time = 300
        
        self.canvas.after(time, self.enemyShootManager)
    
    def resume(self):

        '''Resumes game'''

        if self.paused:
            self.paused = False
            self.enemyShootManager()
    
    def removeAllEnemies(self):
        
        '''Remove the enemies'''

        for enemy in self.enemyArray:
            enemy.deleteEnemy()