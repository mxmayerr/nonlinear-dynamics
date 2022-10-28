# quadratic equation explorer program 
# for NLD 2022/23
# Author: MCM Oct '22
# ======================================================================


import sys
from math import sqrt
sys.path.append("../lib")
from DEgraphics import *

def main():

    # hard coded values i used
    screenWidth = 1440
    appWidth = 1100

    # used later, just created here
    obj = []
    startingVal = -5
    endingVal = 5

    # ------------------------ WINDOWS ----------------------
    # create DE graph win for all 4 windows
    winTitle = DEGraphWin(title = "FUN WITH GRAPHICS", defCoords=[-10,-10,10,10], width = appWidth, height = 100,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2,50], autoflush=True, hBGColor=color_rgb(213,213,213))

    winInfo = DEGraphWin(title = "FUN WITH GRAPHICS", defCoords=[-175,-300,175,300], width = 350, height = 600,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2,150], autoflush=True, hBGColor=color_rgb(213,213,213))

    winGraph = DEGraphWin(title = "FUN WITH GRAPHICS", defCoords=[-30,-25,30,25], width = appWidth-350, height = 600,
    hasTitlebar = False, offsets=[screenWidth/2-appWidth/2 + 350,150], autoflush=False, hBGColor=color_rgb(213,213,213))

    winInput = DEGraphWin(title = "Control Center", defCoords=[-100, -100, 100, 100], width = 300, height = 225,
    hasTitlebar = True, offsets=[500,400], autoflush=True, hBGColor=color_rgb(213,213,213))

    # set backgrounds to white, turn on the axis and set them to grey
    winTitle.setBackground('white')
    winInfo.setBackground('white')
    winGraph.setBackground('white')
    winGraph.updateAxes(0,'grey')
    winGraph.toggleAxes()
    winInput.setBackground('white')

    # ======================= TEXT OBJECTS =========================
    # ------------------------- AXIS LABELS -------------------------
    # x axis
    # for every integer -29-29, draw a line
    # if the integer is a multiple of 5, draw a text object with that integer
    # if it's 0, dont draw it at all
    for i in range(-29,29):
        if i % 5 == 0:
            l = Line(Point(i,-0.75), Point(i,0.75))
            if i != 0:
                t = Text(Point(i,-1.5), i)
                t.draw(winGraph)
        else:
            l = Line(Point(i,-0.35), Point(i,0.35))
        l.draw(winGraph)
    
    # now the same for the y axis
    for i in range(-24,24):
        if i % 5 == 0:
            l = Line(Point(-0.75,i), Point(0.75,i))
            if i != 0:
                t = Text(Point(1.5,i), i)
                t.draw(winGraph)
        else:
            l = Line(Point(-0.35,i), Point(0.35,i))
        l.draw(winGraph)

    # ----------------- A, B, AND C TEXT AND ENTRIES -------------------
    # create entries for a, b, and c
    aText = Text(Point(-63, 60), "A = ")
    aText.setStyle('bold')
    aText.setSize(16)
    aText.setOutline(color_rgb(35,110,150))
    aText.draw(winInput)

    aEntry = DblEntry(Point(-25,60), width = 10, span = [-100,100],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    aEntry.draw(winInput)

    bText = Text(Point(-63, 30), "B = ")
    bText.setStyle('bold')
    bText.setSize(16)
    bText.setOutline(color_rgb(35,110,150))
    bText.draw(winInput)

    bEntry = DblEntry(Point(-25,30), width = 10, span = [-100,100],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    bEntry.draw(winInput)

    cText = Text(Point(-63, 0), "C = ")
    cText.setStyle('bold')
    cText.setSize(16)
    cText.setOutline(color_rgb(35,110,150))
    cText.draw(winInput)

    cEntry = DblEntry(Point(-25, 0), width = 10, span = [-100,100],
                       colors = ['gray','white'],
                       errorColors = ['red','white'])
    cEntry.draw(winInput)

    # ----------------------- TITLE TEXT ----------------------------------
    # create title text and description text

    titleText = Text(Point(0,2), "Quadratic Equation Demonstration")
    titleText.setSize(36)
    titleText.setStyle('bold')
    titleText.setFace('verdana')
    titleText.draw(winTitle)

    instructionText = Text(Point(0,-5),"Welcome to the Quadratic Equation Demonstration created by Max Mayer '23. To begin, enter values for A, B, and C in the control panel, then hit \'plot\'.")
    instructionText.setSize(14)
    instructionText.setFace('verdana')
    instructionText.draw(winTitle)

    # ---------------------- INFO PANEL TITLE --------------------------------
    # info panel title
    infoTitle = Text(Point(0,275), "Graph Info")
    infoTitle.setStyle('bold')
    infoTitle.setSize(25)
    infoTitle.setFace('verdana')
    infoTitle.draw(winInfo)

    # -------------------- A, B, C HEADERS ------------------------
    # text labels for entries a,b, and c
    aEntryDis = Text(Point(0,225), "A = ")
    aEntryDis.setSize(20)
    aEntryDis.setFace('verdana')
    bEntryDis = Text(Point(0,200), "B = ")
    bEntryDis.setSize(20)
    bEntryDis.setFace('verdana')
    cEntryDis = Text(Point(0,175), "C = ")
    cEntryDis.setSize(20)
    cEntryDis.setFace('verdana')
    aEntryDis.draw(winInfo)
    bEntryDis.draw(winInfo)
    cEntryDis.draw(winInfo)

    # ------------------- GRAPH METRICS ------------------
    # make the text for the metrics vertex, roots, equation
    vertexT = Text(Point(0,125), "Vertex: ")
    vertexT.setSize(19)
    vertexT.setStyle('bold')
    vertexT.setFace('verdana')
    vertexT.draw(winInfo)

    rootT = Text(Point(0,75), "Real Roots: ")
    rootT.setSize(19)
    rootT.setStyle('bold')
    rootT.setFace('verdana')
    rootT.draw(winInfo)

    eqText = Text(Point(0,25),' Equation: Ax\u00b2+Bx+C')
    eqText.setSize(19)
    eqText.setStyle('bold')
    eqText.setFace('verdana')
    eqText.draw(winInfo)

    # ------------------ PLOTTING INFO -------------------
    # button information in the info panel
    # create a divider line to span the panel
    divider = Line(Point(-160,0), Point(160,0))
    divider.draw(winInfo)

    # crete info text
    infoT = Text(Point(0,-25), "Button Info")
    infoT.setStyle('bold')
    infoT.setSize(25)
    infoT.setFace('verdana')
    infoT.draw(winInfo)

    infoB1 = Text(Point(0,-70), "Reset: clears graph and numbers")
    infoB1.setSize(20)
    infoB1.setFace('verdana')
    infoB1.draw(winInfo)

    infoB2 = Text(Point(0,-105), "Zoom: zooms the graph")
    infoB2.setSize(20)
    infoB2.setFace('verdana')
    infoB2.draw(winInfo)

    infoB3 = Text(Point(0,-150), "After clicking the zoom button, you \n click on two points on the graph \n then click the rectangle to zoom.")
    infoB3.setSize(18)
    infoB3.setFace('verdana')
    infoB3.draw(winInfo)

    infoB4 = Text(Point(0,-210), "Learn More: learn more")
    infoB4.setSize(20)
    infoB4.setFace('verdana')
    infoB4.draw(winInfo)

    # ========================= BUTTONS ======================= 
    # --------------------- SHUT DOWN BUTTON --------------------------------
    # create button to shut down
    btnClose = Button(winInput, topLeft = Point(40,-40), width = 50, height = 30,
                 edgeWidth = 2, label = 'QUIT',
                 buttonColors = [color_rgb(243,135,47),color_rgb(243,135,47),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)

    btnClose.activate()

    # -------------------- VALUE RESET BUTTON -----------------------
    # create button to reset values
    btnReset = Button(winInput, topLeft = Point(40,10), width = 50, height = 30,
                 edgeWidth = 2, label = 'RESET',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    
    btnReset.activate()

    # ------------------------ PLOT BUTTON  -------------------------------
    # create button to plot graph
    btnPlot = Button(winInput, topLeft = Point(40,50), width = 50, height = 30,
                 edgeWidth = 2, label = 'PLOT',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    
    btnPlot.activate()

    # ----------------- GRAPH AXES & ZOOM BUTTONS ---------------------
    # zoom buttons
    btnZoomIn = Button(winInput, topLeft = Point(66,90), width = 24, height = 30,
                 edgeWidth = 2, label = '+',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)

    btnZoomOut = Button(winInput, topLeft = Point(40,90), width = 24, height = 30,
                 edgeWidth = 2, label = '-',
                 buttonColors = [color_rgb(21,178,211),color_rgb(21,178,211),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)

    # ------------------------ HELP BUTTON ---------------------------
    btnHelp = Button(winInput, topLeft = Point(-85,-40), width = 105, height = 30,
                 edgeWidth = 2, label = 'Learn More',
                 buttonColors = [color_rgb(255,215,0),color_rgb(255,215,0),'white'],
                 clickedColors = ['white','red','black'],
                 font=('courier',18), timeDelay = 0.05)
    btnHelp.activate()

    # ======================= ACTIVE LOOP ============================
    # the followeing in the while loop will run until the quit button is clicked
    # get click input
    clickPt = winInput.getMouse() #returns a point object

    # when arent clicking the quit button
    while not btnClose.clicked(clickPt):

        # -------------- PLOT BUTTON -----------
        # if click on the plot button
        if btnPlot.clicked(clickPt):
                # clear graph
            winGraph.clear()
            winGraph.flush()

            # update the values to the entreis
            a = aEntry.getValue()
            aEntryDis.setText("A = " + str(a))
            b = bEntry.getValue()
            bEntryDis.setText("B = " + str(b))
            c = cEntry.getValue()
            cEntryDis.setText("C = " + str(c))

            # update metrics
            # update vertex with the function
            vertex = findVertex(a,b,c)
            vertexT.setText("Vertex: " + formatVertex(vertex))

            # update roots with the funciton
            rootsArr = findRoots(a,b,c)
            rootT.setText("Real Roots: " + formatRoots(rootsArr))

            # update equation with the values a,b and c 
            eqText.setText('Equation: ' + str(a) + 'x\u00b2' + '+' + str(b) + 'x' + '+' + str(c))

            # flush the window to refresh
            winInfo.flush()

            # if the line is linear, increase the starting and ending val to -30 - 30 (to encapsulate the whole screen)
            if a == 0:
                startingVal = -30
                endingVal = 30

            # plot the values for domain increasing by 0.001
            x = startingVal
            while x < endingVal:
                winGraph.plot(x,a * x * x + b * x + c, color='red')
                x += 0.001
            
            # then put the values back to what they were
            startingVal = -5
            endingVal = 5

            # clear existing circles for roots and vertex
            for o in obj:
                o.undraw()
            obj = []

            # make root circles on the graph
            # for every root in the roots array, plot the circle and add it to the array obj
            # obj keeps circles in memory so we can delete them later
            for i in rootsArr:
                cir = Circle(Point(i,0),0.25)
                cir.setFill('yellow')
                cir.draw(winGraph)
                obj.append(cir)


            # make vertex point
            # do the same as above with vertex, just majke sure a isnt 0 since it wouldnt have a vertex
            if a != 0:
                cir = Circle(Point(vertex[0], vertex[1]), 0.25)
                cir.setFill('black')
                cir.draw(winGraph)
                obj.append(cir)
    
            # since we plot the graoh, activate the zoom in buttion
            btnZoomIn.activate()

        # ------------ ZOOM BUTTONS --------------
        # if we clickon the zom button, zoom in and regraph the function
        if (btnZoomIn.clicked(clickPt)):
            winGraph.zoom(ZOOM_IN)
            x = startingVal
            while x < endingVal:
                winGraph.plot(x,a * x * x + b * x + c, color='red')
                x += 0.001
            # since we zoomed in, we can activate the zoom out button
            btnZoomOut.activate()

        # otherwise, if zoom out is clicked, zoom out and replot again
        elif (btnZoomOut.clicked(clickPt)):
            winGraph.zoom(ZOOM_OUT)
            x = startingVal
            while x < endingVal:
                winGraph.plot(x,a * x * x + b * x + c, color='red')
                x += 0.001
            # we must deactivate the zoom out button since we cant zoom out more then once at a time
            # (until we click the zoom in button again)
            btnZoomOut.deactivate()

        # ------------ LEARN MORE WINDOW ----------------
        # if click on the learn more button
        if (btnHelp.clicked(clickPt)):
            # display help window
            winHelp = DEGraphWin(title = "Learn More - Quadratic Equation Explorer", defCoords=[-350,-400,350,400], width = 700, height = 800,
            hasTitlebar = True, offsets=[screenWidth/2-appWidth/2,50], autoflush=True)

            winHelp.setBackground('white')

            # add the text to the window
            helpTitle = Text(Point(0,370), "Learn more about the Quadratic Equation Explorer")
            helpTitle.setStyle('bold')
            helpTitle.setSize(28)
            helpTitle.draw(winHelp)

            helpIntroductionTitle = Text(Point(-260, 340), "Introduction")
            helpIntroductionTitle.setStyle('bold')
            helpIntroductionTitle.setSize(23)
            helpIntroductionTitle.draw(winHelp)

            helpIntroductionBody = Text(Point(0,275), "The quadratic equation in it's most general form is:\n Ax^2 + Bx + C\n where A, B, and C are real numbers. In this program, A, B, and C are given by the user. \n These values determine how the graph looks and behaves on the graph screen.")
            helpIntroductionBody.setSize(18)
            helpIntroductionBody.draw(winHelp)

            helpRootsTitle = Text(Point(-130, 210), "Roots and Stuff of Quadratic Equation")
            helpRootsTitle.setStyle('bold')
            helpRootsTitle.setSize(23)
            helpRootsTitle.draw(winHelp)

            helpRootsBody = Text(Point(0,125), "A root is where the graph crosses the x-axis. A typical quadratic equaiton \n can have either zero, one, or two real roots. To determine the real roots, use: \n discriminant = B^2 - 4AC \n If the discriminant is positive, the equaiton has two real roots. If the discriminant \n is exactly 0, there is a single real root, and if it is negtive, the eqiaiton \n has no real roots (never touches x axis). Additionally, you can compute metrics like \n the vertex or the inflection points using their respective formulas. ")
            helpRootsBody.setSize(18)
            helpRootsBody.draw(winHelp)

            helpHowTitle = Text(Point(-190, 40), "How to Use This Program")
            helpHowTitle.setStyle('bold')
            helpHowTitle.setSize(23)
            helpHowTitle.draw(winHelp)

            helpHowBody = Text(Point(0,-55), "The quadratic equation is solely based off values A, B, and C. Therefore, \n you can easily enter various vales for A, B, and C on the Control Panel window. \n After you enter values, make sure to click the \'plot\' button which updates the graphs \n and the metrics in the Graph Info section. If you'd like to clear the graph, click on the \n \'clear\' button. This will reset A,B,C values to default value (1) and will \n clear the graph. You can use the \'+\' and \'-\' icons to zoom in and out of \n your graph in the graphing window. At any time, you can click on the \'quit\' \n button to close the program Beware: you will lose your current graph and metrics.")
            helpHowBody.setSize(18)
            helpHowBody.draw(winHelp)

            helpProblemsTitle = Text(Point(-200, -150), "Running Into Problems?")
            helpProblemsTitle.setStyle('bold')
            helpProblemsTitle.setSize(23)
            helpProblemsTitle.draw(winHelp)

            helpProblemsBody = Text(Point(0,-215), "If you are running into issues with the program, try the following steps: \n 1. Use the \'reset\' button. Warning: this will delete your current values. \n 2. Quit and re-open the program. Agaain, you will lose your current values. \n 3. Quit button doesnt work? Use the red \'x\' in the top corner of the Control Panel window. \n 4. Contact Max for help.")
            helpProblemsBody.setSize(18)
            helpProblemsBody.draw(winHelp)

            helpFinal = Text(Point(0,-300), "Ready to close this window? Click on the red \'x\' in the top corner. \n You can reopen this window anytime by clicking \'Learn More\' on the Control Panel.\n Happy Graphing!")
            helpFinal.setSize(17)
            helpFinal.setStyle('bold')
            helpFinal.draw(winHelp)

        # -------------- RESET BUTTONS -----------------
        # if we click on the reset button
        if btnReset.clicked(clickPt):
            # set a,b, and c to 1 (default value)
            a = 1
            aEntryDis.setText("A = ")
            b = 1
            bEntryDis.setText("B = ")
            c = 1
            cEntryDis.setText("C = ")

            # reset the metric text for vertex, root, and equation
            vertexT.setText("Vertex: ")
            rootT.setText("Real Roots: ")
            eqText.setText("Equation: ")

            # deactivate the zoom buttons and zoom out to normal scale
            btnZoomOut.deactivate()
            btnZoomIn.deactivate()
            winGraph.zoom(ZOOM_OUT)

            # clear and refresh the window
            winGraph.clear()
            winInfo.flush()

            # undraw all the circles we made earlier
            for o in obj:
                o.undraw()
            obj= []

        # get click point object again
        clickPt = winInput.getMouse()
    
    winTitle.close()

# methods to help out with some of the math

# format roots formats the roots to my needs for printing on the panel
def formatRoots(roots):
    # if the roots array is 0, we have no roots and return no real roots
    if len(roots) == 0:
        return "No Real Roots"
    # otherwise, for all the roots we have, format them and add them to a string which we return later
    s = ""
    for i in range(len(roots)):
        if i == 1:
            s+=", "
        s = s + "x = " + str(round(roots[i],2))
    return s

# plot circles takes roots array and plots circles at the x value of those metrics
def plotCircles(roots):
    for i in roots:
        cir = Circle(Point(i,0),0.75)
        cir.draw(winGraph)
                
# find vertex takes a,b,c and finds the vertex
# retrurns a string of No Vertex if there isnt a vertex (a == 0)
def findVertex(a,b,c):
    if a == 0:
        return ["No Vertex"]
    x =  (-b / (2 * a))
    y = (((4 * a * c) - (b * b)) / (4 * a)) 
    return [x,y]

# format vertex takes an array of vertex and formats it to my needs for printing
def formatVertex(vertex):
    # if its a string, meaning findVertex returns "no vertex", return no vertex
    if isinstance(vertex, str) or len(vertex) < 2:
        return "No Vertex"
    # otherwise, format the vertex for printing
    else:
        return "(" + str(vertex[0]) + "), (" + str(vertex[1]) + ")"

# find roots finds the roots of a quadratic equation and adds them to a list
# if there are no roots or fake roots, it returns an empty list
def findRoots(a,b,c):
    # create list of roots
    roots = []
    # if we would get a divide 0 error or a and b are 0, handle those cases
    if a == 0 and b != 0:
        roots = [-c/b]
        return roots
    elif a == 0 and b == 0:
        return roots

    # else, calculate the roots like normal
    r = b**2 - 4*a*c

    if r > 0:
        x1 = (((-b) + sqrt(r))/(2*a))     
        x2 = (((-b) - sqrt(r))/(2*a))
        roots.append(x1)
        roots.append(x2)
        return roots
    elif r == 0:
        x = (-b) / 2*a
        roots.append(x)
        return roots
    else:
        return roots


# run main
if __name__ == "__main__":
    main()







