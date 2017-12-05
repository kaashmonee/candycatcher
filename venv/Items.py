import random
from tkinter import *

class Fruit:
    # fruit class for the game

    def __init__(self, imagePath, x=0, y=0):
        # initializing the fruit image and the path of the fruit
        self.imagePath = imagePath

        # initializing the fruit width and height
        self.width, self.height = 100, 100

        # initializing starting x and y values
        self.x, self.y = x, y

        # initializing x and y values
        self.vx = random.randint(2, 10)
        self.vy = random.randint(-50, 50)

    def drawFruit(self, canvas):
        # getting the image from the path and drawing the image.
        self.image = PhotoImage(file = self.imagePath)
        self.image = self.image.subsample(30, 30)
        canvas.create_image(self.x, self.y, image=self.image, anchor=NW)



