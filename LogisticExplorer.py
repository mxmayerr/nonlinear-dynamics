# Logistic Map Explorer
# 
# Written by MCM in 2023

# import modules (i cant use numpy for some reason idk)
import random
import sys
sys.path.append("../lib")
from DEgraphics import *


# main method
def main():

    # create windows and store them inside a list
    windows = createWindows()
    # get info from initialize funciton
    arr = initializeWindows(windows)
    # objects is a listt of buttons and entries 
    objects = arr[0]
    # helpBtns is a array of help buttons
    helpBtns = arr[1]
    # to better understant the contents of the above lists:

    # WINDOWS LIST:
    # 0. Title
    # 1. Input
    # 2. Bifurcation
    # 3. Cobweb
    # 4. Time

    # OBJECTS LIST:
    # 0. Cobweb Plot
    # 1. Bifurcation Plot
    # 2. Bifurcation Zoom +
    # 3. Bifurcation Zoom -
    # 4. Cobweb Zoom +
    # 5. Cobweb Zoom -
    # 6. Clear
    # 7. Quit
    # 8. Iterations Entry (int, 0-100)
    # 9. Transient Entry (int, 0-1000)
    # 10. R-Value Entry (dbl, 1-4)
    # 11. Get R 
    # 12. X0 Entry (dlb, 0-1)
    # 13. Get Random

    # HELP LIST:
    # easier to remember, just a list from top to bottom of buttons

    # run the main loop and pass the above lists
    mainLoop(windows, objects, helpBtns)

# ---------- METHODS ---------------

# method to create windows with no content at my specifications
def createWindows():
    # hard coded values I use
    screenWidth = 1440
    appWidth = 1100

    # create title window
    winTitle = DEGraphWin(title = "Title Window", defCoords=[-10,-10,10,10], width = appWidth, height = 100,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2,30], autoflush=True, hBGColor=color_rgb(213,213,213))

    # create input window
    winInput = DEGraphWin(title = "Input Window", defCoords=[0,0,350,300], width = 350, height = 300,
    hasTitlebar = True, offsets=[screenWidth/2-appWidth/2,130], autoflush=True, hBGColor=color_rgb(213,213,213))

    # create main window 
    winBi = DEGraphWin(title = "Graph Window", defCoords=[0.8,-0.2,4, 1], width = appWidth-350, height = 330,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2 + 350,130], autoflush=False, hBGColor=color_rgb(213,213,213))

    # create cobweb diagram window
    winCob = DEGraphWin(title = "Graph Window", defCoords=[-0.1,-0.1,1.1,1.1], width = appWidth/2, height = 300,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2,460], autoflush=False, hBGColor=color_rgb(213,213,213))
    
    # create time series window
    winTime = DEGraphWin(title = "Graph Window", defCoords=[-30,-25,30,25], width = appWidth/2, height = 300,
    hasTitlebar = False, offsets=[screenWidth/2,460], autoflush=False, hBGColor=color_rgb(213,213,213))

    # set all backgrounds to white
    winTitle.setBackground('white')
    winInput.setBackground('white')
    winBi.setBackground('white')
    winCob.setBackground('white')
    winTime.setBackground('white')

    # make x axis on bifurcation diagram
    l = Line(Point(0.8, 0), Point(4,0))
    l.draw(winBi)
    i = 0.8
    while i <= 4:
        l = Line(Point(i, 0.02), Point(i, -0.02))
        l.draw(winBi)
        t = Text(Point(i,-0.03), round(i, 1))
        t.draw(winBi)
        i+=0.2

    # make axis on the cobweb diagram
    winCob.updateAxes(0,'grey')
    winCob.toggleAxes()
    # x
    i = 0.2
    while i <= 1:
        l = Line(Point(i, 0.02), Point(i, -0.02))
        l.draw(winCob)
        t = Text(Point(i,-0.03), round(i, 1))
        t.draw(winCob)
        i+=0.2
    # y
    i = 0.2
    while i <= 1:
        l = Line(Point(-0.01, i), Point(0.01, i))
        l.draw(winCob)
        t = Text(Point(-0.03, i), round(i, 1))
        t.draw(winCob)
        i+=0.2


    # return the windows in a list format
    return [winTitle, winInput, winBi, winCob, winTime]

