# Newton's Method Explorer
# MCM '23
# Nonlinear Dynamics, Nov/Dec 2022


# imports
import sys
sys.path.append("../lib")
from DEgraphics import *
import numpy as np
from sympy import diff, sympify, lambdify, solveset, Symbol
import time
import pyautogui

# ----------       DEFINE CONSTANTS      -----------
font = "verdana"
circles = []
count = 1

# ---------------     DEFINE FUNCTIONS       ---------------

# PLOT FUNCTION
# plots newton's method on graph window
# with user inputted values and options
def plot():
    # start timer
    start = time.perf_counter()
    # tell user it's loading
    l = loading1()
    # update equation string and equation
    equation = eqEntry.getText()
    z = Symbol('z')
    e = sympify(equation)
    f = lambdify(z,e)
    d = diff(e,z)
    fprime = lambdify(z,d)
    # colors update
    colors = getColorList()
    # update the roots
    roots = list(solveset(e, z))
    roots = convertList(roots)
    winInfo.update()
    winGraph.update()

    # clear existing graph and circles
    winGraph.clear()
    for c in circles:
        c.undraw()
    c = []

    # load current coords into variables
    xcoord = winGraph.currentCoords[0]
    ycoord = winGraph.currentCoords[1]
    xmin = winGraph.currentCoords[0]
    ymin = winGraph.currentCoords[1]
    xmax = winGraph.currentCoords[2]
    ymax = winGraph.currentCoords[3]

    # determine the x and y step by getting the multiplier 
    multiplier = getQualityMultiplier()
    xStep = (abs(xmax - xmin) / 750) * multiplier
    yStep = (abs(ymax - ymin) / 750) * multiplier

    # get iterations from the user and set counter variable (for statistics) to 0 
    iters = itersEntry.getValue()
    counter = 0

    # now time to iterate through and plot
    # while current x coord is less then x coord max
    while xcoord < xmax:
        # while y coord is less then y coord max
        while ycoord < ymax:
            # turn the position into a complex number
            zPoint = complex(xcoord,ycoord)
            # run it through newtons method
            zPoint = newtons(zPoint, iters, f, fprime)
            # plot the point and its specified color
            winGraph.plot(xcoord,ycoord,color=colors[findClosestRoot(roots, zPoint)])
            # increment counter and y step
            counter+=1
            ycoord += yStep
        # reset y coord back to default
        ycoord = winGraph.currentCoords[1]      
        # increment x step
        xcoord += xStep

    # now its time to plot the roots
    index = 0
    # for every root, create a circle at the location with specified color
    for r in roots:
        c = Circle(Point(r.real, r.imag), 0.05)
        c.setFill(colors[index])
        c.setOutline("white")
        c.setWidth(0.04)
        c.draw(winGraph)
        circles.append(c)
        index+=1
    
    # update statistics
    s1.setText("Number of Roots: " + str(len(roots)))
    s2.setText("Iterations Calculated: " + str("{:,}".format(counter * iters)))
    s3.setText("Points Plotted: " + str("{:,}".format(counter)))
    s4.setText("Process Time: " + str(round(time.perf_counter()-start,2)) + " seconds")

    # undraw the loading message, update graph, and activate zoom button
    loading2(l)
    winGraph.update()
    winInfo.update()
    btnZoomIn.activate()

# FIND CLOSEST ROOT
# returns index of list entry that is closest to value
# I use this to determine how to color the roots
def findClosestRoot(roots, value):
    # turn list into a numpy array
    list = np.asarray(roots)
    # subtract all list entries by value, and run argmin to find the minimum value
    index = (np.abs(list - value)).argmin()
    # then return index
    return index

# CONVERT LIST 
# converts a sympy list of complex roots into a python
# complex compatable list
def convertList(roots):
    # all we need to do is cast python complex to each value in roots list
    result = []
    for val in roots:
        result.append(complex(val))
    return result

# NEWTONS METHOD
# returns the result of running newton's method on 
# z0 for iters iterations, using f and fprime (sympy equations)
def newtons(z0, iters, f, fprime):
    # for every iteration, z0 = z0 - f(z0)/f'(z0)
    for i in range(iters):
        z0 = z0 - f(z0) / fprime(z0)
    return z0

