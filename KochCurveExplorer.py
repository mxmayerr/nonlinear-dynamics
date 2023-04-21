# visualizer for the koch curve and snowflake
# nonlinear dynamics, april 2023
# author: MCM '23

# ------------------ IMPORTS & GLOBALS ------------------
from random import randint
import sys
sys.path.append("../lib")
from DEgraphics import *
from math import *

global lines
lines = []

global p
p = Point(50,200)

font = "verdana"

# -------------------- FUNCTIONS --------------------

# function to draw a line secment from start point to length, with theta angle from x-axis
# also adhears to the color given, or random
def drawLine(startPt, theta, length, color, width = 2):
    global lines

    if color == "Random":
            color = color_rgb(randint(0,255), randint(0,255), randint(0,255))
    else:
        color = color.lower()

    xfinal = startPt.getX() + length * cos(radians(theta))
    yfinal = startPt.getY() + length * sin(radians(theta))
    endPoint = Point(xfinal, yfinal)

    lineSegment = Line(startPt, endPoint)
    lineSegment.setWidth(width)
    lineSegment.setFill(color)
    lineSegment.draw(mainWin)
    lines.append(lineSegment)
    startPt.move(xfinal-startPt.getX(), yfinal-startPt.getY())

# function to clear all the lines on the screen and reset global lines list
def clearLines():
    global lines

    for line in lines:
        line.undraw()
    lines = []

# funciton to reset the global point p for drawing
def resetPoint():
    global p

    p = Point(50,200)

# function to draw the koch curve recursively at the given level, koch angle, inclide angle, and total length
def drawKC(level, theta, inclineAngle, totalLength, color):
    # base case, if level is 0, draw a standard line
    if level == 0:
        drawLine(p, inclineAngle + theta, totalLength, color = color)
    # otherwise, decrement level and draw 4 koch curves at the given angles, but with length reletive to the level
    else:
        level-=1
        length = totalLength * 1 / (2 * (1 + cos(radians(theta))))
        drawKC(level, theta, inclineAngle, length, color)
        drawKC(level, theta, inclineAngle + theta, length, color)
        drawKC(level, theta, inclineAngle - theta, length, color)
        drawKC(level, theta, inclineAngle, length, color)


def drawKCColor(level, theta, inclineAngle, totalLength, colors):
    # in progress
    pass
 
def plot():
    # if introtext is shown, remove it
    if introText.isDrawn():
        introText.undraw()
    # start timer
    start = time.time()
    clearLines()
    # get values from user controls
    level = levelInput.getValue()
    theta = thetaInput.getValue() % 360
    type = typeInput.getChoice()
    color = colorInput.getChoice()   

    # if level is more than 7, draw leven 7 but calculate statistics for inputted level
    fakeLevel = level
    if level > 7:
        fakeLevel = 7

    # if type is koch curve, draw a koch curve
    if type == "Koch Curve":
        print (theta)
        drawKC(fakeLevel, theta, -60, 480, color)
    # if type is koch snowflake, draw a koch snowflake (3 curves)
    elif type == "Koch Snowflake":
        drawKC(fakeLevel, theta, 0, 350, color)
        drawKC(fakeLevel, theta, -120, 350, color)
        drawKC(fakeLevel, theta, -240, 350, color)
    
    # reset the point, end timer, update analytics
    resetPoint()
    end = time.time()
    updateAnalytics(end-start)

def updateAnalytics(t):
    # update the statistics with the current values
    level = levelInput.getValue()
    theta = thetaInput.getValue() % 360
    type = typeInput.getChoice()

    # calculate the curve length (level 0 is 1 unit)
    if type == "Koch Curve":
        length = (4 / 3) ** level
    elif type == "Koch Snowflake":
        length = 3 * (4 / 3) ** level
    
    # calculate the area under the curve, reletive to x axis
    area = 0
    for i in range(int(level)):
        area += (4 / 9) ** i
    area *= sqrt(3)/36

    # calculate number of lines reletive to the level
    lines = 4 ** level
    
    # update the text
    curveLength.setText("Curve Length: " + str(round(length, 3)) + " units") #type: ignore
    curveArea.setText("Area Under Curve: " + str(round(area, 3)) + " units"u"\u00B2")
    timeTaken.setText("Time taken: " + str(round(t, 3)) +  "seconds")
    numLines.setText("Number of Lines: " + str(round(lines, 3))) 




def editStartPoint():
    # Edits the start point global object and replots
    global p

    # clear the existing window
    clearLines()

    # display the instructions in the middle
    middleX, middleY = mainWin.currentCoords[2]/2, mainWin.currentCoords[3]/2
    instructions = Text(Point(middleX, middleY), "Click anywhere on the screen to move the drawing.")
    instructions.setSize(16)
    instructions.setStyle("bold")
    instructions.setFace(font)
    instructions.draw(mainWin)

    # wait for the user to click on the screen
    click = mainWin.getMouse()

    # undraw the instructions
    instructions.undraw()

    # update p
    p = Point(click.getX(), click.getY())

    # plot the new curve
    plot()

    
