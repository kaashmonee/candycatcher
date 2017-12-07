# events-example0.py
# Barebones timer, mouse, and keyboard events
# Barebones tkinter animation starter code taken from 112 website

from tkinter import *
from Items import Fruit, MouthCircle
import random
import os
import numpy as np
import cv2
import sys
import dlib
import time
import imutils
from imutils.video import VideoStream
from imutils import face_utils
import mathematics as mat
# from tkinter import PhotoImage


####################################
# customize these functions
####################################

def init(data):
    # image paths for all the items
    data.pathDicts = {"apple": "./assets/apple.png"}
    # dictionary for different colors and their hex values
    data.colors = {"cyan": "#00FFFF", "purple": "#6206d0",
                   "yellow": "#f0ff2e"}
    
    # 60 seconds in a game
    data.timeLeft = 60
    data.score = 0
    

    # list of all the fruits
    data.fruits = []
    data.livesPerLevel = {0: 10, 1: 7, 2: 5, 3: 2}

    # level
    data.level = 0
    # the frequency of the fruit changes with the level


    # frequency at which fruits come up given level
    data.levelFruitFrequency = {0: 3000, 1: 4000, 2: 3000, 3: 1000}
    data.mode = "splashScreen"
    data.score = 0
    data.timePassed = 0
    # initializing gravity
    data.g = 9.8


    # this list keeps track of all the points that are in the mouth
    data.facePoints = []
    data.mouthPoints = []
    data.mouthCircle = MouthCircle(0, 0, 0)
    # data.mouthOpen = False

    # delta t
    data.dt = 0.4


    # milliseconds elapsed
    data.milliElapsed = 0
    

    # scale factor (how much we want the facial features on the canvas blown up)
    data.scaleFactor = 4

    # time to wait before shooting next fruit
    data.timeBeforeNextFruit = data.levelFruitFrequency[data.level]
    # data.fruits.append(Fruit("apple", data.height + 50, random.r))



    # VIDEO STUFF
    # getting the video capture element from opencv


    # data.capture = cv2.VideoCapture(0)
    data.videoStream = VideoStream(0).start()
    data.sizeOfCapture = 200


    # initializing the dlib facial feature tracker
    data.detector = dlib.get_frontal_face_detector()
    
    LANDMARKS_CLASSIFIER = "./assets/shape_predictor_68_face_landmarks.dat"
    data.predictor = dlib.shape_predictor(LANDMARKS_CLASSIFIER)


def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == "splashScreen":
        splashScreenMousePressed(event, data)
    if data.mode == "playGame":
        playGameMousePressed(event, data)
    if data.mode == "gameOver":
        gameOverMousePressed(event, data)
    if data.mode == "helpScreen":
        helpScreenMousePressed(event, data)


def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "splashScreen":
        splashScreenKeyPressed(event, data)
    if data.mode == "playGame":
        playGameKeyPressed(event, data)
    if data.mode == "gameOver":
        gameOverKeyPressed(event, data)
    if data.mode == "helpScreen":
        helpScreenKeyPressed(event, data)
    pass


def timerFired(data):
    if data.mode == "splashScreen":
        splashScreenTimerFired(data)
    if data.mode == "playGame":
        playGameTimerFired(data)
    if data.mode == "gameOver":
        gameOverTimerFired(data)
    if data.mode == "helpScreen":
        helpScreenTimerFired(data)


def redrawAll(canvas, data):
    if data.mode == "splashScreen":
        splashScreenRedrawAll(canvas, data)
    if data.mode == "playGame":
        playGameRedrawAll(canvas, data)
    if data.mode == "gameOver":
        gameOverRedrawAll(canvas, data)
    if data.mode == "helpScreen":
        helpScreenRedrawAll(canvas, data)


##################################
# Splash screen mode
##################################
def splashScreenMousePressed(event, data):
    pass


def splashScreenKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "playGame"
    if event.keysym == "h":
        data.mode = "helpScreen"


