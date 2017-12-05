# events-example0.py
# Barebones timer, mouse, and keyboard events
# Barebones tkinter animation starter code taken from 112 website

from tkinter import *
from Items import Fruit
import os

####################################
# customize these functions
####################################

def init(data):
    data.pathDicts = {"apple":"./assets/apple.png"}
    # load data.xyz as appropriate
    data.fruits = []
    data.mode = "splashScreen"
    data.score = 0
    # initializing gravity
    data.g = 9.8

    # time differential
    data.dt = 0.5


    # time to wait before shooting next fruit
    data.timeBeforeNextFruit = 1
    data.fruits.append(Fruit(data.pathDicts["apple"], 10, 10))





    pass



def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    # randomize the time before the next fruit here
    # data.fruits.append(Fruit())
    # print("vy:", fruit.vy)
    # dt = 0.5
    for fruit in data.fruits:
        dv = 9.8 * data.dt
        fruit.vy += dv
        dy = fruit.vy * data.dt
        fruit.y += dy

    pass

def redrawAll(canvas, data):
    # draw in canvas
    # print("data.fruit", data.fruit)
    canvas.create_rectangle(0, 0, 10, 10)
    for fruit in data.fruits: fruit.drawFruit(canvas)
    pass

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
    data.timerDelay = 2 # milliseconds
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

run(400, 200)