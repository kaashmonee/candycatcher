import random
from tkinter import *
import mathematics as mat
import time

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
        # print(facePoints)
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

    @staticmethod
    def isFruitInMouth(facePoints, fruit, isMouthOpen):
        print("This method is at least being called")
        # sys.exit(0)
        # determines if a fruit has collided with the user's mouth
        # basically, i want to check if the center of the fruit is within the 
        # bounding rectangle of the person's open mouth. But first and foremost
        # it needs to ensure that the mouth is open, so we will start with that.

        # isMouthOpen = MouthCircle.isMouthOpen(facePoints)
        # if the mouth is not open, then there are no collissions possible
        print("is mouth open", isMouthOpen)
        # time.sleep(0.01)
        if not isMouthOpen: 
            return False
        else:
            # getting bounding box of open mouth region
            # starting point will be the point at the 61st index
            # ending point will the point at the 65th index
            # startX = facePoints[49][0]
            # startY = facePoints[49][1]
            # endX = facePoints[55][0]
            # endY = facePoints[55][1]

            # print("testing the starting and ending values", startX, startY, endX, endY); time.sleep(1)

            # rect = Rectangle(startX, startY, endX, endY)
            # # creates a rectangle
            # # if the point is in the rectangle, then return True
            # # otherwise, return false
            # if rect.pointInRectangle(fruit.x, fruit.y):
            #     return True
            # else:
            #     return False

            # going to create a circle around the mouth and hopefully that 
            # will work

            # create a circle with diamter left most point to the right most point
            # top left corner is 
            # y-value of 50, xvalue of 48, diamater of 48-54
            print("GETING TO THE ELSE")
            # THIS PART IS WHERE IT FUCKS UP
            x = facePoints[48][0] * 4 # blowing it up by the scale factor! I think this will work...
            y = facePoints[50][1] * 4 # same deal
            print("x", x, "y", y)
            radius = mat.distance(facePoints[48][0] * 4, facePoints[48][1] * 4,
                                  facePoints[54][0] * 4, facePoints[54][1] * 4) / 2
            centerX = x+radius
            centerY = y+radius - 100

            print("radius", radius, "distance", mat.distance(fruit.x, fruit.y, centerX, centerY))
            if mat.distance(fruit.x, fruit.y, centerX, centerY) <= radius * 1.5:
                return True
            else:
                return False

class Rectangle:

    def __init__(self, startX, startY, endX, endY):
        self.x1 = startX
        self.y1 = startY
        self.x2 = endX
        self.y2 = endY
        self.centerX = (startX + endX) / 2
        self.centerY = (startY + endY) / 2
 
    def pointInRectangle(self, x, y):
        # if x value is greater than the starting x value and the y value
        # is greater than the starting y value, but both are less than their
        # respective ending values
        if (x >= self.x1 and x <= self.x2 and 
            y >= self.y1 and y <= self.y2):
            return True
        else:
            return False

# mouth class to discuss dimensions and locations of mouth
# it's basically a rectangle









