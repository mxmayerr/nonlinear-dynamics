# Mandelbrot Julia Set Super Explorer
# MCM '23
# Nonlinear Dynamics, Jan/Feb 2023

# imports
import random as r
import sys
sys.path.append("../lib")
from DEgraphicsMod import *
import numpy as np
from numpy import inf
from tkinter import colorchooser

# global and program variables
font = "verdana"
seaColors = [color_rgb(233,182,107), color_rgb(191,208,202), color_rgb(164,178,181), color_rgb(13,76,128), color_rgb(91,143,144)]


global cVal
cVal = complex(0, 0)

global colorMode 
colorMode = "light"

global virtualSizeM
virtualSizeM = 10 # 10 cm wide to start

global virtualSizeJ
virtualSizeJ = 10 # 10 cm wide to start

global lines
lines = []

global autoFlush
autoFlush = False

# dictionary that holds the labels and up-to values for the virtual size, also holds conversion factor
global virtualSizeDict
virtualSizeDict = {
    # up to 100 cm, display in cm, with a conversion factor of 1x from the starting cm value
    100: ("cm", 1),
    # up to 1000 m (1,000,000 cm), display in m, with a conversion factor of 100x
    1_000_000: ("m", 100),
    # up to 5000 km (5,000,000,000 cm), display in km, with a conversion factor of 100,000x
    5_000_000_000: ("km", 100_000),
    # up to 7917 miles (width of earth, 1,274,100,000 cm), display in miles, with a conversion factor of 160,934x (how wide is mile in cm)
    1_274_100_000: ("miles", 160_934),
    # up to 11 earths (width of jupiter, 13,982,100,000 cm), display in earths, with a conversion factor of 1,274,200,000x (how wide is earth cm)
    13_982_100_000: ("earths", 1_274_200_000),
    # up to 10 jupiters (width of sun, 1,392,000,000,000,000,000 cm), display in jupiters, with a conversion factor of 13,920,000,000x (how wide is jupiter cm)
    139_821_000_000: ("jupiters", 13_920_000_000),
    # up to 6500 suns (width of solar system, 908,997,718,576,000 cm), display in suns, with a conversion factor of 139,267,800,000x (how wide is sun cm)
    908_997_718_576_000: ("suns", 139_821_000_000),
    # up to 10 solar systems (width of a light year, 9,460,730,472,580,800,000 cm), display in solar systems, with a conversion factor of 908,997,718,576,000x (how wide is solar system cm)
    9_460_730_472_580_800_000: ("solar systems", 908_997_718_576_000),
    # up to infinity, display in light years, with a conversion factor of 9,460,730,472,580,800,000x (how wide is light year cm)
    inf: ("light years", 9_460_730_472_580_800_000)
}



