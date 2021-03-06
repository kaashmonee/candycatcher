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

###NEED GLOBAL VARIABLE SO AS TO AVOID RESTARTING THE VIDEO STREAM OVER AND 
# OVER AGAIN.

# VIDEO_STREAM = VideoStream(0).start()

def init(data):
    # image paths for all the items
    data.pathDicts = {"apple": "./assets/apple.png"}
    # dictionary for different colors and their hex values
    data.colors = {"cyan": "#00FFFF", "purple": "#6206d0",
                   "yellow": "#f0ff2e", "orange": "#FF6600",
                   "red": "#ff0000", "green": "#00ff00"}
    
    # 60 seconds in a game
    data.timeLeft = 60
    data.score = 0
    

    # list of all the fruits
    data.fruits = []
    data.livesPerLevel = {0: 10, 1: 7, 2: 5, 3: 2}

    # level
    data.level = 3
    # the frequency of the fruit changes with the level


    # frequency at which fruits come up given level
    data.levelFruitFrequency = {0: 3000, 1: 4000, 2: 3000, 3: 1000}
    data.mode = "splashScreen"
    data.score = 0
    data.timePassed = 0
    data.lives = 7
    # initializing gravity
    data.g = 9.8


    # this list keeps track of all the points that are in the mouth
    data.facePoints = []
    data.mouthPoints = []
    data.mouthCircle = MouthCircle(0, 0, 0)
    # data.mouthOpen = False

    # delta t
    data.dt = 0.4
    data.gameMode = "timeTrial"
    data.timesFired = 0


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
    # data.videoStream = VideoStream(0).start()
    data.sizeOfCapture = 200


    # initializing the dlib facial feature tracker
    data.detector = dlib.get_frontal_face_detector()
    
    LANDMARKS_CLASSIFIER = "./assets/shape_predictor_68_face_landmarks.dat"
    data.predictor = dlib.shape_predictor(LANDMARKS_CLASSIFIER)


def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == "splashScreen":
        splashScreenMousePressed(event, data)
    elif data.mode == "playGame":
        playGameMousePressed(event, data)
    elif data.mode == "gameOver":
        gameOverMousePressed(event, data)
    elif data.mode == "helpScreen":
        helpScreenMousePressed(event, data)
    elif data.mode == "modeScreen":
        modeScreenMousePressed(event, data)


def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "splashScreen":
        splashScreenKeyPressed(event, data)
    elif data.mode == "playGame":
        playGameKeyPressed(event, data)
    elif data.mode == "gameOver":
        gameOverKeyPressed(event, data)
    elif data.mode == "helpScreen":
        helpScreenKeyPressed(event, data)
    elif data.mode == "modeScreen":
        modeScreenKeyPressed(event, data)


def timerFired(data):
    if data.mode == "splashScreen":
        splashScreenTimerFired(data)
    elif data.mode == "playGame":
        playGameTimerFired(data)
    elif data.mode == "gameOver":
        gameOverTimerFired(data)
    elif data.mode == "helpScreen":
        helpScreenTimerFired(data)
    elif data.mode == "modeScreen":
        modeScreenTimerFired(data)


def redrawAll(canvas, data):
    if data.mode == "splashScreen":
        splashScreenRedrawAll(canvas, data)
    elif data.mode == "playGame":
        playGameRedrawAll(canvas, data)
    elif data.mode == "gameOver":
        gameOverRedrawAll(canvas, data)
    elif data.mode == "helpScreen":
        helpScreenRedrawAll(canvas, data)
    elif data.mode == "modeScreen":
        modeScreenRedrawAll(canvas, data)


##################################
# Splash screen mode
##################################


def splashScreenMousePressed(event, data):
    pass


def splashScreenKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "modeScreen"
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
    # print("getting here...create_image not working")
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
        if data.lives < 0:
            data.mode = "gameOver"
        pass


    elif data.gameMode == "timeTrial":
        data.timesFired += 1
        # print(data.milliElapsed)
        if data.timesFired == 50:
            if data.timeLeft > 0:
                data.timeLeft -= 1
                data.timesFired = 0
            else:
                data.mode = "gameOver"

    # making items fall w/gravity
    for fruit in data.fruits:
        # updates the positions of all the fruits in the list
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

    # for now do the collission

    for fruitInd in range(len(data.fruits)):
        fruit
        if fruitInd in range(len(data.fruits)):
            fruit = data.fruits[fruitInd]
        if fruit.y > data.height and fruit.vy > 0:
            # dealing with separate cases if the fruit falls during time trial
            # and classic modes
            if data.gameMode == "timeTrial":
                data.score -= 3
            elif data.gameMode == "classic":
                if (fruit.color != "green" and fruit.color != data.colors["green"]
                    and fruit.color != "red" and fruit.color != data.colors["red"]):
                    data.lives -= 1
            if fruit in data.fruits:
                data.fruits.pop(data.fruits.index(fruit))
        if fruit.x <= 0:
            # data.score -= 3
            # data.fruits.pop(data.fruits.index(fruit))
            fruit.vx = -fruit.vx
        if fruit.x+2*fruit.radius >= data.width:
            # data.score -= 3
            # data.fruits.pop(data.fruits.index(fruit))
            fruit.vx = -fruit.vx
        else:
            for i in range(fruitInd+1, len(data.fruits)):
                fruit2 = data.fruits[i]
                if (mat.distance(fruit.x, fruit.y, fruit2.x, fruit2.y)
                    <= fruit.radius * 2):
                    doCollision(fruit, fruit2, data)

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

    checkIfInMouth(data)

    # creating the text for the score
    print(data.fruits)

