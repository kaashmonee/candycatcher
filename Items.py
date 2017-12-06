import random
from tkinter import *

class Fruit:
    # fruit class for the game

    # fruit dictionary
    FRUIT_DICT = {"apple": "./assets/apple.png", "orange": "./assets/orange.png",
                  "mango": "./assets/mango.png", "grape": "./assets/grape.png",
                  }

    def __init__(self, fruit, x=0, y=750):
        # random x value for x
        x = random.randint(0, 400)

        # initializing the fruit image and the path of the fruit
        self.imagePath = Fruit.FRUIT_DICT[fruit]

        # initializing the fruit width and height
        self.width, self.height = 100, 100

        # initializing starting x and y values
        self.x, self.y = x, y

        # initializing x and y values
        self.vx = random.randint(-20, 20)
        self.vy = -100

    def drawFruit(self, canvas):
        # getting the image from the path and drawing the image.
        """
        self.image = PhotoImage(file = self.imagePath)
        self.image = self.image.subsample(30, 30)
        canvas.create_image(self.x, self.y, image=self.image, anchor=NW)

        :param canvas:
        :return:
        """
        canvas.create_oval(self.x, self.y, self.x+self.width, self.y+self.height, fill="red")


    def getHashables(self):
        return (self.imagePath, self.x, self.y, self.vx, self.vy)

    def __hash__(self):
        return hash(self.getHashables())



# is the circle that bounds the mouth
class MouthCircle:

    def __init__(self, centerx, centery, radius):
        self.x = centerx
        self.y = centery
        self.radius = radius

    def draw(self, canvas):
        canvas.create_oval(self.x, self.y, self.x + self.radius,
                           self.y + self.radius, fill="red")




