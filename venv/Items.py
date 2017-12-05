import random
from tkinter import *

class Fruit:
    # fruit class for the game

    def __init__(self, imagePath):
        # initializing the fruit image and the path of the fruit
        self.imagePath = imagePath

        # initializing the fruit width and height
        self.width, self.height = 100, 100

        # initializing starting x and y values
        self.x, self.y = 0, 0

        # initializing x and y values
        self.vx = random.randint(2, 10)
        self.vy = random.randint(2, 10)

    def drawFruit(self, canvas):
        # getting the image from the path and drawing the image.
        image = PhotoImage(file = self.imagePath)
        canvas.create_image(self.x, self.y, image=image, anchor=NW)



