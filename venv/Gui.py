# events-example0.py
# Barebones timer, mouse, and keyboard events
# Barebones tkinter animation starter code taken from 112 website

from tkinter import *
from Items import Fruit
import random
import os

####################################
# customize these functions
####################################

def init(data):
    data.pathDicts = {"apple":"./assets/apple.png"}
    # load data.xyz as appropriate
    data.fruits = []
    data.level = 0
    # the frequency of the fruit changes with the level
    data.levelFruitFrequency = {0: 3000, 1: 4000, 2: 3000, 3: 1000}
    data.mode = "splashScreen"
    data.score = 0
    data.timePassed = 0
    # initializing gravity
    data.g = 9.8

    # delta t
    data.dt = 0.2


    # time to wait before shooting next fruit
    data.timeBeforeNextFruit = data.levelFruitFrequency[data.level]
    # data.fruits.append(Fruit("apple", data.height + 50, random.r))





    pass



def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == "splashScreen":
        splashScreenMousePressed(event, data)
    if data.mode == "playGame":
        playGameMousePressed(event, data)
    if data.mode == "gameOver":
        gameOverMousePressed(event, data)

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "splashScreen":
        splashScreenKeyPressed(event, data)
    if data.mode == "playGame":
        playGameKeyPressed(event, data)
    if data.mode == "gameOver":
        gameOverMousePressed(event, data)
    pass

def timerFired(data):
    if data.mode == "splashScreen":
        splashScreenTimerFired(data)
    if data.mode == "playGame":
        playGameTimerFired(data)
    if data.mode == "gameOver":
        gameOverTimerFired(data)


def playGameTimerFired(data):
    # randomize the time before the next fruit here

    # making items fall w/gravity
    for fruit in data.fruits:
        # this works because i'm changing the actual fruit object
        dv = data.g * data.dt
        fruit.vy += dv
        dy = fruit.vy * data.dt
        fruit.y += dy
        print("fruit x:", fruit.x, "fruit y:", fruit.y)

        # if the fruit is below the window and the fruit is falling down, get rid
        # of the fruit
        if fruit.y > data.height and fruit.vy > 0:
            data.fruits.pop(data.fruits.index(fruit))

    # after this many milliseconds, create another fruit
    if data.timeBeforeNextFruit <= 0:
        data.fruits.append(Fruit("apple"))
        data.timeBeforeNextFruit = random.randint(0, data.levelFruitFrequency[data.level])

    print("time before next fruit", data.timeBeforeNextFruit)
    data.timeBeforeNextFruit -= 10

    # creating the text for the score




    print(data.fruits)

def redrawAll(canvas, data):
    # draw in canvas
    # print("data.fruit", data.fruit)
    # just testing to see that the canvas was working
    canvas.create_rectangle(0, 0, 10, 10)
    # draw all the fruits
    for fruit in data.fruits:
        fruit.drawFruit(canvas)


    # creating text to update the score
    canvas.create_text(10, 10, fill="black", font="Times 20 italic bold",
                       text="Score: " + str(data.score), anchor=NW)

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
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
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