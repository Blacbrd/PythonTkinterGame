from projectile import Projectile

class ProjectileManager:

    def __init__(self, canvas, pauseMenu, gameVariables):

        self.canvas = canvas
        self.gameVariables = gameVariables
        self.pauseMenu = pauseMenu

        # Keeps track of how many projectiles are on the screen
        self.projectiles = []

        # Individual pause flag to allow for projectiles to fly once unpaused
        self.paused = False

        # This tells the projectile manager to stop moving all projectiles
        self.stop = False
    
    def setIsPaused(self, boolean):
        self.paused = boolean
    
    def setStop(self, boolean):
        self.stop = boolean

    def createProjectile(self, object, direction, directionString, enemyProjectile):

        projectile = Projectile(object, self.canvas, direction, directionString, enemyProjectile, self.gameVariables)

        # Adds projectile to array of currently active projectiles
        self.projectiles.append(projectile)
    
    def update(self):

        if self.stop:
            return

        # If paused, freeze projectiles
        if self.pauseMenu.getIsPaused() or self.paused:
            self.paused = True
            return

        # For every active projectile, move in specified direction
        for projectile in self.projectiles:

            if projectile.getIsActive():

                projectile.collision()
            
            # This is so that the array doesn't grow too large, makes the program more efficient
            if not projectile.getIsActive():

                self.projectiles.remove(projectile)
        
        # 16ms is about 60fps
        self.canvas.after(16, self.update)
    
    # If paused, resume projectile flying
    def resume(self):

        if self.paused:
            self.paused = False
            self.update()
    
    def deleteProjectiles(self):
        for projectile in self.projectiles:

            projectile.deleteProjectile(False, False, None)