def splashScreenTimerFired(data):
    getAndDrawCameraFeed(data)
    # playGameTimerFired(data)


def splashScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    data.image = PhotoImage(file="./assets/welcometext.png")
    print("getting here")
    # downsizes the image
    data.image = data.image.subsample(2, 1)
    # print(data.image)
    canvas.create_image(data.width/2, 100, image = data.image)
    print("getting here...create_image not working")
    # creating the help and start menu
    buttonYVal = data.height-data.height/3
    canvas.create_rectangle(0, buttonYVal, data.width/2, 
                            data.height, fill=data.colors["purple"])
    canvas.create_rectangle(data.width/2, buttonYVal, 
                            data.width, data.height, fill=data.colors["yellow"])
    # play game label
    canvas.create_text(data.width//4, buttonYVal+data.height/6,
                       fill="black", text="Play Game", anchor=CENTER,
                       font="Times 30")
    canvas.create_text(3 * data.width//4, buttonYVal+data.height/6,
                       fill="black", text="Help", anchor=CENTER,
                       font="Times 30")
    # playGameTimerFired(data)
    playGameRedrawAll(canvas, data)
    


##################################
# Play game mode
##################################

def playGameMousePressed(event, data):
    pass


def playGameKeyPressed(event, data):
    pass


def playGameTimerFired(data):

    if data.gameMode == "classic":
        # with lives and shit classic game mode here
        pass


    elif data.gameMode == "timeTrial":
        data.milliElapsed += data.timerDelay
        # print(data.milliElapsed)
        if data.milliElapsed % 500 == 0:
            if data.timeLeft > 0:
                data.timeLeft -= 1
            else:
                data.mode = "gameOver"

    # making items fall w/gravity
    for fruit in data.fruits:

        # sys.exit()
        # this works because i'm changing the actual fruit object
        dvy = data.g * data.dt
        fruit.vy += dvy
        dy = fruit.vy * data.dt
        dx = fruit.vx * data.dt
        # sys.exit(0)
        print("fuck me")
        # sys.exit(0)
        fruit.y += dy
        fruit.x += dx
        # sys.exit(0)

        # DETECT COLLISSION between mouth and fruit
        # if there is a collission, remove the fruit
        # if (mat.distance(fruit.x, fruit.y, data.mouthCircle.x,
        #                  data.mouthCircle.y) < data.mouthCircle.radius):

        #     data.fruits.pop(data.fruits.index(fruit))


        # print("fruit x:", fruit.x, "fruit y:", fruit.y)
        # print("GETTING HERE")
        # sys.exit(0)


        # for each fruit, checking if the fruit is in the mouth

        # if the fruit is outside the window and its trajectory is moving 
        # further away, then simply eliminate it
        if fruit.y > data.height and fruit.vy > 0:
            data.score -= 3
            data.fruits.pop(data.fruits.index(fruit))
        if fruit.x < 0 and fruit.vx < 0:
            data.score -= 3
            data.fruits.pop(data.fruits.index(fruit))
        if fruit.x > data.width and fruit.vx > 0:
            data.score -= 3
            data.fruits.pop(data.fruits.index(fruit))

    # after this many milliseconds, create another fruit
    if data.timeBeforeNextFruit <= 0:
        # randomly picking a color and item
        data.fruits.append(Fruit("apple",
                           color=data.colors[random.choice(list(data.colors))]))
        # randomly creates the next location of when it should go up
        data.timeBeforeNextFruit = random.randint(0, data.levelFruitFrequency[data.level])


    print("time before next fruit", data.timeBeforeNextFruit)
    data.timeBeforeNextFruit -= 10

    
    getAndDrawCameraFeed(data)

    for fruit in data.fruits:
        def checkIfInMouth(data):
            # print(data.facePoints)
            # print(len(data.facePoints))
            if (len(data.facePoints)):
                print("Getting here fine")
                # sys.exit(0)
                if MouthCircle.isFruitInMouth(data.facePoints, fruit, data.mouthOpen):
                    print("This collission happens!")
                    # sys.exit(0)
                    # break
                    data.score += 5
                    data.fruits.pop(data.fruits.index(fruit))

        checkIfInMouth(data)

    # creating the text for the score
    print(data.fruits)