# GET COLOR LIST
# returns the list of colors that the user chooses
def getColorList():
    color = colorEntry.getChoice()
    if color == "Fall":
        return [color_rgb(91,22,69), color_rgb(147,9,62), color_rgb(202,0,54), color_rgb(255,87,48), color_rgb(255,196,10)]
    elif color == "Sea":
        return [color_rgb(233,182,107), color_rgb(191,208,202), color_rgb(164,178,181), color_rgb(13,76,128), color_rgb(91,143,144)]
    elif color == "Sunrise":
        return [color_rgb(145,110,199), color_rgb(208,96,171), color_rgb(243,106,138), color_rgb(254,158,129), color_rgb(237,186,102)]
    elif color == "Forest":
        return [color_rgb(75,107,63), color_rgb(58,73,42), color_rgb(59,46,31), color_rgb(144,122,76), color_rgb(212,191,139)]
    elif color == "Greyscale":
        return [color_rgb(0,0,0), color_rgb(51,51,51), color_rgb(102,102,102), color_rgb(153,153,153), color_rgb(200,200,200)]
    else: #rainbow (default)
        return [color_rgb(237,19,72), color_rgb(251,191,94), color_rgb(5,113,82), color_rgb(0,44,120), color_rgb(238,107,65), color_rgb(14,194,97), color_rgb(112,6,94), color_rgb(2,84,89)]

# GET QUALITY MULTIPLIER
# returns a value used to calculate the step size
def getQualityMultiplier():
    quality = qualEntry.getChoice()
    if quality == "Ultra (Very Slow)":
        return 0.35
    elif quality == "High (Slow)":
        return 0.7
    elif quality == "Medium (Default)":
        return 1
    elif quality == "Low (Faster)":
        return 2
    else: # "Sketch" option (default)
        return 3

# ERROR WINDOW
# displays an error window if the user has an error
# with entering an equation
def errorWindow():
    winError = DEGraphWin(title = "Error", defCoords=[-3,-3,3,3], width = 300, height = 300,
    hasTitlebar = True, offsets=[500,150], autoflush=False, hBGColor=color_rgb(213,213,213))
    t = Text(Point(0,0), "Plot Error. Please check:\n\n1. Equation box is not empty.\n\n2. Equation uses variable \'z\'\nand no other letter.\n\n3. If equation has more than 5\nroots, use rainbow color (up\nto 8 roots).\n\n4. Equation does not include trig\nfunctions.")
    t.setStyle('bold')
    t.setFace(font)
    t.setSize(16)
    t.draw(winError)

# SCREENSHOT FUNCTION
# saves a screenshot of the graph window to the user's desktop
# returns the number of screenshots taken so far - 1
def screenshot(count):
    # take screenshot using pyautogui
    image = pyautogui.screenshot("NewtonsFractal" + str(count) + ".png", region=(1000,300,1500,1200))
    # update screenshot count
    return count + 1

# STATUS FUNCTIONS
# functions that let user know it is verifying/loading
# 1 functions create and return a text
# 2 functions take as input the text and undraw it
def loading1():
    t = Text(Point(0,150), "Loading...")
    t.setFace(font)
    t.setSize(18)
    t.setStyle('bold')
    t.setFill('red')
    t.draw(winInfo)
    return t

def loading2(t):
    t.undraw()

def verify1():
    t = Text(Point(0,150), "Verifying...")
    t.setFace(font)
    t.setSize(18)
    t.setStyle('bold')
    t.setFill('green')
    t.draw(winInfo)
    return t

def verify2(t):
    t.undraw()

# ----------------------    CREATE WINDOWS     ----------------------
winTitle = DEGraphWin(title = "Title Window", defCoords=[-10,-10,10,10], width = 1100, height = 100,
hasTitlebar = False, offsets=[150,50], autoflush=True, hBGColor=color_rgb(213,213,213))

winInfo = DEGraphWin(title = "Control Panel", defCoords=[-175,-300,175,300], width = 350, height = 600,
hasTitlebar = True, offsets=[150,150], autoflush=True, hBGColor=color_rgb(213,213,213))
winInfo.setBackground(color_rgb(213,213,213))

winGraph = DEGraphWin(title = "Graph Window", defCoords=[-3.75,-3,3.75,3], width = 750, height = 600,
hasTitlebar = False, offsets=[500,150], autoflush=False, hBGColor=color_rgb(213,213,213))

# ---------------------        CREATE TITLES     ---------------------
titleText = Text(Point(0,2), "Newton's Method Explorer")
titleText.setSize(36)
titleText.setStyle('bold')
titleText.setFace(font)
titleText.draw(winTitle)

instructionText = Text(Point(0,-5),"Welcome to Newton's Method Explorer created by Max Mayer '23. To begin, enter an equation in the control panel and then hit \'plot\'.")
instructionText.setSize(14)
instructionText.setFace(font)
instructionText.draw(winTitle)

infoTitle = Text(Point(0,275), "Control Panel")
infoTitle.setStyle('bold')
infoTitle.setSize(25)
infoTitle.setFace(font)
infoTitle.draw(winInfo)

