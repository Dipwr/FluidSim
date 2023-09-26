import copy
import arcade
import math

class cell:
    def __init__(self):
        self.x = 0
        self.y = 0
		
        self.den = 0
		
        self.velX = 0
        self.velY = 0

width = 25
height = 25
grid = []

windowWidth = 500
windowHeight = 500


diffuseSpeed = 0.5

for i in range(height):
    grid.append([])
    for j in range(width):
        grid[i].append(cell())
        grid[i][j].x = j
        grid[i][j].y = i

def lerp(a,b,k):
    return a + (k * (b - a))

def diffuse(ks, precision):
    global grid

    gridC = [[copy.copy(cell_obj) for cell_obj in line] for line in grid]
    gridN = [[copy.copy(cell_obj) for cell_obj in line] for line in grid]
    
    for i in range(height):
        for j in range(width):
            gridN[i][j].den = 0

    for x in range(precision):
        gridNT = [[copy.copy(cell_obj) for cell_obj in line] for line in gridN]
        for i in range(height):
            for j in range(width):
                sd = []
                if gridN[i][j].x != (width-1):
                    sd.append(gridNT[i][j+1].den)
                if gridN[i][j].x != 0:
                    sd.append(gridNT[i][j-1].den)
                if gridN[i][j].y != (height-1):
                    sd.append(gridNT[i+1][j].den)                    
                if gridN[i][j].y != 0:
                    sd.append(gridNT[i-1][j].den)

                acc = 0
                for k in range(sd.__len__()):
                    acc += sd[k]
                sn = acc/sd.__len__()
                
                gridN[i][j].den = (gridC[i][j].den + (ks * sn))/(1+ks)

                #Equation: gridN[i][j].den = (gridC[i][j].den + (k * ((gridNT[i+1][j].den + gridNT[i-1][j].den + gridNT[i][j+1].den + gridNT[i][j-1].den)/4)))/(1+k)
        
        gridC = [[copy.copy(cell_obj) for cell_obj in line] for line in gridN]
    
    grid = [[copy.copy(cell_obj) for cell_obj in line] for line in gridN]
    return grid

def advect(deltaTime):
    global grid

    gridC = [[copy.copy(cell_obj) for cell_obj in line] for line in grid]
    gridN = [[copy.copy(cell_obj) for cell_obj in line] for line in grid]

    for i in range(height):
        for j in range(width):
            nX = gridC[i][j].x - (gridC[i][j].velX*deltaTime)
            nY = gridC[i][j].y - (gridC[i][j].velY*deltaTime)

            inX = math.floor(nX)
            inY = math.floor(nY)

            fracX = nX - inX
            fracY = nY - inY

            acc = gridC[inY][inX].den
            accX = gridC[inY][inX].velX
            accY = gridC[inY][inX].velY
            if gridC[inY][inX].x != (width-1):
                acc = lerp(acc,gridC[inY][inX+1].den,fracX)
                accX = lerp(accX,gridC[inY][inX+1].velX,fracX)
                accY = lerp(accY,gridC[inY][inX+1].velY,fracY)
            if gridC[inY][inX].y != (height-1):
                acc = lerp(acc,gridC[inY+1][inX].den,fracY)
                accX = lerp(accX,gridC[inY+1][inX].velX,fracX)
                accY = lerp(accY,gridC[inY+1][inX].velY,fracY)                
            if gridC[inY][inX].x != (width-1) and gridC[inY][inX].y != (height-1):
                acc = lerp(acc,gridC[inY+1][inX+1].den,fracX)
                accX = lerp(accX,gridC[inY+1][inX+1].velX,fracX)
                accY = lerp(accY,gridC[inY+1][inX+1].velY,fracY)                
            
            gridN[i][j].den = acc
            gridN[i][j].velX = accX
            gridN[i][j].velY = accY
    print(gridN[0][5].velY)
    print(gridN[0][5].velX)
    return gridN

def display(dgrid):
    Awidth = arcade.get_window().width
    Aheight = arcade.get_window().height

    relWidth = Awidth/width
    relHeight = Aheight/height

    arcade.start_render()

    for i in range(height):
        for j in range(width):
            color = abs(((dgrid[i][j].den-25000)/(dgrid[i][j].den+98.039))+255)
            cenX = (j*relWidth) + (relWidth/2)
            cenY = Aheight - ((i*relHeight) + (relHeight/2))
            arcade.draw_rectangle_filled(cenX,cenY,relWidth,relHeight,(color,color,color))
          

FPS = []
def main(deltaTime):
    global grid
    # Avg Fps calc
    FPS.append(1/deltaTime)
    if FPS.__len__() > 60:
        FPS.pop(0)
    acc = 0
    for i in range(FPS.__len__()):
        acc += FPS[i]
    tFPS = acc/FPS.__len__()
    #print(tFPS)
    # Avg Fps calc End


    #grid = advect(deltaTime)
    grid = diffuse(deltaTime*diffuseSpeed,25)
    display(grid)

class MainGame(arcade.Window):
    def __init__(self):
            super().__init__(windowWidth, windowHeight, title="Fluid",resizable=True)
    def on_update(self,deltaTime):
        global windowWidth
        global windowHeight
        windowWidth = arcade.get_window().width
        windowHeight = arcade.get_window().height
        main(deltaTime)
    def on_mouse_press(self, x, y, button, modifiers):
        global grid
        relWidth = windowWidth/width
        relHeight = windowHeight/height
        gridY = (height-1) - math.floor(y/relHeight)
        gridX = math.floor(x/relWidth)
        grid[gridY][gridX].den += 1000
        grid[gridY][gridX].velX += 1
        


MainGame()
arcade.run()
