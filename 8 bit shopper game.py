"""
Created on Wed Nov  30 13:44:12 2023

@author: dluen
created the shopper, store, and grocery item on piskelapp.com
item pickup sound- https://opengameart.org/content/pick-up-item-yo-frankie
"""
import pygame
import simpleGE
import random


class GroceryItem(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.reset()
        self.setImage("grocery_item.png")
        self.setSize(25, 25)

    def reset(self):
        newX = random.randint(0, 640)
        newY = random.randint(0, 480)
        self.setPosition((newX, newY))

class Shopper(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("shopper.png")
        self.setSize(50, 50)
        self.coinSound = simpleGE.Sound("sfx_pick.flac")
        self.setPosition((50, 50))
        self.rotation_speed = 10
        self.move_speed = 3

    def checkKeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turnBy(self.rotation_speed)
        elif keys[pygame.K_RIGHT]:
            self.turnBy(-self.rotation_speed)
        if keys[pygame.K_DOWN]: 
            self.forward(-self.move_speed)
        elif keys[pygame.K_UP]:
            self.forward(self.move_speed)

    
        scrWidth = self.screen.get_width()
        scrHeight = self.screen.get_height()
        
    
        self.x = max(0, min(self.x, scrWidth - self.rect.width + 50))
        self.y = max(0, min(self.y, scrHeight - self.rect.height + 50))

    def checkCollision(self):
        for item in self.scene.grocery_items:
            if self.collidesWith(item):
                self.scene.score += 1
                self.scene.lblScore.text = f"Score: {self.scene.score}"
                self.coinSound.play()
                item.reset()

    def checkTime(self):
        time = self.scene.timer.getElapsedTime()
        if time > self.scene.MAXTIME:
            self.scene.btnQuit.show((300, 200))
            self.move_speed = 0
        else:
            timeLeft = self.scene.MAXTIME - time
            self.scene.lblTimer.text = f"time left: {timeLeft:.2f}"

    def checkEvents(self):
        self.checkTime()
        self.checkKeys()
        self.checkCollision()
        if self.scene.btnQuit.clicked:
            self.scene.stop()

def main():
    pygame.mixer.init()
    scene = simpleGE.Scene()

    background_image = pygame.image.load("grocery.png")
    scene.background = pygame.transform.scale(background_image, (640, 480))

    scene.setCaption("8 bit shopping game")

    scene.shopper = Shopper(scene)
    scene.grocery_items = [GroceryItem(scene) for _ in range(20)]

    scene.lblTimer = simpleGE.Label()
    scene.lblTimer.center = (100, 30)

    scene.lblScore = simpleGE.Label()
    scene.lblScore.center = (550, 30)
    scene.lblScore.text = "Score: 0"

    scene.btnQuit = simpleGE.Button()
    scene.btnQuit.text = 'Quit'
    scene.btnQuit.hide()

    scene.btnPause = simpleGE.Button()
    scene.btnPause.text = 'Pause'
    scene.btnPause.hide()

    scene.sprites = [scene.lblTimer, scene.lblScore, scene.shopper, scene.btnQuit, scene.btnPause] + scene.grocery_items

    scene.score = 0
    scene.timer = simpleGE.Timer()
    scene.MAXTIME = 30

    scene.start()

if __name__ == "__main__":
    main()