l = Line(Point(-170, 130), Point(170,130))
l.draw(winInfo)

cusTitle = Text(Point(0,110), "Customizations")
cusTitle.setStyle('bold')
cusTitle.setSize(20)
cusTitle.setFace(font)
cusTitle.draw(winInfo)

colorTitle = Text(Point(-80, 80), "Color Scheme: ")
colorTitle.setStyle('bold')
colorTitle.setFace(font)
colorTitle.setSize(16)
colorTitle.draw(winInfo)

itersTitle = Text(Point(-60, 50), "Iterations: ")
itersTitle.setStyle('bold')
itersTitle.setFace(font)
itersTitle.setSize(16)
itersTitle.draw(winInfo)

qualTitle = Text(Point(-80, 20), "Quality: ")
qualTitle.setStyle('bold')
qualTitle.setFace(font)
qualTitle.setSize(16)
qualTitle.draw(winInfo)

l = Line(Point(-170,0), Point(170,0))
l.draw(winInfo)

statTitle = Text(Point(0,-20), "Statistics")
statTitle.setStyle('bold')
statTitle.setSize(20)
statTitle.setFace(font)
statTitle.draw(winInfo)

s1 = Text(Point(0,-50), "Number of Roots: ")
s1.setStyle('bold')
s1.setFace(font)
s1.setSize(16)
s1.draw(winInfo)

s2 = Text(Point(0,-75), "Iterations Calculated: ")
s2.setStyle('bold')
s2.setFace(font)
s2.setSize(16)
s2.draw(winInfo)

s3 = Text(Point(0,-100), "Points Plotted: ")
s3.setStyle('bold')
s3.setFace(font)
s3.setSize(16)
s3.draw(winInfo)

s4 = Text(Point(0,-125), "Process Time: ")
s4.setStyle('bold')
s4.setFace(font)
s4.setSize(16)
s4.draw(winInfo)

l = Line(Point(-170,-140), Point(170,-140))
l.draw(winInfo)

newtonsTitle = Text(Point(0,-160), "What is Newton's Method?")
newtonsTitle.setStyle('bold')
newtonsTitle.setSize(20)
newtonsTitle.setFace(font)
newtonsTitle.draw(winInfo)

newtonsText = Text(Point(0,-230), "Newton's Method is a method used to find\nthe roots of a function using the following\nformula: x_n+1 = x_n - f(x_n)/f'(x_n).\nThe colors on the graph indicate\nthe root that the point belongs to.\nThe number of roots is the number of colors\non the graph.")
newtonsText.setSize(14)
newtonsText.setFace(font)
newtonsText.draw(winInfo)


# ---------------------     CREATE INPUT      -----------------------
eqTitle = Text(Point(-70, 235), "Equation = ")
eqTitle.setStyle('bold')
eqTitle.setSize(18)
eqTitle.draw(winInfo)
eqEntry = Entry(Point(35,235), width = 15)
eqEntry.draw(winInfo)

colorEntry = DropDown(Point(65,80), ["Rainbow", "Sea", "Forest", "Fall", "Sunrise", "Greyscale"],(font,14), color_rgb(213,213,213))
colorEntry.draw(winInfo)

itersEntry = IntEntry(Point(55,50), 16, [1,100])
itersEntry.setDefault(10)
itersEntry.draw(winInfo)

qualEntry = DropDown(Point(60,20), [ "Sketch (Fastest)", "Low (Faster)", "Medium (Default)", "High (Slow)", "Ultra (Very Slow)"], (font,14), color_rgb(213,213,213))
qualEntry.draw(winInfo)