# method to fill windows with needed buttons, text, inputs, etc
def initializeWindows(windows):

    # create array to hold entries and buttons
    objects = []
    helpBtns = []

    # ----------- TITLE WINDOW ---------------
    # create title text and instruction text
    titleText = Text(Point(0,2), "Logistic Map Explorer")
    titleText.setSize(36)
    titleText.setStyle('bold')
    titleText.setFace('verdana')
    titleText.draw(windows[0])

    # description text
    instructionText = Text(Point(0,-5),"Welcome to the Logistic Map Explorer created by Max Mayer '23. Click the \"?\" icons to learn more.")
    instructionText.setSize(14)
    instructionText.setFace('verdana')
    instructionText.draw(windows[0])

    # ---------------- Graph Option Section Buttons ---------------
    # when we create the button, we append it to the objects array

    # bufurcation plot button
    bifurcationPlotBtn = Button(windows[1], topLeft = Point(40,280), width = 220, height = 30,
                 edgeWidth = 2, label = 'Bifurcation Diagram',
                 buttonColors = [color_rgb(255,215,0),color_rgb(255,215,0),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    bifurcationPlotBtn.activate()

    # create bifurcation  help button
    b = helpButton(15,265,windows[1])
    helpBtns.append(b)
    b.activate()

    # cobweb plot button
    cobwebPlotBtn = Button(windows[1], topLeft = Point(40,240), width = 220, height = 30,
                 edgeWidth = 2, label = 'Cobweb / Time Series',
                 buttonColors = [color_rgb(255,215,0),color_rgb(255,215,0),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    cobwebPlotBtn.activate()
    objects.append(cobwebPlotBtn)
    # this may seem weird but i messed up the ordering and adding it after cobweb butten is less work
    objects.append(bifurcationPlotBtn)

    # create cobweb help button
    b = helpButton(15,225,windows[1])
    helpBtns.append(b)
    b.activate()


    # create zoom buttons for bifurcation and cobweb diagram:
    # we dont activate these buttons yet, since if the user clicks on them without content in the window, we get error
    btnZoomInBi = Button(windows[1], topLeft = Point(270,280), width = 30, height = 30,
                 edgeWidth = 2, label = '+',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    objects.append(btnZoomInBi)

    btnZoomOutBi = Button(windows[1], topLeft = Point(304,280), width = 30, height = 30,
                 edgeWidth = 2, label = '-',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    objects.append(btnZoomOutBi)

    btnZoomInCob = Button(windows[1], topLeft = Point(270,240), width = 30, height = 30,
                 edgeWidth = 2, label = '+',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    objects.append(btnZoomInCob)

    btnZoomOutCob = Button(windows[1], topLeft = Point(304,240), width = 30, height = 30,
                 edgeWidth = 2, label = '-',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    objects.append(btnZoomOutCob)

    # button to clear graph
    btnClear = Button(windows[1], topLeft = Point(190,200), width = 64, height = 30,
                 edgeWidth = 2, label = 'Clear',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    objects.append(btnClear)
    
    # quit button
    btnQuit = Button(windows[1], topLeft = Point(270,200), width = 64, height = 30,
                 edgeWidth = 2, label = 'Quit',
                 buttonColors = [color_rgb(239,66,29),color_rgb(239,66,29),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    btnQuit.activate()
    objects.append(btnQuit)

    # -------------- Inputs Section ---------------
    # create line to divide 
    divider = Line(Point(10,155), Point(340,155))
    divider.draw(windows[1])

    # display iterations
    # create placeholder text
    iterationsText = Text(Point(145,135), "Display Iterations = ")
    iterationsText.setSize(18)
    iterationsText.setFace('verdana')
    # create the entry
    iterationsEntry = IntEntry(Point(280,135), width = 10, span = [0,500],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    iterationsText.draw(windows[1])
    iterationsEntry.draw(windows[1])
    iterationsEntry.setDefault(10)
    # add entry to list
    objects.append(iterationsEntry)
    # create the help button
    iterationsHelpBtn = helpButton(32,135,windows[1])
    iterationsHelpBtn.activate()
    # add help button to respected list
    helpBtns.append(iterationsHelpBtn)

    # repeat the process above for other entries:

    # transient iterations
    transientText = Text(Point(145,100), "Transient Iterations = ")
    transientText.setSize(18)
    transientText.setFace('verdana')

    transientEntry = IntEntry(Point(295,100), width = 10, span = [0,500],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    transientText.draw(windows[1])
    transientEntry.draw(windows[1])
    transientEntry.setDefault(0)
    objects.append(transientEntry)

    transientHelpBtn = helpButton(22,100,windows[1])
    transientHelpBtn.activate()
    helpBtns.append(transientHelpBtn)

    # r values entries
    rvalueText = Text(Point(105,65), "R - Value = ")
    rvalueText.setSize(18)
    rvalueText.setFace('verdana')

    rvalueEntry = DblEntry(Point(205,65), width = 10, span = [1,4],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    rvalueText.draw(windows[1])
    rvalueEntry.draw(windows[1])
    rvalueEntry.setDefault(2)
    objects.append(rvalueEntry)

    rvalueHelpBtn = helpButton(30,65,windows[1])
    rvalueHelpBtn.activate()
    helpBtns.append(rvalueHelpBtn)

    # here, we are adding a get r button
    getrBtn = Button(windows[1], topLeft = Point(255,77), width = 64, height = 24,
                 edgeWidth = 2, label = 'Get R',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    getrBtn.activate()
    objects.append(getrBtn)

    # x0 value entry
    x0valueText = Text(Point(110,30), "X\u2080 - Value = ")
    x0valueText.setSize(18)
    x0valueText.setFace('verdana')

    x0valueEntry = DblEntry(Point(205,30), width = 10, span = [0,1],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    x0valueText.draw(windows[1])
    x0valueEntry.draw(windows[1])
    x0valueEntry.setDefault(0.25)
    objects.append(x0valueEntry)

    # again, we are adding a get random x0 button
    x0valueHelpBtn = helpButton(30,30,windows[1])
    x0valueHelpBtn.activate()
    helpBtns.append(x0valueHelpBtn)

    randBtn = Button(windows[1], topLeft = Point(255,42), width = 70, height = 24,
                 edgeWidth = 2, label = 'Random',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    randBtn.activate()
    objects.append(randBtn)

    # return the objects and help buttons lists
    return [objects,helpBtns]
     
# default help button function, returns the button
def helpButton(x, y, window):
    helpBtn = Button(window, topLeft = Point(x,y+7.5), width = 15, height = 15,
                 edgeWidth = 2, label = '?',
                 buttonColors = [color_rgb(243,135,47),color_rgb(243,135,47),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    return helpBtn

# main loop function takes all lists from above
def mainLoop(windows, objects, helpBtns):

    # create these lists for use later
    lines = [] # (for cobweb diagram clearing)
    rl = [] # (for get r line clearing)

    # get a click on input window
    clickPt = windows[1].getMouse()
    # while we arent clicking on the quit button
    while not objects[7].clicked(clickPt):

        # ------- if help buttons are clicked ---------
        # if bifurcation diagram is clicked
        if helpBtns[0].clicked(clickPt):
            win = createHelpWin("Bifurcation Help", "This shows possible R\n values on the x-axis and\n their orbits on the y\n axis. In other words,\n the orbit is the amount\n of times a vertical line\n intersects the graph at\n a certain x (r) value.")
            win.setBackground('white')

        # if cobweb plot is clicked
        if helpBtns[1].clicked(clickPt):
            win = createHelpWin("Cobweb and Time Series Help", "Cobweb diagram shows the\n behavior of the map at\ngiven r and x0 value. A\ntime series graph shows\niterations on the x-axis\n and the value at that\niteration on the y-axis.")
            win.setBackground('white')

        # if display iterations is clicked
        if helpBtns[2].clicked(clickPt):
            win = createHelpWin("Display Iteration Help", "This is the amount of \n iterations to display on  \n on the cobweb diagram. \n Play around with this \n value to see new \n combinations!")
            win.setBackground('white')
        
        # if transient iterations help is clicked
        if helpBtns[3].clicked(clickPt):
            win = createHelpWin("Transient Iteration Help", "This is the amount pf \n iterations used to \n calculate x0 value \n before plotting iterations. \n In other words, this \n is the number of \n iterations that are \n not being shown.")
            win.setBackground('white')

        # if r value help is clicked
        if helpBtns[4].clicked(clickPt):
            win = createHelpWin("R-Value Help", "The R-Value is a \n variable in the logistic \n equation. Play around \n with different R-Values \n or use the \'Get R\' button \n and click on the \n bifurcation diagram to \n get a value.")
            win.setBackground('white')
        
        # if x0 value help is clicked
        if helpBtns[5].clicked(clickPt):
            win = createHelpWin("X0-Value Help", "This is the starting \n x-value for the cobweb \n diagram. Play with values \n to find interesting X0 \n points.")
            win.setBackground('white')

        # if the bifurcation plot button is clicked
        if objects[1].clicked(clickPt):
            # call bifurcation function and pass it graph window (to graph) and input window (to draw loading text)
            plotBifurcation(windows[2], windows[1])
            # activate the bifurcation zoom and clear buttons
            objects[2].activate()
            objects[6].activate()

        
        # if bifurcation zoom in button is clicked
        if objects[2].clicked(clickPt):
            # zoom in
            windows[2].zoom(ZOOM_IN)
            # replot bifurcation
            plotBifurcation(windows[2], windows[1])
            # activate the zoom out button
            objects[3].activate()

        # if bifurcation zoom out is clicked
        if objects[3].clicked(clickPt):
            # zoom out
            windows[2].zoom(ZOOM_OUT)
            # replot bifurcation
            plotBifurcation(windows[2], windows[1])
            # deactivate both zomo buttons
            objects[2].deactivate()
            objects[3].deactivate()
        
        # get r button
        if objects[11].clicked(clickPt):
            # for line in rl, undraw it and reset rl to empty array (removing previous line)
            for l in rl:
                l.undraw()
            rl = []
            # get the x coord in the bifurcation window
            x = windows[2].getMouse().getX()
            # set the text/value of the r entry to x
            objects[10].setText(x)
            # create verticle line , draw it in graph, and append to rl list (so we can remove it later)
            l = Line(Point(x,0.98), Point(x,0.02))
            l.setFill('red')
            rl.append(l)
            l.draw(windows[2])
        
        # get random x0 button
        if objects[13].clicked(clickPt):
            # set text/value to a random between 0 and 1
            objects[12].setText(random.uniform(0,1))


        
        # if plot cobweb and time series
        if objects[0].clicked(clickPt):
            # plot cobweb with arguments window, iterations, r value, x0, lines array, and transient value)
            plotCobweb(windows[3], objects[8].getValue(), objects[10].getValue(), objects[12].getValue(), lines, objects[9].getValue())
            # activate cobweb zoom in and clear button
            objects[4].activate()
            objects[6].activate()
            # then, plot the time series with arguments window, iterations, r
            plotTimeSeries(windows[4], objects[8].getValue(), objects[10].getValue(), objects[12].getValue(), objects[9].getValue())
        
        # if cobweb zoom in is slicked
        if objects[4].clicked(clickPt):
            # zoom in
            windows[3].zoom(ZOOM_IN)
            # replot cobweb
            plotCobweb(windows[3], objects[8].getValue(), objects[10].getValue(), objects[12].getValue(), lines, objects[9].getValue())
            # activate cobweb zoom button
            objects[5].activate()

        # if cobweb zoom out is clicked
        if objects[5].clicked(clickPt):
            # zoom out
            windows[3].zoom(ZOOM_OUT)
            # replot cobweb
            plotCobweb(windows[3], objects[8].getValue(), objects[10].getValue(), objects[12].getValue(), lines, objects[9].getValue())
            # activate zoom in, deactivate zoom out
            objects[4].activate()
            objects[5].deactivate()

        
        # if clear button is clicked
        if objects[6].clicked(clickPt):
            # clear all windows
            windows[2].clear()
            windows[3].clear()
            windows[4].clear()
            # deactivte clear button
            objects[6].deactivate()
            # remove any lines in lines (from cobweb or get r)
            for l in lines:
                l.undraw()
            l = []
            for l in rl:
                l.undraw()
            rl = []
        
        # get click point again
        clickPt = windows[1].getMouse()

    # close the window if quit button is clicked
    windows[1].close()

# function to create a help window with given tltle and text, returns the window
def createHelpWin(title, text):
    win = DEGraphWin(title = title, defCoords=[0,0,200,200], width = 250, height = 200,
    hasTitlebar = True, offsets=[500,200], autoflush=False, hBGColor=color_rgb(213,213,213))
    t = Text(Point(100,100), text)
    t.setSize(18)
    t.setFace('verdana')
    t.draw(win)
    return win

# plot bifurcation function draws the graph on graph win and draws loading on input win
def plotBifurcation(graphWin, inputWin):
    # draw loading to input win
    t = Text(Point(85,185), "Loading...")
    t.setSize(18)
    t.setFace('verdana')
    t.setFill('red')
    t.setStyle('bold')
    t.draw(inputWin)
    # set transient length to 400 (i found was best balance between time and graph defenition)
    transientLength = 400
    # set r to 0
    r = 0
    # while r is less then 3.5
    while r <= 3.5:
        # get a random in a random range
        x = random.uniform(random.random(),random.random())
        # for i in the range of the transient 
        for i in range(transientLength):
            # calculate the value of the logistic function
            x = r * x * (1-x)
        # plot to graph win
        graphWin.plot(r,x)
        # increment r
        r += 0.0005
    # for r = 3.5 -> 4, we do the same as above just with a smaller iterate so we get more HD
    while r <= 4:
        x = random.uniform(random.random(),random.random())
        for i in range(transientLength):
            x = r * x * (1-x)
        graphWin.plot(r,x)
        r += 0.00001
    # undraw the loading text
    t.undraw()

# function to plot cobweb function in given window with given arguments, adds lines to a lines list 
def plotCobweb(window, iterations, r, x0, lines, transient):
    # clear window first
    window.clear()
    # we need to remove previous lines first
    for l in lines:
        l.undraw()
    l = []
    # first thing we need to do is plot the steady state lime
    x = -0.5
    while x <= 1.5:
        window.plot(x,x)
        x+=0.001
    # then, we need to plot the logistic function with given r value
    x = -0.5
    while x <= 1.5:
        window.plot(x,logisticFunction(x,r))
        x+=0.001
    # then, we need to iterate the transients iterations
    i = 0
    x = x0
    while i < transient:
        x = logisticFunction(x,r)
        i+=1
    # now that we iterated the transient, we can start to dysplay the visual iterations
    i = 0
    y = 0
    while i < iterations:
        # vertical line has the same x value, different y values
        l = Line(Point(x,y), Point(x,logisticFunction(x,r)))
        l.setFill('red')
        lines.append(l)
        l.draw(window)
        y = logisticFunction(x,r)

        # sideways line has different x values, same y value
        l = Line(Point(x,y), Point(y,y))
        l.setFill('blue')
        lines.append(l)
        l.draw(window)
        x = y

        # increment i by one
        i+=1

# function to plot time series graph in given window 
def plotTimeSeries(window, iters, r, x0, transient):
    # clear the previous graph
    window.clear()
    # set coords to shpw up nicely with the given values
    window.setCoords(0,0,iters,1)
    # then, plot the iterations on the x with the function value on the y
    # initialize x to x0 and t to 0
    t = 0
    x = x0
    # time to calculare the transient iterations
    # while t is less then transient, x = logistic function, then increment t by 1
    while t < transient:
        x = r * x * (1-x)
        t+=1
    # reset t to 0 for real iterations
    t = 0
    # same as above, just increment t by 0.001
    while t <= iters:
        window.plot(t,x)
        x = r * x * (1 - x)
        t+=0.001

# returns the value of the logistic function at x with parameter r
def logisticFunction(x,r):
    return r * x * (1-x)

# run the main function
if __name__ == "__main__":
    main()