def helpWin():
    # creates the help win with info
    helpWin = DEGraphWin(title = "Help Window", defCoords=[0,0,750,400], width = 750, height = 400,
    hasTitlebar = True, offsets=[400,400], autoflush=False, hBGColor=color_rgb(213,213,213))

    # create the text
    helpText = Text(Point(375, 200), "Welcome to Max Mayer's Koch Curve Explorer.\n\nButton Info:\nMove: allows user to reposition starting point of drawing\n+/-: Allows user to zoom in/out of the window, in case the graph is out of screen\nDraw: Draws the given curve with the given options. Resets start point\nClear: Clears existing lines and resets start point\nQuit: Well, quits the program\n\nOptions Info:\nLevel: The level of the curve to be drawn. Higher levels take longer to draw\nTheta: The angle of the curve to be drawn. Most common is 60 degrees\nType: The type of curve to be drawn. Currently only Koch Curve and Koch Snowflake are supported\nColor: The color of the curve to be drawn. Color by level coming soon\n\nStatistics Info:\nCurve Length: The length of the curve, with level 0 being 1 unit\nArea Under Curve: The area under the curve, reletive to x axis and unit length\nTime Taken: The time taken to draw the curve\nNumber of Lines: The number of lines used to draw the curve\n\nLearn more at wikipedia.org/wiki/Koch_snowflake")
    helpText.setSize(14)
    helpText.setFace(font)
    helpText.draw(helpWin)
# ------------------ GUI ------------------

# windows
mainWin = DEGraphWin(title = "Graph Window", defCoords=[0,0,500,500], width = 700, height = 700,
hasTitlebar = False, offsets=[100,50], autoflush=False, hBGColor=color_rgb(213,213,213))

controlWin = DEGraphWin(title = "Control Window", defCoords=[0,0,500,500], width = 350, height = 500,
hasTitlebar = True, offsets=[400,400], autoflush=False, hBGColor=color_rgb(213,213,213))

# titles
controlTitle = Text(Point(250, 485), "Koch Curve Explorer")
controlTitle.setSize(22)
controlTitle.setStyle("bold")
controlTitle.setFace(font)
controlTitle.draw(controlWin)

smallText = Text(Point(250, 455), "Welcome to Max Mayer's Koch Curve Explorer.\n  To begin, enter a theta angle and click \'draw\'.")
smallText.setSize(12)
smallText.setFace(font)
smallText.draw(controlWin)

introText = Text(Point(250,250), "Welcome to Max Mayer's Koch Curve Explorer.\nThis is your plotting window. See your control window for instructions.")
introText.setSize(16)
introText.setStyle("bold")
introText.setFace(font)
introText.draw(mainWin)


# line
line = Line(Point(10, 430), Point(490, 430))
line.setWidth(0.5)
line.setFill("black")
line.draw(controlWin)

# draw rectangle for input
rect = Rectangle(Point(10, 420), Point(490, 380))
rect.setWidth(0.5)
rect.setOutline("grey")
rect.draw(controlWin)

# input and titles
levelTitle = Text(Point(100, 400), "Curve Level")
levelTitle.setSize(16)
levelTitle.setStyle("bold")
levelTitle.setFace(font)
levelTitle.draw(controlWin)

levelInput = Slider(Point(355, 400), length = 180, height = 10, min = 0, max = 20, font = (font, 16))
levelInput.draw(controlWin)

rect = Rectangle(Point(10, 370), Point(490, 330))
rect.setWidth(0.5)
rect.setOutline("grey")
rect.draw(controlWin)

thetaTitle = Text(Point(115, 350), "Koch Angle (" + u"\u03B8" + u"\u00B0" + ")")
thetaTitle.setSize(16)
thetaTitle.setStyle("bold")
thetaTitle.setFace(font)
thetaTitle.draw(controlWin)

thetaInput = Slider(Point(355, 350), length = 180, height = 10, min = 0, max = 360, font = (font, 16))
thetaInput.draw(controlWin)

# input for type of drawing (koch curve or koch snowflake)

rect = Rectangle(Point(10, 320), Point(490, 280))
rect.setWidth(0.5)
rect.setOutline("grey")
rect.draw(controlWin)

typeTitle = Text(Point(100, 300), "Type")
typeTitle.setSize(16)
typeTitle.setStyle("bold")
typeTitle.setFace(font)
typeTitle.draw(controlWin)

typeInput = DropDown(Point(355, 300), ["Koch Curve", "Koch Snowflake"], 0, bg=color_rgb(232,232,232))
typeInput.draw(controlWin)

# color input and title (red, green, blue, black, random)

rect = Rectangle(Point(10, 270), Point(490, 230))
rect.setWidth(0.5)
rect.setOutline("grey")
rect.draw(controlWin)