def getAndDrawCameraFeed(data):
        # SHOWING THE VIDEO FEED (WORKS)
    # ret, frame = data.capture.read()
    # reading from video stream -- makes things faster
    frame = data.videoStream.read()
    frame = cv2.flip(frame, 1)
    frame=imutils.resize(frame, width=data.sizeOfCapture)
    # print("frame:", frame)

    # cv2.imshow("frame", frame)
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     sys.exit(0)




    # GETTING DLIB FACIAL FEATURES
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detecting faces
    rects=data.detector(gray, 0)
    # for each rectangle in rects, get facial landmarks and locations
    for rect in rects:
        # detect facial landmarks and convert to numpy array
        shape=data.predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        # loop over and draw on image
        for ind, (x, y) in enumerate(shape):
            # cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            # if it is a mouth point, then append to list
            # if ind in range(49, 69):
            data.facePoints.append((x, y))
    

    # make sure there is actually a face on the canvas
    if len(data.facePoints) != 0:
        # print("data.facepoitns length", len(data.facePoints))
        if MouthCircle.isMouthOpen(data.facePoints):
            print("Mouth is open!")
            data.mouthOpen = True
            # sys.exit(0)
        else:
            data.mouthOpen = False
            # sys.exit(0)


    # cv2.imshow("Frame", frame)
    key=cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        sys.exit(0)


def makeBoundingCircle(data):
    for (x, y) in data.mouthPoints:
        pass






def playGameRedrawAll(canvas, data):
    if data.mode == "playGame":
        canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
        # draw in canvas
        # print("data.fruit", data.fruit)
        # just testing to see that the canvas was working
        canvas.create_text(5, 10, text="Time left: "+str(data.timeLeft), 
                        fill="white", font="Times 14", anchor=NW)
        canvas.create_text(data.width - 5, 10, text="Score: "+str(data.score), 
                        fill="white", font="Times 14", anchor=NE)

    # draw all the fruits
    for fruit in data.fruits:
        fruit.drawFruit(canvas)


    # drawing the mouth points on the canvas (in this case, it might not even
    # be more than just the mouth points)
    for (x, y) in data.facePoints:
        # print("data.mouthPoints redraw all", data.mouthPoints)
        # time.sleep(1)
        fill = "red"
        # if it's the mouth, color it blue
        # print("mouth points", data.mouthPoints)
        if (x, y) in data.mouthPoints:
            fill = "blue"
        canvas.create_oval(data.scaleFactor*x, data.scaleFactor*y, 
                           data.scaleFactor*x+5, data.scaleFactor*y+5, 
                           fill=fill)
        data.facePoints = []
        data.mouthPoints = []

    # creating text to update the score
    canvas.create_text(10, 10, fill="black", font="Times 20 italic bold",
                       text="Score: " + str(data.score), anchor=NW)


#################################
# Game over mode
#################################
def gameOverKeyPressed(event, data):
    pass


def gameOverMousePressed(event, data):
    pass


def gameOverTimerFired( data):
    pass


def gameOverRedrawAll(canvas, data):
    pass






###################################
# Help Screen mode
###################################
def helpScreenKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "playGame"


def helpScreenMousePressed(event, data):
    pass


def helpScreenTimerFired(data):
    pass


def helpScreenRedrawAll(canvas, data):
    label = """
Welcome to fruiteater! The objective of this game is simple: try to catch as
many fruits as you can within the given time limit!

Press 'p' to get started!"""
    # background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")

    canvas.create_text(data.width / 2, data.height / 2, text=label, 
                       fill=data.colors["purple"], 
                       font="Times 17")






####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    # print(os.getcwd())
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10  # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    # setting background
    root.configure(background="black")
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(700, 700)
