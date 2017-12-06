import random
from tkinter import *
import mathematics as mat

class Fruit:
    # fruit class for the game

    # fruit dictionary
    FRUIT_DICT = {"apple": "./assets/apple.png", "orange": "./assets/orange.png",
                  "mango": "./assets/mango.png", "grape": "./assets/grape.png",
                  }

    def __init__(self, fruit, x=0, y=750, color="red"):
        # random x value for x
        x = random.randint(0, 400)
        self.color = color

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
        canvas.create_oval(self.x, self.y, self.x+self.width, 
                           self.y+self.height, fill=self.color)


    def getHashables(self):
        return (self.imagePath, self.x, self.y, self.vx, self.vy)

    def __hash__(self):
        return hash(self.getHashables())



# is the circle that bounds the mouth
# class with all things to do with the circle around the mouth and mouth
# related things in general
class MouthCircle:

    # tweaking this variable will allow the user to change the amount the user
    # needs to open their mouth to be detected as an open mouth
    # the greater this number, the wider the mouth needs to be opened
    MOUTH_OPEN_MIN_RATIO = 0.35

    def __init__(self, centerx, centery, radius):
        self.x = centerx
        self.y = centery
        self.radius = radius

    def draw(self, canvas):
        canvas.create_oval(self.x, self.y, self.x + self.radius,
                           self.y + self.radius, fill="red")

    @staticmethod
    def isMouthOpen(facePoints):
        # determing if the mouthis open or not.
        # will calculate average distance between top and bottom poitns of mouth
        # if the ratio is closer to 0, then mouth is closed
        # if not, then mouth is open
        leftCorner = facePoints[60]
        rightCorner = facePoints[64]
        horizontalDistance = mat.distance(leftCorner[0], leftCorner[1],
                                          rightCorner[0], rightCorner[1])
        
        # dictionary -- maps each point to point right across from it. 
        # only looks at bottom part of upper lip
        pointsAcross = {61: 67, 62: 66, 63: 65}
        
        average = 0
        for key, val in pointsAcross.items():
            point1 = facePoints[key]
            # print("Val", val)
            point2 = facePoints[val]

            # calculates distance between 2 points
            distance = mat.distance(point1[0], point1[1], point2[0], point2[1])
            average += distance

        average /= len(pointsAcross)

        ratio = average / horizontalDistance

        if ratio < MouthCircle.MOUTH_OPEN_MIN_RATIO:
            return False
        else:
            return True