colorTitle = Text(Point(100, 250), "Color")
colorTitle.setSize(16)
colorTitle.setStyle("bold")
colorTitle.setFace(font)
colorTitle.draw(controlWin)

colorInput = DropDown(Point(365, 250), ["Red", "Green", "Blue", "Black", "Random"], 0, bg=color_rgb(232,232,232))
colorInput.draw(controlWin)

# buttons

editStartButton = Button(controlWin, Point(10, 215), 155, 30, label="Move", font = (font, 16), buttonColors=[color_rgb(133,133,133), color_rgb(133,133,133), 'white'], clickedColors=['white', color_rgb(133,133,133), 'black'], timeDelay=0)
editStartButton.activate()

zoomInButton = Button(controlWin, Point(177.5, 215), 70, 30, label="+", font = (font, 16), buttonColors=[color_rgb(133,133,133), color_rgb(133,133,133), 'white'], clickedColors=['white', color_rgb(133,133,133), 'black'], timeDelay=0)
zoomInButton.activate()

zoomOutButton = Button(controlWin, Point(255, 215), 70, 30, label="-", font = (font, 16), buttonColors=[color_rgb(133,133,133), color_rgb(133,133,133), 'white'], clickedColors=['white', color_rgb(133,133,133), 'black'], timeDelay=0)
zoomOutButton.activate()

drawButton = Button(controlWin, Point(337.5, 215), 155, 30, label="Draw", font = (font, 16), buttonColors=[color_rgb(16,134,237), color_rgb(16,134,237), 'white'], clickedColors=['white', color_rgb(16,134,237), 'black'], timeDelay=0)
drawButton.activate()

# statistics

curveLength = Text(Point(250, 160), "Curve Length: ")
curveLength.setSize(16)
curveLength.setFace(font)
curveLength.draw(controlWin)

curveArea = Text(Point(250, 135), "Area Under Curve: ")
curveArea.setSize(16)
curveArea.setFace(font)
curveArea.draw(controlWin)

numLines = Text(Point(250, 110), "Number of Lines: ")
numLines.setSize(16)
numLines.setFace(font)
numLines.draw(controlWin)

timeTaken = Text(Point(250, 85), "Time Taken: ")
timeTaken.setSize(16)
timeTaken.setFace(font)
timeTaken.draw(controlWin)


# help, clear, and quit buttons 

helpButton = Button(controlWin, Point(10, 50), 155, 30, label="Help", font = (font, 16), buttonColors=[color_rgb(133,133,133), color_rgb(133,133,133), 'white'], clickedColors=['white', color_rgb(133,133,133), 'black'], timeDelay=0)
helpButton.activate()

clearButton = Button(controlWin, Point(177.5, 50), 147.5, 30, label="Clear", font = (font, 16),buttonColors=[color_rgb(241,196,51),color_rgb(241,196,51),'white'], clickedColors=['white', color_rgb(241,196,51), 'black'], timeDelay=0)
clearButton.activate()

quitButton = Button(controlWin, Point(337.5, 50), 155, 30, label="Quit", font = (font, 16), buttonColors=[color_rgb(232,77,64),color_rgb(232,77,64),'white'], clickedColors=['white', color_rgb(232,77,64), 'black'], timeDelay=0)
quitButton.activate()



# ------------------ MAIN LOOP ------------------

clickPt = controlWin.getMouse()

while not quitButton.clicked(clickPt):

    
    if drawButton.clicked(clickPt):
        # check if valid input
        if thetaInput.getValue() == 180:
            # create error window
            errorWindow = DEGraphWin(title = "Error", width = 200, height = 200, hasTitlebar=True, offsets=[500,500])
            error = Text(Point(100, 100), "ERROR:\n\nTheta cannot be 180.\nClick to dismiss.")
            error.setSize(16)
            error.setFace(font)
            error.setTextColor("red")
            error.draw(errorWindow)
        # if valid input, draw
        else:
            # reset the mainwindow current coords
            mainWin.setCoords(0,0,500,500)
            plot()
            zoomInButton.activate()
        

    elif zoomInButton.clicked(clickPt):
        mainWin.zoom(ZOOM_IN)
        zoomOutButton.activate()

    elif zoomOutButton.clicked(clickPt):
        # if current coorsd x/y are 500 or any multiple of times 1,5, zoom out
        if mainWin.currentCoords == [0,0,500,500] or (mainWin.currentCoords[2] % 2 == 0 and mainWin.currentCoords[3] % 2 == 0):
            mainWin.setCoords(0,0,mainWin.currentCoords[2]*2,mainWin.currentCoords[3]*2)
            # replot
            plot()
        # else, zoom out
        else:
            mainWin.zoom(ZOOM_OUT)

    elif editStartButton.clicked(clickPt):
        editStartPoint()

    elif clearButton.clicked(clickPt):
        clearLines()
        resetPoint()
    

    elif helpButton.clicked(clickPt):
        helpWin()

        

    clickPt = controlWin.getMouse()
   

mainWin.close()
controlWin.close()


# END