def checkIfInMouth(data):
    for fruit in data.fruits:
        # print(data.facePoints)
            # print(len(data.facePoints))
            if (len(data.facePoints)):
                print("Getting here fine")
                # sys.exit(0)
                if MouthCircle.isFruitInMouth(data.facePoints, fruit, data.mouthOpen):
                    print("This collission happens!")
                    # sys.exit(0)
                    # break
                    if data.gameMode == "timeTrial":
                        data.score += 5
                    elif data.gameMode == "classic":
                        # red kills you faster, green can help revive you
                        if fruit.color == "red" or fruit.color == "#ff0000":
                            data.lives -= 1
                        elif fruit.color == "green" or fruit.color == "#00ff00":
                            data.lives += 1
                        # if it's neither a killer or helper, the score goes up
                        # by 5
                        else:
                            data.score += 5
                    data.fruits.pop(data.fruits.index(fruit))



def doCollision(fruit1, fruit2, data):
    collisionPointX = (fruit1.x + fruit2.x) / 2 # getting the collision point
    collisionPointY = (fruit1.y + fruit2.y) / 2 # same thing for yellow


    tempvx1 = fruit1.vx
    tempvy1 = fruit1.vy


    fruit1.vx = fruit2.vx
    fruit1.vy = fruit2.vy

    fruit2.vx = tempvx1
    fruit2.vy = tempvy1

    fruit1.x += fruit1.vx * data.dt
    fruit2.y += fruit2.vy * data.dt






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






def playGameRedrawAll(canvas, data):
    if data.mode == "playGame":
        # change behaviors for time trial mode vs. classic mode
        canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
        if data.gameMode == "timeTrial":
            # draw in canvas
            # print("data.fruit", data.fruit)
            # just testing to see that the canvas was working
            canvas.create_text(5, 30, text="Time left: "+str(data.timeLeft), 
                            fill="white", font="Times 14", anchor=NW)
            canvas.create_text(data.width - 5, 30, text="Score: "+str(data.score), 
                            fill="white", font="Times 14", anchor=NE)
        
        # classic mode behavior
        elif data.gameMode == "classic":
            canvas.create_text(5, 30, text="Lives " + str(data.lives),
                               fill="white", font="Times 14", anchor=NW)

            canvas.create_text(data.width - 5, 30, text="Score: " + str(data.score),
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
    # canvas.create_text(10, 10, fill="white", font="Times 20 italic bold",
    #                    text="Score: " + str(data.score), anchor=NW)


#################################
# Game over mode
#################################
def gameOverKeyPressed(event, data):
    if event.keysym == "p":
        init(data)
    elif event.keysym == "q":
        sys.exit(0)


def gameOverMousePressed(event, data):
    pass


def gameOverTimerFired( data):
    pass


def gameOverRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    canvas.create_text(data.width/2, 20, text="Game Over", font="Times 40", 
                       fill="white")
    canvas.create_text(data.width/2, 120, text="Your score is: "+str(data.score), 
                       font="Times 40", fill="red")

    canvas.create_text(data.width/2, 250, text="Please press 'p' to play again, or 'q' to quit.", 
                       font="Times 30", fill="white", anchor=CENTER)






###################################
# Help Screen mode
###################################
def helpScreenKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "modeScreen"
        print("data.mode: ", data.mode)


def helpScreenMousePressed(event, data):
    pass


def helpScreenTimerFired(data):
    pass


def helpScreenRedrawAll(canvas, data):
    label = """
Welcome to CandyCatcher! You can choose between two modes: Classic, and Time Trials.
In classic mode, the objective is to try to get as many points as possible before
the number of lives run out. You start with 7 lives. But watch out for red colored candy!
If you eat red candy, or drop a candy, you will lose a life. 
But, if you eat green candy, you will gain a life. 
If you drop candy, you will also lose a life. 

In Time Trials, you will have around 60 or so seconds to catch as much candy
as you can. 5 points are awarded for catching candy, and 3 points are deducted
for dropping candy. 

Beware, candy behave like physical balls! They bounce off of walls and each other!

Press 'p' to get started!"""
    # background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")

    canvas.create_text(data.width / 2, data.height / 2, text=label, 
                       fill=data.colors["red"], 
                       font="Times 14")







####################################
# Mode Screen
####################################

def modeScreenKeyPressed(event, data):
    # sets the type of game the user will play
    if event.keysym == "c":
        data.gameMode = "classic"
    elif event.keysym == "t":
        data.gameMode = "timeTrial"
    

    # overall game mode
    data.mode = "playGame"


def modeScreenMousePressed(event, data):
    pass


def modeScreenTimerFired(data):
    # print("Fucking getting here")
    pass


def modeScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width/2, data.height, 
                       fill=data.colors["purple"])

    canvas.create_rectangle(data.width/2, 0, data.width, data.height, 
                       fill=data.colors["orange"])

    canvas.create_text(3*data.width/4, data.height/2, fill="white", 
                       text="'T' for Time Trial", font="Times 30")

    canvas.create_text(data.width/4, data.height/2, fill="white", 
                       text="'C' for Classic", font="Times 30")









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
    data.videoStream = VideoStream(0).start()
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