# ---------------------      CREATE BUTTONS       ------------------------
btnClose = Button(winInfo, topLeft = Point(85,200), width = 65, height = 30,
                 edgeWidth = 2, label = 'QUIT',
                 buttonColors = [color_rgb(243,135,47),color_rgb(243,135,47),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
btnClose.activate()

# create button to reset values
btnReset = Button(winInfo, topLeft = Point(0,200), width = 65, height = 30,
                edgeWidth = 2, label = 'RESET',
                buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                clickedColors = ['white','red','black'],
                font=('courier',18), timeDelay = 0.05)
btnReset.activate()

# create button to plot graph
btnPlot = Button(winInfo, topLeft = Point(-80,200), width = 65, height = 30,
                edgeWidth = 2, label = 'PLOT',
                buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                clickedColors = ['white','red','black'],
                font=('courier',18), timeDelay = 0.05)
btnPlot.activate()

# zoom buttons
btnZoomIn = Button(winInfo, topLeft = Point(-160,200), width = 30, height = 30,
                edgeWidth = 2, label = '+',
                buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                clickedColors = ['white','red','black'],
                font=('courier',18), timeDelay = 0.05)

btnZoomOut = Button(winInfo, topLeft = Point(-125,200), width = 30, height = 30,
                edgeWidth = 2, label = '-',
                buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                clickedColors = ['white','red','black'],
                font=('courier',18), timeDelay = 0.05)

# equation syntax help button
btnHelp = Button(winInfo, topLeft = Point(100,242), width = 15, height = 15,
                 edgeWidth = 2, label = '?',
                 buttonColors = [color_rgb(243,135,47),color_rgb(243,135,47),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
btnHelp.activate()

# button to take screenshot of graph

btnScreenshot = Button(winInfo, topLeft = Point(140,290), width = 25, height = 25,
                 edgeWidth = 2, label = u"\U0001F4F7",
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
btnScreenshot.activate()


# -------------------         MAIN LOOP        -----------------
clickPt = winInfo.getMouse()
while not btnClose.clicked(clickPt):
    # if plot is clicked
    if btnPlot.clicked(clickPt):
        t = verify1()
        entry = eqEntry.getText()
        # ERRORS:
        # if no equation is entered
        # if equation doesnt have z
        # if roots are more then the available colors
        if len(entry) == 0 or not entry.__contains__("z") or (len(list(solveset(sympify(entry), Symbol('z')))) > 5 and colorEntry.getChoice() != "Rainbow"):
            # undraw the verification text
            verify2(t)
            # and show error window
            errorWindow()
        # otherwise, plot
        else:
            # undraw the verification text
            verify2(t)
            # plot the graph
            plot()
    
    # if zoom in button is clicked
    elif btnZoomIn.clicked(clickPt):
        # zoom in, tell user it's veryfying, and get equation
        winGraph.zoom(ZOOM_IN)
        t = verify1()
        entry = eqEntry.getText()
        # the error check is the same as above
        if len(entry) == 0 or not entry.__contains__("z") or (len(list(solveset(sympify(entry), Symbol('z')))) > 5 and colorEntry.getChoice() != "Rainbow"):
            verify2(t)
            winGraph.zoom(ZOOM_OUT)
            errorWindow()
        # otherwise, plot
        else:
            verify2(t)
            plot()
            btnZoomOut.activate()
    
    # if zoom out button is clicked
    elif btnZoomOut.clicked(clickPt):
        # this is pretty much the same at the one above
        winGraph.zoom(ZOOM_OUT)
        t = verify1()
        entry = eqEntry.getText()
        if len(entry) == 0 or not entry.__contains__("z") or (len(list(solveset(sympify(entry), Symbol('z')))) > 5 and colorEntry.getChoice() != "Rainbow"):
            verify2(t)
            errorWindow()
        else:
            verify2(t)
            plot()
            # since we zoomed out, deactivate the zoom out button so we dont get an error if clicked
            btnZoomOut.deactivate()
            # and then we can activate the zoom in button just in case it isnt
            btnZoomIn.activate()

    # if reset button is clicked
    elif btnReset.clicked(clickPt):
        # undraw all the circles (roots)
        for c in circles:
            c.undraw()
        c = []
        # clear graph, deactivate zoom buttons
        winGraph.clear()
        btnZoomIn.deactivate()
        btnZoomOut.deactivate()
        # reset statistics
        s1.setText("Number of Roots: ")
        s2.setText("Iterations Calculated: ")
        s3.setText("Points Plotted: ")
        s4.setText("Process Time: ")

    # if help button is clicked
    elif btnHelp.clicked(clickPt):
        # display help window
        winHelp = DEGraphWin(title = "Equation Entry Syntax", defCoords=[-3,-3,3,3], width = 300, height = 300,
        hasTitlebar = True, offsets=[500,150], autoflush=False, hBGColor=color_rgb(213,213,213))

        t = Text(Point(0,0), "Equation Entry Syntax: \n\n Main Variable: \'z\'\n Add: \'+\'\nSubtract: \'-\'\nMultiply: \'*\'\nDivide: \'/\'\nPower (^): \'**\'\n\nExamples/Inspirations:\n\n z**2 + 1\nz**6 - z**3 + 2\nz**4 - 1")
        t.setStyle('bold')
        t.setFace(font)
        t.setSize(16)
        t.draw(winHelp)
    
    # if camera button is clicked
    elif btnScreenshot.clicked(clickPt):
        # take screenshot with screenshot function and count variable
        count = screenshot(count)
    
    # finnaly, get a click point
    clickPt = winInfo.getMouse()

# close windows
winInfo.close()
winGraph.close()
winTitle.close()