def plotMandelbrot(maxit = 30, sweeps = 3):
    """
    Plots the mandelbrot set using the current window settings

    Args:
        maxit (int, optional): The maximum number of iterations to run. Defaults to 30.
        sweeps (int, optional): The number of sweeps to do. Defaults to 3.
    
    Returns:
        None
    """
    # first, we need to get the color and type
    type, color = typeMEntry.getChoice().split(" ")
    
    # update maxit
    maxit = int(itersMEntry.getText())

    # clear the window
    winMandel.clear()

    # get current pixel informaiton
    h = winMandel.height
    w = winMandel.width
    xmin = winMandel.currentCoords[0]
    ymin = winMandel.currentCoords[1]
    xmax = winMandel.currentCoords[2]
    ymax = winMandel.currentCoords[3]

    # create 2d numpy array of complex numbers and initialize
    x,y = np.ogrid[ xmin:xmax:w*1j , ymax:ymin:h*1j ]
    c = x + (y * 1j)
    z = c

    # create a 2d numpy array of integers to hold the number of iterations
    divtime = maxit + np.zeros(z.shape, dtype=int)

    # iterate
    for i in range(maxit):
        # iterate
        z = z**2 + c
        # check for divergence (more than 2 in magnitude)
        diverge = z*np.conj(z) > 4
        # update the diverge time
        div_now = diverge & (divtime==maxit)
        divtime[div_now] = i
        # update z
        z[diverge] = 2
    
    # if we are plotting an escape
    if type == "Escape":
        # determine the color type
        if color == "(Sea)":
            for sweep in range(sweeps):
                # do sweeps
                i = sweep
                while i < winMandel.width:
                    for j in range(winMandel.height):
                        # using the following colors from the sea array, we can catorgarize the escaping points
                        if divtime [i,j] != maxit:
                            if divtime[i,j] < 4:
                                winMandel.plotPixel(i, j, seaColors[0])
                            elif divtime[i,j] < 8:
                                winMandel.plotPixel(i, j, seaColors[1])
                            elif divtime[i,j] < 12:
                                winMandel.plotPixel(i, j, seaColors[2])
                            elif divtime[i,j] < 16:
                                winMandel.plotPixel(i, j, seaColors[3])
                            else:
                                winMandel.plotPixel(i, j, seaColors[4])
                    i+=sweeps
                winMandel.update()
        # other color scheme
        elif color == "(Sunrise)":
            for sweep in range(sweeps):
                i = sweep
                while i < winMandel.width:
                    for j in range(winMandel.height):
                        if divtime [i,j] != maxit:
                            winMandel.plotPixel(i, j, color_rgb(divtime[i,j]*255//maxit, 0, 200))
                    i+=sweeps
                winMandel.update()
                print (sweep)
        elif color == "(Custom)":
            # get the custom color
            rgb,hex = colorchooser.askcolor(title="Choose Color")
            r,g,b = rgb

            for sweep in range(sweeps):
                i = sweep
                while i < winMandel.width:
                    for j in range(winMandel.height):
                        if divtime [i,j] != maxit:
                            winMandel.plotPixel(i, j, color_rgb(divtime[i,j]*r//maxit, divtime[i,j]*g//maxit, divtime[i,j]*b//maxit))
                    i+=sweeps
                winMandel.update()
    else: # type == "2Tone":
        for sweep in range(sweeps):
            i = sweep
            while i < winMandel.width:
                for j in range(winMandel.height):
                    if divtime [i,j] != maxit:
                        winMandel.plotPixel(i, j, 'black')
                    else:
                        winMandel.plotPixel(i, j, 'white')
                i+=sweeps
            winMandel.update()
            print (sweep)
    btnZoomInMandel.activate()

def getC():
    """
    Gets the current c value from the mouse click

    Args: 
        None
    
    Returns:
        None (updates global variable)
    """
    global cVal
    global lines
    # clear existing lines
    for line in lines:
        line.undraw()
    cVal = complex(winMandel.getMouse().getX(), winMandel.getMouse().getY())
    # put the red lines on the graph
    vLine = Line(Point(cVal.real, winMandel.currentCoords[1]), Point(cVal.real, winMandel.currentCoords[3]))
    hLine = Line(Point(winMandel.currentCoords[0], cVal.imag), Point(winMandel.currentCoords[2], cVal.imag))
    vLine.setWidth(2)
    hLine.setWidth(2)
    vLine.setFill('red')
    hLine.setFill('red')
    lines.append(vLine)
    lines.append(hLine)
    vLine.draw(winMandel)
    hLine.draw(winMandel)
    cLabel.setText("C: " + str(round(cVal.real, 2)) + " + " + str(round(cVal.imag, 2)) + "i")

def showOrbit():
    """
    Shows the orbit of the current c value on the Mandelbrot set

    Args:
        None
    
    Returns:
        None (draws on the window)
    
    Notes:
        This funciton works, but when drawn on the graphed window, is very slow.
        This is most likely because of double drawing. Maybe need to implement 
        multithreading?
    """
    global cVal

    drawings = []

    z = complex(0,0)
    z = z ** z + cVal
    # we will plot 20 lines
    for n in range(50):
        # plot the point at original z
        c = Circle(Point(z.real, z.imag), 0.01)
        c.setFill('red')
        c.draw(winMandel)
        winMandel.update()
        drawings.append(c)

        # wait 0.3
        time.sleep(0.02)

        ogZ = z

        # iterate z
        z = z ** z + cVal

        # plot the line from the previous point to the new point
        l = Line(Point(ogZ.real, ogZ.imag), Point(z.real, z.imag))
        l.setWidth(2)
        l.setFill('red')
        l.draw(winMandel)
        winMandel.update()
        drawings.append(l)

        # wait 0.3
        time.sleep(0.02)  

    # undraw all the drawings
    for drawing in drawings:
        drawing.undraw()
        winMandel.update()
        time.sleep(0.02)

def plotJulia(): # type = "inverse", "border"
    """
    Calls the appropriate function to plot the Julia set

    Args:
        None

    Returns:
        None (plots on the window)
    """
    type = typeJEntry.getChoice().split(" ")[0]
    if type == "Inverse":
        plotJuliaInverse()
    elif type == "Border":
        plotJuliaBorder()
    else:
        print("Error: invalid type")
        return
    
def plotJuliaInverse():
    """
    Plots the julia set using the inverse algorithm

    Args:
        None

    Returns:
        None (plots on the window)
    """
    # get color
    rgb,hex = colorchooser.askcolor(title="Choose Color")
    rr,g,b = rgb

    # initialize complex number z
    z = complex(20*r.random(), 20*r.random())
    # for 10,000 iterations, calculate the inverse and randomize the sign
    for n in range(10000):
        z = (z-cVal)**0.5
        if r.random() < 0.5:
            z*= -1
        
    # do the same thing again but plot the points
    for n in range(10000):
        z = (z-cVal)**0.5
        if r.random() < 0.5:
            z*= -1
        winJulia.plot(z.real, z.imag, color_rgb(rr, g, b))
    winJulia.update()

def plotJuliaBorder(maxit = 50):
    """
    Plots the julia set using the border scan algorithm.

    Args:
        maxit (int, optional): the maximum number of iterations to run
    
    Returns:    
        None (plots on the window)
    """
    # get color
    rgb,hex = colorchooser.askcolor(title="Choose Color")
    r,g,b = rgb

    # get iterations
    maxit = int(itersJEntry.getText())

    # get the window coordinates
    h = winJulia.height
    w = winJulia.width
    xmin = winJulia.currentCoords[0]
    ymin = winJulia.currentCoords[1]
    xmax = winJulia.currentCoords[2]
    ymax = winJulia.currentCoords[3]

    
    # first, we need to create an array of complex numbers
    x,y = np.ogrid[ xmin:xmax:(w*1j) , ymax:ymin:(h*1j) ]
    c = x + (y * 1j)
    z = c

    # then, we need to iterate through the array and calculate the escape time
    # for each point
    divtime = maxit + np.zeros(z.shape, dtype=int)
    for i in range(maxit):
        z = z**2 + cVal
        diverge = z*np.conj(z) > 4
        div_now = diverge & (divtime==maxit)
        divtime[div_now] = i
        z[diverge] = 2

    # now, we need to iterate through the array and plot the points
    # that are at max iterations and at least one of its neighbors are but not all of them
    
    # for evert point in the array
    for i in range(w-1):
        for j in range(h-1):
            # if the point is at max iterations
            if divtime[i,j] == maxit:
                # check if any of its neighbors are at max iterations but not all of them
                # so if a point in either of the 4 cardinal directions or 4 diagonal directions is at max iterations, then we should plot it
                if (divtime[i-1,j] == maxit and divtime[i+1,j] != maxit) or (divtime[i+1,j] == maxit and divtime[i-1,j] != maxit) or (divtime[i,j-1] == maxit and divtime[i,j+1] != maxit) or (divtime[i,j+1] == maxit and divtime[i,j-1] != maxit) or (divtime[i-1,j-1] == maxit and divtime[i+1,j+1] != maxit) or (divtime[i+1,j+1] == maxit and divtime[i-1,j-1] != maxit) or (divtime[i-1,j+1] == maxit and divtime[i+1,j-1] != maxit) or (divtime[i+1,j-1] == maxit and divtime[i-1,j+1] != maxit):
                    winJulia.plotPixel(i, j, color_rgb(r,g,b))
    btnZoomInJulia.activate()
    winJulia.update()

def zoomIn(window):
    """
    Zooms in on the given window

    Args:
        window (GraphWin): the window to zoom in on

    Returns:
        magnitude (float): the magnitude of the zoom in
    """
    # get current coords before zoom in
    xmin1, ymin1, xmax1, ymax1 = window.currentCoords

    # zoom in
    window.zoom(ZOOM_IN)

    # get new coords after zoom in
    xmin2, ymin2, xmax2, ymax2 = window.currentCoords

    # return how much the window was zoomed in
    # for example, if the window size was 4, and after zooming in it was 2, the magnitude would be 2
    mag = abs(xmax1 - xmin1) / abs(xmax2 - xmin2)

    # activate the zoom out button
    if "M" in str(window):
        btnZoomOutMandel.activate()
    elif "J" in str(window):
        btnZoomOutJulia.activate()

    return (mag)


def zoomOut(window):
    """
    Zooms out on the given window.

    Args:
        window (GraphWin): the window to zoom out on

    Returns:
        None (updates global variables and replots on the window)
    """
    global virtualSizeM
    global virtualSizeJ

    window.zoom(ZOOM_OUT)

    if "M" in str(window):
        virtualSizeM = 10
        virtualSizeLabelM.setText("Virtual Size: " + str(virtualSizeM) + " cm")
        btnZoomOutMandel.deactivate()
        plotMandelbrot()
    elif "J" in str(window):
        virtualSizeJ = 10
        virtualSizeLabelJ.setText("Virtual Size: " + str(virtualSizeJ) + " cm")
        btnZoomOutJulia.deactivate()
        plotJulia()
   

def toggleAutoFlush():
    """
    Toggles auto flush on and off.

    Args:
        None

    Returns:
        None (updates global variables)
    """    
    global autoFlush

    if autoFlush:
        autoFlush = False
        btnAutoFlush.setCaption("AF: OFF")
        winMandel.setAutoFlush(False)
        winJulia.setAutoFlush(False)
    else:
        autoFlush = True
        btnAutoFlush.setCaption("AF: ON")
        winMandel.setAutoFlush(True)
        winJulia.setAutoFlush(True)


def updateVirtualSize(magnitude, type): #type is either "Mandelbrot" or "Julia"
    """
    Updates the virtual size for the given window and magnitude

    Args:
        magnitude (float): the magnitude of the zoom in
        type (str): the type of window to update the virtual size for. Either "Mandelbrot" or "Julia"

    Returns:
        None (updates global variables)
    """
    global virtualSizeM
    global virtualSizeJ
    global virtualSizeDict

    if type == "Mandelbrot":
        virtualSizeM = virtualSizeM * magnitude

        # update the virtual size label
        for size in virtualSizeDict:
            if virtualSizeM < size:
                scaledSize = virtualSizeM / virtualSizeDict[size][1] #convert to the correct scale with the scale factor
                virtualSizeLabelM.setText("Virtual Size: " + str(round(scaledSize)) + " " + virtualSizeDict[size][0])
                break

    elif type == "Julia":
        virtualSizeJ = virtualSizeJ * magnitude

         # update the virtual size label
        for size in virtualSizeDict:
            if virtualSizeJ < size:
                scaledSize = virtualSizeJ / virtualSizeDict[size][1] #convert to the correct scale with the scale factor
                virtualSizeLabelJ.setText("Virtual Size: " + str(round(scaledSize)) + " " + virtualSizeDict[size][0])
                break
    

def toggleControlPanel():
    """
    Toggles the control panel.

    Args:
        None

    Returns:
        None 
    """
    # if the title is open, switch to control panel
    if titleText.isDrawn():
        titleText.undraw()
        instructionText.undraw()

        mandelTitle.draw(winTitle)
        juliaTitle.draw(winTitle)
        controlTitle.draw(winTitle)
        itersMLabel.draw(winTitle)
        typeMLabel.draw(winTitle)
        itersJLabel.draw(winTitle)
        typeJLabel.draw(winTitle)
        cLabel.draw(winTitle)
        virtualSizeLabelM.draw(winTitle)
        virtualSizeLabelJ.draw(winTitle)

        itersMEntry.draw(winTitle)
        typeMEntry.draw(winTitle)
        itersJEntry.draw(winTitle)
        typeJEntry.draw(winTitle)

        btnQuit.draw(winTitle)
        btnClearMandel.draw(winTitle)
        btnClearJulia.draw(winTitle)
        btnPlotMandel.draw(winTitle)
        btnGetC.draw(winTitle)
        btnZoomInMandel.draw(winTitle)
        btnZoomInJulia.draw(winTitle)
        btnZoomOutJulia.draw(winTitle)
        btnZoomOutMandel.draw(winTitle)
        btnAutoFlush.draw(winTitle)

        div1.draw(winTitle)
        div2.draw(winTitle)
        div3.draw(winTitle)

        winJulia.setBorderColor(color_rgb(255,0,0))
        winMandel.setBorderColor(color_rgb(0,0,255))

    # else, if the control panel is open, switch to title
    else:
        mandelTitle.undraw()
        juliaTitle.undraw()
        controlTitle.undraw()
        itersMLabel.undraw()
        typeMLabel.undraw()
        itersJLabel.undraw()
        typeJLabel.undraw()
        cLabel.undraw()
        virtualSizeLabelM.undraw()
        virtualSizeLabelJ.undraw()

        itersMEntry.undraw()
        typeMEntry.undraw()
        itersJEntry.undraw()
        typeJEntry.undraw()

        btnQuit.undraw()
        btnClearMandel.undraw()
        btnClearJulia.undraw()
        btnPlotMandel.undraw()
        btnGetC.undraw()
        btnZoomInMandel.undraw()
        btnZoomInJulia.undraw()
        btnZoomOutJulia.undraw()
        btnZoomOutMandel.undraw()
        btnAutoFlush.undraw()




        div1.undraw()
        div2.undraw()
        div3.undraw()
        
        winJulia.setBorderColor(color_rgb(213,213,213))
        winMandel.setBorderColor(color_rgb(213,213,213))

        titleText.draw(winTitle)
        instructionText.draw(winTitle)


def toggleColorMode():
    """
    Toggles the color mode.

    Args:
        None

    Returns:
        None (updates global variables)
    """
    global colorMode
    if colorMode == "dark": 
        colorMode = "light"

        btnColorMode.setCaption("\U0001F319")

        winTitle.setBackground(color_rgb(236,236,236))
        winMandel.setBackground(color_rgb(236,236,236))
        winJulia.setBackground(color_rgb(236,236,236))
        titleText.setTextColor(color_rgb(0,0,0))
        instructionText.setTextColor(color_rgb(0,0,0))
        controlTitle.setTextColor(color_rgb(0,0,0))
        itersMLabel.setTextColor(color_rgb(0,0,0))
        typeMLabel.setTextColor(color_rgb(0,0,0))
        itersJLabel.setTextColor(color_rgb(0,0,0))
        typeJLabel.setTextColor(color_rgb(0,0,0))
        cLabel.setTextColor(color_rgb(0,0,0))
        div1.setFill(color_rgb(0,0,0))
        div2.setFill(color_rgb(0,0,0))
        div3.setFill(color_rgb(0,0,0))
        typeMEntry.setFill(color_rgb(236,236,236))
        typeJEntry.setFill(color_rgb(236,236,236))
        
    elif colorMode == "light": 
        colorMode = "dark"

        btnColorMode.setCaption("\u2600\uFE0F")

        winTitle.setBackground(color_rgb(39,39,39))
        winMandel.setBackground(color_rgb(39,39,39))
        winJulia.setBackground(color_rgb(39,39,39))
        titleText.setTextColor(color_rgb(255,255,255))
        instructionText.setTextColor(color_rgb(255,255,255))
        controlTitle.setTextColor(color_rgb(255,255,255))
        itersMLabel.setTextColor(color_rgb(255,255,255))
        typeMLabel.setTextColor(color_rgb(255,255,255))
        itersJLabel.setTextColor(color_rgb(255,255,255))
        typeJLabel.setTextColor(color_rgb(255,255,255))
        cLabel.setTextColor(color_rgb(255,255,255))
        div1.setFill(color_rgb(255,255,255))
        div2.setFill(color_rgb(255,255,255))
        div3.setFill(color_rgb(255,255,255))
        typeMEntry.setFill(color_rgb(39,39,39))
        typeJEntry.setFill(color_rgb(39,39,39))
        
# ----------------------    CREATE WINDOWS     ----------------------
winTitle = DEGraphWin(title = "Title Window", defCoords=[0,0,120,17.5], width = 1200, height = 175,
hasTitlebar = False, offsets=[100,25], autoflush=True, hBGColor=color_rgb(213,213,213))

winMandel = DEGraphWin(title = "Mandel", defCoords=[-2,-1.4,0.8,1.4], width = 600, height = 600,
hasTitlebar = False, offsets=[100,200], autoflush=False, hBGColor=color_rgb(213,213,213), hThickness=3)

winJulia = DEGraphWin(title = "Julia", defCoords=[-2,-2, 2, 2], width = 600, height = 600,
hasTitlebar = False, offsets=[700,200], autoflush=False, hBGColor=color_rgb(213,213,213), hThickness=3)


# ---------------------        CREATE TITLES     ---------------------
titleText = Text(Point(60,14), "Mandelbrot SUPER Explorer")
titleText.setSize(36)
titleText.setStyle('bold')
titleText.setFace(font)
titleText.draw(winTitle)

# instructionText = Text(Point(60,6),"The Mandelbrot set is a really, really big deal. A lot of people don't understand it, but it's a tremendous thing. It's a set of complex numbers\nthat creates an amazing pattern when you graph them. Trust me, it's huge. It's like a fractal, and it's been studied by some of the best minds in mathematics.\nIt's one of the most famous examples of a fractal. And let me tell you, it's a tremendous fractal, it's a fantastic fractal.\n-Donald Trump, proud supportter of the Mandelbrot set")
instructionText = Text(Point(60,6), "Welcome to the SUPER Mandelbrot Explorer created by Max Mayer '23. Click the gear icon on this panel to begin.\n\nTo see these sets in action, choose a plot type and click plot. \"GetC\" button requires a click on the Mandelbrot set. You can Set iteration amount\nif you'd like, and play around with the colors. Zoom by using the \"+\" and \"-\"buttons and clicking two points on the coresponding\nwindow. The virtual size represents the size of the originally plotted graph.\"AF\" stands for Autoflush.\nIf you run into any errors, close the program and rerun.")
instructionText.setSize(14)
instructionText.setFace(font)
instructionText.draw(winTitle)

juliaTitle = Text(Point(80,15), "Julia Set Controls") 
mandelTitle = Text(Point(40,15), "Mandelbrot Set Controls")
juliaTitle.setSize(24)
mandelTitle.setSize(24)
juliaTitle.setFace(font)
mandelTitle.setFace(font)
mandelTitle.setStyle('bold')
juliaTitle.setStyle('bold')
juliaTitle.setFill(color_rgb(255,0,0))
mandelTitle.setFill(color_rgb(0,0,255))

controlTitle = Text(Point(10,8), "Control\nPanel")
controlTitle.setSize(32)
controlTitle.setFace(font)
controlTitle.setStyle('bold')

# titles for mandelbrot set controls (iterations, plot type, color scheme)
itersMLabel = Text(Point(26,10), "Iterations:")
itersMLabel.setSize(16)
itersMLabel.setFace(font)
itersMLabel.setStyle('bold')

typeMLabel = Text(Point(23.8,7), "Type:")
typeMLabel.setSize(16)
typeMLabel.setFace(font)
typeMLabel.setStyle('bold')

# titles for julia set controls (iterations, plot type, color scheme)
itersJLabel = Text(Point(68,10), "Iterations:")
itersJLabel.setSize(16)
itersJLabel.setFace(font)
itersJLabel.setStyle('bold')

typeJLabel = Text(Point(65.8,7), "Type:")
typeJLabel.setSize(16)
typeJLabel.setFace(font)
typeJLabel.setStyle('bold')

cLabel = Text(Point(75,2), "C Value:")
cLabel.setSize(14)
cLabel.setFace(font)
cLabel.setStyle('bold')

# virtual size labels for both graphs
virtualSizeLabelM = Text(Point(35,4), "Virtual Size: 10 cm")
virtualSizeLabelM.setSize(14)
virtualSizeLabelM.setFace(font)
virtualSizeLabelM.setStyle('bold')

virtualSizeLabelJ = Text(Point(75,4), "Virtual Size: 10 cm")
virtualSizeLabelJ.setSize(14)
virtualSizeLabelJ.setFace(font)
virtualSizeLabelJ.setStyle('bold')


# ---------------------     CREATE INPUT      -----------------------
itersMEntry = Entry(Point(37,10), 8)
itersMEntry.setText("25")
itersMEntry.undraw()

typeMEntry = DropDown(Point(37,7), ['2Tone (Yellow/Blue)', '2Tone (Purple/Blue)', 'Escape (Sea)', 'Escape (Custom)'], (font, 14), color_rgb(236,236,236))
typeMEntry.undraw()

itersJEntry = Entry(Point(77,10), 7)
itersJEntry.setText("25")
itersJEntry.undraw()

typeJEntry = DropDown(Point(78,7), ['Border (Custom)', 'Inverse (Custom)'], (font, 14), color_rgb(236,236,236))
typeJEntry.undraw()


# ---------------------      CREATE BUTTONS       ------------------------
btnPanel = Button(winTitle, topLeft = Point(115,15.5), width = 3, height = 3,
                 edgeWidth = 2, label = "\u2699\uFE0F",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,18), timeDelay = 0)
btnPanel.activate()

btnQuit = Button(winTitle, topLeft = Point(101,15.5), width = 12, height = 3,
                 edgeWidth = 2, label = "Quit",
                 buttonColors = [color_rgb(232,77,64),color_rgb(232,77,64),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnQuit.activate()
btnQuit.setCaptionStyle('bold')
btnQuit.undraw()

btnClearMandel = Button(winTitle, topLeft = Point(101,10.5), width = 17, height = 3,
                 edgeWidth = 2, label = "Clear Mandelbrot",
                 buttonColors = [color_rgb(241,196,51),color_rgb(241,196,51),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnClearMandel.activate()
btnClearMandel.undraw()

btnClearJulia = Button(winTitle, topLeft = Point(101,5.5), width = 17, height = 3,
                 edgeWidth = 2, label = "Clear Julia",
                 buttonColors = [color_rgb(241,196,51),color_rgb(241,196,51),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnClearJulia.activate()
btnClearJulia.undraw()

btnPlotMandel = Button(winTitle, topLeft = Point(51,11.5), width = 7, height = 3,
                 edgeWidth = 2, label = "Plot",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnPlotMandel.activate()
btnPlotMandel.undraw()

btnZoomInMandel = Button(winTitle, topLeft = Point(51,7.5), width = 3, height = 3,
                 edgeWidth = 2, label = "+",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnZoomInMandel.deactivate()
btnZoomInMandel.undraw()

btnZoomOutMandel = Button(winTitle, topLeft = Point(55,7.5), width = 3, height = 3,
                 edgeWidth = 2, label = "-",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnZoomOutMandel.deactivate()
btnZoomOutMandel.undraw()

btnGetC = Button(winTitle, topLeft = Point(91,11.5), width = 7, height = 3,
                 edgeWidth = 2, label = "Get C",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnGetC.activate()
btnGetC.undraw()

btnZoomInJulia = Button(winTitle, topLeft = Point(91,7.5), width = 3, height = 3,
                 edgeWidth = 2, label = "+",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnZoomInJulia.deactivate()
btnZoomInJulia.undraw()

btnZoomOutJulia = Button(winTitle, topLeft = Point(95,7.5), width = 3, height = 3,
                 edgeWidth = 2, label = "-",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnZoomOutJulia.deactivate()
btnZoomOutJulia.undraw()

btnColorMode = Button(winTitle, topLeft = Point(2,16), width = 3, height = 3,
                 edgeWidth = 2, label = "\U0001F319",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnColorMode.activate()

btnScreenShot = Button(winTitle, topLeft = Point(6,16), width = 3, height = 3,
                 edgeWidth = 2, label = "\U0001F4F7",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnScreenShot.activate()

btnAutoFlush = Button(winTitle, topLeft = Point(10,16), width = 8, height = 3,
                 edgeWidth = 2, label = "AF: OFF",
                 buttonColors = [color_rgb(44,62,79),color_rgb(44,62,79),'white'],
                 clickedColors = ['white','black','black'],
                 font=(font,16), timeDelay = 0)
btnAutoFlush.activate()
btnAutoFlush.undraw()

# create divider lines
div1 = Line(Point(60,1), Point(60,16.5))
div2 = Line(Point(100,1), Point(100,16.5))
div3 = Line(Point(20,1), Point(20,16.5))


# -------------------         MAIN LOOP        -----------------
clickPt = winTitle.getMouse()
while not btnQuit.clicked(clickPt):

    # control panel button
    if btnPanel.clicked(clickPt):
        toggleControlPanel()
    
    # plot mandelbrot button
    elif btnPlotMandel.clicked(clickPt):
        plotMandelbrot()
    
    # get c (plot julia) button
    elif btnGetC.clicked(clickPt):
        winJulia.clear()
        getC()
        # showOrbit()
        plotJulia()
        print("C = ", cVal)
        
    # color mode toggle button
    elif btnColorMode.clicked(clickPt):
        toggleColorMode()

    # zoom in buttons for mandelbrot and julia
    elif btnZoomInMandel.clicked(clickPt):
        updateVirtualSize(zoomIn(winMandel), "Mandelbrot")
        plotMandelbrot()

    elif btnZoomInJulia.clicked(clickPt):
        updateVirtualSize(zoomIn(winJulia), "Julia")
        plotJulia()
    
    # zoom out buttons for mandelbrot and julia
    elif btnZoomOutMandel.clicked(clickPt):
        zoomOut(winMandel)

    elif btnZoomOutJulia.clicked(clickPt):
        zoomOut(winJulia)
    
    # clear buttons for both graphs
    elif btnClearMandel.clicked(clickPt):
        winMandel.clear()
    
    elif btnClearJulia.clicked(clickPt):
        winJulia.clear()
    
    # toggle autoflush buttons 
    elif btnAutoFlush.clicked(clickPt):
        toggleAutoFlush()


    clickPt = winTitle.getMouse()

# close windows if quit button is clicked
winTitle.close()
winMandel.close()
winJulia.close()

# END