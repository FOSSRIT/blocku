#http://freebooks.by.ru/view/RedHatLinux6Unleashed/rhl6u348.htm
#http://stackoverflow.com/questions/3696114/when-blitting-a-sprite-with-colorkey-transparency-in-pygame-the-areas-that-shoul
"""Main Blocku game logic class

import every thing that the activity needs and run game code

Original creators: Fran Rogers and Ariel Zamparini
Developed by: Kai Ito
"""

#!/usr/bin/python
import pygame, random, os.path, os, sys

from pygame.locals import *
from pygame import *
from itertools import chain

try: import gtk
except ImportError:
    print('gtk error')
    gtk = None

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#game constants
SCREENRECT     = Rect(0, 0, 1200, 900)
KEYBOARDMOVESPEED = 10

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

"""def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs"""

def display_box(screen, message, x, y):
	"Print a message in a box in the middle of the screen"
	font = pygame.font.Font(None, 42)
	rect = pygame.Rect([x, y, 300, 30])

	#center = screen.get_rect().center
	#rect.center = center

	pygame.draw.rect(screen, (255, 255, 255), rect, 0)
	pygame.draw.rect(screen, (0,0,0), rect, 1)

	screen.blit(font.render(message, 1, (0,0,0)), rect.topleft)
	
	pygame.display.flip()

# num - number of blocks on one side of grid (ex: pass in 3 for a 3x3 grid)
def GenerateAddition(num, answer):
    rows = list([] for i in range(num))
    blocks = list([] for i in range(num * num))
    for i in range(num):
        rows[i] = list([] for i in range(num))

    # x and y positions of starting point of grid
    x = 398
    y = 298
    # answer to solve for

    # populate the list with blocks
    #blocks are Block(n,s,e,w,x,y) xy= starting position
    for i in range(num):
        for k in range(num):
            temp = Block(-1, -1, -1, -1, (x + (i * 108)+100), (y + (k * 108)+50))
            rows[i][k] = temp
            #blocks[(i * 3) + k] = temp

    # Left and right answers
    for i in range(num):
        for k in range(num):
            # set the block's right side answer
            rows[i][k].origEast = rows[i][k].east = random.randint(0, answer)
            # generate a random num for the block's west answer
            if rows[i][k].west == -1:
                rows[i][k].origWest = rows[i][k].west = random.randint(0, answer + 10)
            # check the left side answer of the block in the adjacent row
            if (i + 1) < num:
                rows[i + 1][k].origWest = rows[i + 1][k].west = (answer - rows[i][k].east)
                 #rows[i + 1][k].west
    #print(rows[3][2])

    # Top and bottom answers
    for i in range(num):
        for k in range(num):
            # set top answer if empty
            if (rows[i][k].north == -1):
                rows[i][k].origNorth = rows[i][k].north = random.randint(0, answer + 10)
                 #rows[i][k].north
            # get random number for south
            rows[i][k].origSouth = rows[i][k].south = random.randint(0, answer)
            # get answer in block below the block we just filled in
            if (k + 1) < num:
                rows[i][k].origNorth = rows[i][k + 1].north = (answer - rows[i][k].south)

    # get all the blocks into a single list
    count = 0
    #print(count)
    for i in range(num):
        for k in range(num):
            blocks[count] = rows[i][k]
            count += 1
            
    # make sure all the original positions are saved
    for block in blocks:
        block.origNorth = block.north
        block.origSouth = block.south
        block.origEast = block.east
        block.origWest = block.west
        
        
    #print(count)

    return blocks


# num - number of blocks on one side of grid (ex: pass in 3 for a 3x3 grid)
def GenerateSubtraction(num, answer):
    rows = list([] for i in range(num))
    blocks = list([] for i in range(num * num))
    for i in range(num):
        rows[i] = list([] for i in range(num))

    # x and y positions of starting point of grid
    x = 398
    y = 298
    # answer to solve for

    # populate the list with blocks
    #blocks are Block(n,s,e,w,x,y) xy= starting position
    for i in range(num):
        for k in range(num):
            temp = Block(-1, -1, -1, -1, (x + (i * 108)+100), (y + (k * 108)+50))
            rows[i][k] = temp
            #blocks[(i * 3) + k] = temp

    # Left and right answers
    for i in range(num):
        for k in range(num):
            # set the block's right side answer
            rows[i][k].origEast = rows[i][k].east = random.randint(0, answer)
            # generate a random num for the block's west answer
            if rows[i][k].west == -1:
                rows[i][k].origWest = rows[i][k].west = random.randint(0, answer + 10)
            # check the left side answer of the block in the adjacent row
            if (i + 1) < num:
                rows[i + 1][k].origWest = rows[i + 1][k].west = (answer + rows[i][k].east)
                 #rows[i + 1][k].west
    #print(rows[3][2])

    # Top and bottom answers
    for i in range(num):
        for k in range(num):
            # set top answer if empty
            if (rows[i][k].north == -1):
                rows[i][k].origNorth = rows[i][k].north = random.randint(0, answer + 10)
                 #rows[i][k].north
            # get random number for south
            rows[i][k].origSouth = rows[i][k].south = random.randint(0, answer)
            # get answer in block below the block we just filled in
            if (k + 1) < num:
                rows[i][k].origNorth = rows[i][k + 1].north = (answer + rows[i][k].south)

    # get all the blocks into a single list
    count = 0
    #print(count)
    for i in range(num):
        for k in range(num):
            blocks[count] = rows[i][k]
            count += 1
            
    # make sure all the original positions are saved
    for block in blocks:
        block.origNorth = block.north
        block.origSouth = block.south
        block.origEast = block.east
        block.origWest = block.west
        
        
    #print(count)

    return blocks

def Solve(blocks):
    for block in blocks:
        # checks original position
        if (block.rect.x != (block.origX + 0) or block.rect.y != (block.origY + 0)):
            return "Incomplete"
        # checks original rotation
        if (block.north != block.origNorth or block.south != block.origSouth or block.east != block.origEast or block.west != block.origWest):
            return "Incomplete"
        
    return "Solved!"

# puts the blocks in random positions
def Randomize(blocks):
    for block in blocks:
        block.rect.x = random.randint(200, 900)
        block.rect.y = random.randint(200, 700)

# read in a board called testFile.txt
def LoadBoard(nm):
    # File format:
    # ---------------
    # Number of blocks in board
    # X-Pos Y-Pos BlockHeight N S W E R G B
    # NSWE = directions
    # RGB = color of the block in RGB
    
    # For now, we'll ignore the block height and color
    try:
        file = open("boards\\" + nm + ".txt", "r")
        numLines = file.readline()
        #print(numLines)
        blocks = list([] for i in range(int(numLines)))
        # read in each line and split it
        for i in range(int(numLines)):
            line = file.readline()
            args = line.rsplit()
            #blocks are Block(n,e,s,w,x,y) xy= starting position
            blocks[i] = Block(args[2], args[5], args[3], args[4], int(args[0]), int(args[1]))

        file.close()
    except:
        return "Can't load board"
    
    return blocks

# Will grab the last line of the file
def LastLine(nm):
    try:
        file = open("boards\\" + nm + ".txt", 'rU')
        lines = file.readlines()
        file.close()
    except:
        lines = 'Solve for: X + Y = 61'

    return lines[len(lines)-1]

    
def GenerateGrid(blocks):
    gridPos = list([] for i in range(len(blocks)))

    for k in range(len(blocks)):
        gridPos[k] = (blocks[k].rect.x - 6, blocks[k].rect.y - 6)

    #print(gridPos)
    return gridPos

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join('data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print('Warning, unable to load,', file)
    return dummysound()

        
#block class. this is the block with the numbers on it.
#http://www.pygame.org/docs/tut/chimp/chimp.py.html
class Block(pygame.sprite.Sprite):
    permImages = []
    images = []
    north=''
    east=''
    south=''
    west=''
    origNorth = ''
    origSouth = ''
    origWest = ''
    origEast = ''
    isLast = 0
    isMoving = False
    globX=1
    globY=1
    origX = 0
    origY = 0
    rangeRender = 0
    
    def __init__(self, n='', e='', s='', w='', x='', y=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.images[0].copy()
        self.rect = self.images[0].copy()
        self.blankImage = self.image.copy()
        Block.images = self.images[1:]
        if len(Block.images) == 0:
            Block.images = Block.permImages

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = pygame.Rect(x,y,96,96)

        #self.update()
        
        #self.rect = pygame.Rect(x,y,96,96)
        self.origX = x
        self.origY = y
        self.font = pygame.font.Font(None, 30)
        self.color = Color('black')
        
        self.north = n
        self.east  = e
        self.south = s
        self.west  = w
        self.origNorth = n
        self.origEast = e
        self.origSouth = s
        self.origWest = w

        self.update()
    

    def update(self):
        #keep the block on the screen
        self.rect = self.rect.clamp(SCREENRECT)
        self.image = self.blankImage.copy()
        #self.image = self.images[0].copy()
        self.image.blit(self.font.render(str(self.north), 0, self.color),(39,3))
        self.image.blit(self.font.render(str(self.east), 0, self.color),(self.rangeRender,42))
        self.image.blit(self.font.render(str(self.south), 0, self.color),(39,75))
        self.image.blit(self.font.render(str(self.west), 0, self.color),(5,42))
        

    def setGrabbed(self, sett):
        self.isMoving = sett
    def isGrabbed(self):
        return self.isMoving
    def grab(self, pos):
        x, y = pos;
        globX=x
        globY=y
        #remember the offset here is 48 as this will center the mouse in our 96 pixel image
        newPos = self.rect.move((x,y))
        self.rect.left = x-48
        self.rect.top = y-48
    def getX(self):
        return globX
    def getY(self):
        return globY
    def rotate(self):
        temp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = temp

#the main game class
class Game:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.paused = False

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self, curMode, rng, dif, sub, name):
        pygame.mouse.set_visible(False)
        isRan = 0
        editMode = False

        #print curMode
        #self.rangee = rng
        #print dif

        #pseudo timer
        loopCounter = 0

        #puzzle counter
        numRotateTotal = 0
        
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        # load a test sound
        #pygame.mixer.music.load("sounds\\trololo.ogg")
        
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        
        squares = load_image('square.png')
        global background
        background = load_image('background.png')
        background = background.convert()
        iconImg = load_image('blocku.png')
        self.screen = pygame.display.set_mode((1200,900))
        #spriteBatch = pygame.sprite.RenderUpdates()

        #generate random number between 20 and 99 for the answer to equal
        if rng == 1:
            answer = random.randint(15, 40)
            Block.rangeRender = 65
        elif rng == 2:
            answer = random.randint(30, 99)
            Block.rangeRender = 65
        elif rng == 3:
            answer = random.randint(100, 999)
            Block.rangeRender = 57

        if pygame.font:
            if curMode == 3:
                objective = Text(LastLine(name),253,174)
            elif not curMode == 3 and sub == 0:
                objective = Text('Arrange blocks so that addition equals ' + str(answer),253,174) #Objective text
            elif not curMode == 3 and sub == 1:
                objective = Text('Arrange blocks so that subtraction equals ' + str(answer),253,174) #Objective text
            solved = Text('',400,240,'red',142)  #Text for when solved
            timeText = Text('',375,25,'black',89) #text to display time elapsed
            
            font = pygame.font.Font(None, 42)
            check = font.render("Check Answer", 1, (0,230,0))
            background.blit(check,[978,840])
            pygame.display.flip()
            
        
        
        # load images here
        # for gifs  img = load_image('filename.gif')
        # for bmps img = pygame.image.load('filename.bmp') but our function handles that for us
        # a note for graphics blit means copy pixels from screen.blit()
        #Check solution text
        #cursor = mouseUpdate()            
        #spriteBatch.add(cursor)
            

        
        # the test will need rects and positions i sugest make some kind of default
        # this information can be held by each block as they are created but is made here


        # load images to pipe to the sprite classes
        
        #Block.images = allBlockImages
        
        tempImages = [load_image('c1.png'),load_image('c2.png'),load_image('c3.png'),load_image('c4.png'),load_image('c5.png'),load_image('c6.png'),load_image('c7.png'),load_image('c8.png'),load_image('c9.png')]
        Block.images = tempImages
        Block.permImages = tempImages
        
        gridImg1 = squares
            
        #blocks are Block(n,s,e,w,x,y) xy= starting position
        #
        #
        #
        #RIGHT HERE FOR RANDOM OR READ IN
        #
        #
        #
        #
        # Uncomment lines with an asterisk to make the game generate a random board again
        # Lines with a double pound are used to load a board
        if not curMode == 3: 
            if sub == 0:
                if dif == 1:
                    allBlocks = GenerateAddition(3, answer)
                elif dif == 2:
                    allBlocks = GenerateAddition(4, answer)
                elif dif == 3:
                    allBlocks = GenerateAddition(3, answer)
                    for block in allBlocks:
                        for i in range(0, random.randint(1, 6)):
                            block.rotate()
                elif dif == 4:
                    allBlocks = GenerateAddition(4, answer)
                    for block in allBlocks:
                        for i in range(0, random.randint(1, 6)):
                            block.rotate()
            else:
                if dif == 1:
                    allBlocks = GenerateSubtraction(3, answer)
                elif dif == 2:
                    allBlocks = GenerateSubtraction(4, answer)
                elif dif == 3:
                    allBlocks = GenerateSubtraction(3, answer)
                    for block in allBlocks:
                        for i in range(0, random.randint(1, 6)):
                            block.rotate()
                elif dif == 4:
                    allBlocks = GenerateSubtraction(4, answer)
                    for block in allBlocks:
                        for i in range(0, random.randint(1, 6)):
                            block.rotate()
        else:
            allBlocks = LoadBoard(name)
            if name == 'boardMaker':
                editMode = True
            
        gridpos = GenerateGrid(allBlocks)
        if curMode == 1:
            Randomize(allBlocks)
        elif curMode == 2:
            for block in allBlocks:
                for i in range(0, random.randint(1, 6)):
                    block.rotate()
                    numRotateTotal += 1
            print numRotateTotal
        cursor = mouseUpdate(mouse.get_pos())
        #pygame.display.update(cursor)

        #actually displays everything
        allsprites = pygame.sprite.RenderPlain((cursor, allBlocks, objective, solved, timeText))
        
        #allBlocks = LoadBoard() ##
        
        #answerStr = LastLine()  ##
        #answerStr = 'Arrange blocks so that addition equals ' + str(answer) #*
        #print(answerStr)
        
        #print(allBlocks)

        # Default grid positions - handled now by GenerateGrid()
        #gridpos = [(200,200),(272,200),(344,200),(200,272),(272,272),(344,272),(200,344),(272,344),(344,344)]
        #print(gridpos[0][0])
        
        for i in range(len(gridpos)):
            background.blit(gridImg1, gridpos[i])

        #for i in range(len(allBlocks)):
        #    allBlocks[i].update()
        #    background.blit(allBlocks[i].image,[allBlocks[i].rect.x,allBlocks[i].rect.y])
        
        #get the image and screen in the same format
        """if background.get_bitsize() == 8:
            set_palette(background.get_palette())
        else:
            background.convert()"""

        screen.blit(background,(0,0))
        pygame.display.flip()

        #to set the icon up and to decorate the game window
        icon = pygame.transform.scale(iconImg, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Blocku')

        
        
        #if a key is down
        #global keyDown
            
            #spriteBatch.add(mainText())
        
        #cursor.move_to_front()
        

        # it is important to note that like xna the origin is 0,0
        # the top left of the current window
        # print is trace in console
        # and increases as you go down and to the right
        # pygame has a collision detector under pygame.sprite.spritecollide(group,group,dokill)
        # this will return a list of colliders, dokill will remove the colliders from the parrent group if true
        mousePossible = True
        completed = False
        timer = 0
        counter = 0
        keyDown = False
        mins = 0
        numRotate = 0
        while 1:
            loopCounter += 1
            if curMode == 1:
                if not completed:
                    counter += 1
                    if counter > 30:
                        timer += 1
                        counter = 0
                    if timer > 59:
                        mins += 1
                        timer = 0
                timeText.change('Time Elapsed ' + str(mins) + ':' + str(timer))
            elif curMode == 2:
                timeText.change('Number of Rotations: ' + str(numRotate))
            
            if loopCounter > 50:
                loopCounter = 0
                if not completed:
                    solved.change('')
                
            #pygame.display.update(allBlocks)
            #pygame.display.flip()
            # Pump GTK messages.
            while gtk and gtk.events_pending():
                gtk.main_iteration()

            keystate = pygame.key.get_pressed()
            # Pump PyGame messages.
            for e in event.get():
                if e.type == QUIT or \
                    (e.type == KEYDOWN and e.key == K_ESCAPE):
                        return
                elif e.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(e.size, pygame.RESIZABLE)
                if e.type == MOUSEBUTTONDOWN:
                    event.set_grab(1)
                    mousePossible = True
                    if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                            result = Solve(allBlocks)
                            if result == 'Solved!':
                                solved.change('You Win!')
                                completed = True
                            else:
                                loopCounter = 0
                                solved.change('Incomplete')
                                
                elif e.type == MOUSEBUTTONUP:
                    event.set_grab(0)
                if e.type == KEYDOWN:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        event.set_grab(1)
                elif e.type == KEYUP:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        event.set_grab(0)
                        if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                            result = Solve(allBlocks)
                            if result == 'Solved!':
                                solved.change('You Win!')
                                completed = True
                            else:
                                loopCounter = 0
                                solved.change('Incomplete')
            
            #if keystate[K_b]:
               # pygame.mixer.music.play()
            # for key test use keystate[key] and a return of true will occur when key down
            

            #for block in blocks:
            x = cursor.rect.x
            y = cursor.rect.y

            
            #keyboard and gameboy buttons
            if keystate[K_LEFT] or keystate[K_KP4]:
                cursor.move(3)
                mousePossible = False
            if keystate[K_RIGHT] or keystate[K_KP6]:
                cursor.move(1)
                mousePossible = False
            if keystate[K_UP] or keystate[K_KP8]:
                cursor.move(0)
                mousePossible = False
            if keystate[K_DOWN] or keystate[K_KP2]:
                cursor.move(2)
                mousePossible = False
                
            #cursor.grab(mouse.get_pos())
            if mousePossible == True:
                cursor.mouseMoved(mouse.get_pos())
            
            if not keystate[K_RETURN] or keystate[K_KP1]:
                keyDown = False

            if not editMode:
                for block in allBlocks:
                    #Block rotation when pressing enter
                    if (curMode == 1 and not (dif == 1 or dif == 2)) or curMode == 2 or (curMode == 3 and not dif == 1):
                        if block.isLast == 1 and (keystate[K_RETURN] or keystate[K_KP1]) and not keyDown:
                            block.rotate()
                            numRotate += 1
                            keyDown = True
                    isLast = block

                    #For block dragging
                    if event.get_grab():
                        #debugText += ' holding mouse button 1'
                        # and block.isGrabbed() == False
                        if block.rect.collidepoint([cursor.rect.x,cursor.rect.y]):
                            anotherBlock = 0
                            for blockB in allBlocks:
                                if blockB.isMoving == True and blockB != block:
                                    anotherBlock = 1
                                    break
                            if anotherBlock == 0:
                                if curMode == 1 or curMode == 3:
                                    block.grab([cursor.rect.x, cursor.rect.y])
                                block.setGrabbed(True)
                                for tempblock in allBlocks:
                                    tempblock.isLast = 0
                                block.isLast = 1
                                isRan = 1
                                break
                        elif block.isMoving == True and (curMode == 1 or curMode == 3):
                            block.grab([cursor.rect.x, cursor.rect.y])
                    elif isRan == 1 and block.isLast == 1:
                        for piece in gridpos:
                            if cursor.rect.x > piece[0] and cursor.rect.x < piece[0]+108 and cursor.rect.y > piece[1] and cursor.rect.y < piece[1]+108 and block.isMoving == True and (curMode == 1 or curMode == 3):
                                place = piece[0] + 54, piece[1] + 54
                                isLast.grab(place)
                                isRan = 0
                        block.setGrabbed(False)
            else:
                pass
                #code will go here for clickign on grid piece to add a block

            # note random here is random.random()
            # note foreach here is for object in
            
            allsprites.update()
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)
            
class Text(pygame.sprite.Sprite):
    text = ''
    def __init__(self,txt='',x=0,y=0,clr='black',size=42):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, size)
        self.color = Color(clr)
        self.update()
        self.rect = self.image.get_rect().move(x, y)
        self.text = txt

    def update(self):
        msg = self.text
        self.image = self.font.render(msg, 0, self.color)

    def change(self, new=''):
        self.text = new
        self.update()

class mouseUpdate(pygame.sprite.Sprite):
    def __init__(self, pos):
        x,y = pos
        pygame.sprite.Sprite.__init__(self)
        thisImg = load_image('mouse.png')
        #over = pygame.sprite.LayeredUpdates(*[self])

        #over.move_to_front(self)
        self.image = thisImg
        #self.update()
        #self.rect = self.image.get_rect().move(50, 220)
        self.rect = pygame.Rect(x,y,28,32)

    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        over = pygame.sprite.LayeredUpdates(*[self])
        over.move_to_front(self)

    def mouseMoved(self,mouse):
        self.rect.x, self.rect.y = mouse
        

    def move(self, direction):
        # up = 0, right = 1, down = 2, left = 3
        if direction == 0:
            self.rect.y += -KEYBOARDMOVESPEED
        if direction == 1:
            self.rect.x += KEYBOARDMOVESPEED
        if direction == 2:
            self.rect.y += KEYBOARDMOVESPEED
        if direction == 3:
            self.rect.x += -KEYBOARDMOVESPEED

class MainMenu():
    
    instBool = False
    modeBool = False
    curSel = 1
    selRange = 1
    selDiff = 1
    selSubtraction = 0  
    text = ""
    goodLoad = False
    def __init__(self):
        self.paused = False
        self.clock = pygame.time.Clock()

        #set the screen up
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)


        pygame.display.set_caption('Blocku')
        self.menuImg = load_image('bg.png').convert()
        #self.background = load_image('background.png')
        self.instImg = load_image('instructions.png').convert()
        self.menuWI = load_image('menuWithInst.png').convert()
        self.subAdd = load_image('subAdd.png').convert()
        self.gModes = load_image('modesMain.png').convert()
        self.hi = load_image('hilite.png').convert()
        self.leftArrow = load_image('left.png').convert()
        self.rightArrow = load_image('right.png').convert()
        self.button = load_image('button.png').convert()

        if pygame.font:
            self.selRng = Text('',575,350,'black',42)
            self.selDifficulty = Text('',575,550,'black',42)
            self.selSub = Text('',575,105,'black',42)

        self.screen = pygame.display.set_mode((1200,900))
        #self.screen.blit(self.menuImg,(0,0))
        #get the image and screen in the same format

        screen.blit(self.menuImg, (0,0))

        text = pygame.font.Font(None, 42)
        self.welp = self.wrapline('Goal: position the blocks so that the numbers which are next to each other solve the given equation.      Controls: Use the mouse or Game Buttons to drag and drop the blocks. Use the return key to rotate, or the checkmark button.',text,500)
        
        self.addText()
        pygame.display.flip()
        self.loop()

    def truncline(self, text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
    def wrapline(self, text, font, maxwidth): 
        done=0                      
        wrapped=[]                  
                                   
        while not done:             
            nl, done, stext = self.truncline(text, font, maxwidth) 
            wrapped.append(stext.strip())                  
            text=text[nl:]                                 
        return wrapped
     
     
    def wrap_multi_line(self, text, font, maxwidth):
        """ returns text taking new lines into account.
        """
        lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
        return list(lines)

    def addText(self):
        
        if pygame.font:
            font = pygame.font.Font(None, 50)

            #Exit
            exitt = font.render("Exit", 1, (255,255,255))
            self.screen.blit(exitt,[570,810])

            if self.modeBool == False:
                #Game Modes
                gMode = font.render("Game Modes", 1, (255,255,255))
                self.screen.blit(gMode,[520,660])
            else:
                #apply and close for gModes
                closeG = pygame.font.Font(None, 38)
                close = closeG.render("Apply",1,(0,0,0))
                self.screen.blit(close,[995,692])

                #Time attack       126,198
                tAttack = pygame.font.Font(None, 55)
                time = tAttack.render("Time Attack",1,(0,0,0))
                self.screen.blit(time,[149,250])

                #Puzzle            126,377
                puzzle = pygame.font.Font(None, 55)
                puz = puzzle.render("Puzzle",1,(0,0,0))
                self.screen.blit(puz,[149,430])

                #Story Mode              126,572
                stryMode = pygame.font.Font(None, 55)
                stry = stryMode.render("Story Mode",1,(0,0,0))
                self.screen.blit(stry,[149,625])

            #instructions panel
            if self.instBool == True:
                newFont = pygame.font.Font(None, 100)
                instTitle = newFont.render("Instructions", 1, (255,0,0))
                self.screen.blit(instTitle,[390,310])
                
                for i in range(len(self.welp)):
                    newTxt=pygame.font.Font(None,42)
                    newInst = newTxt.render(self.welp[i],1,(0,0,0))
                    self.screen.blit(newInst,[370,370+(28*i)])

                closeF = pygame.font.Font(None, 28)
                close = closeF.render("Close",1,(255,0,0))
                self.screen.blit(close,[800,577])
                
            elif self.modeBool == False:
                #New Game
                new = font.render("New Game", 1, (255, 255, 255))
                self.screen.blit(new, [530,375])

                #Instructions
                instructs = font.render("Instructions", 1, (255,255,255))
                self.screen.blit(instructs,[520,520])

    def rangeChange(self, change):
        if change == 1:
            if not self.selRange == 1:
                self.selRange -= 1
            else:
                self.selRange = 3
        elif change == 2:
            if not self.selRange == 3:
                self.selRange += 1
            else:
                self.selRange = 1

    def diffChange(self, change):
        if self.curSel == 1:
            if change == 1:
                if not self.selDiff == 1:
                    self.selDiff -= 1
                else:
                    self.selDiff = 4
            elif change == 2:
                if not self.selDiff == 4:
                    self.selDiff += 1
                else:
                    self.selDiff = 1
        else:
            if self.selDiff == 1:
                self.selDiff = 2
            else:
                self.selDiff = 1

    def subChange(self):
        if self.selSubtraction == 0:
            self.selSubtraction = 1
        else:
            self.selSubtraction = 0

    def loop(self):
        pygame.mouse.set_visible(False)
        cursor = mouseUpdate(mouse.get_pos())
        allsprites = pygame.sprite.RenderPlain((cursor, self.selRng, self.selDifficulty, self.selSub))
        
        mousePossible = True
        
        while 1:
            hit = False
            keystate = pygame.key.get_pressed()
            #keyboard and gameboy buttons
            if keystate[K_LEFT] or keystate[K_KP4]:
                cursor.move(3)
                mousePossible = False
            if keystate[K_RIGHT] or keystate[K_KP6]:
                cursor.move(1)
                mousePossible= False
            if keystate[K_UP] or keystate[K_KP8]:
                cursor.move(0)
                mousePossible = False
            if keystate[K_DOWN] or keystate[K_KP2]:
                cursor.move(2)
                mousePossible = False
            if keystate[K_SPACE] or keystate[K_KP3]:
                hit = True
                
            #cursor.grab(mouse.get_pos())
            if mousePossible == True:
                cursor.mouseMoved(mouse.get_pos())

                
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousePossible = True
                        hit = True

                if hit:
                    #new game button is at (382,269) and is 311,122 pixels
                    #insturctions button is at (382, 392) and is 311,122 pixels
                    #game mode is at (382, 510) and is 311,122 pixels
                    #exit is at (382,625) and is 311,122 pixels
                    
                    #new game. launches into a new game of blocku
                    if cursor.rect.x > 466 and cursor.rect.x < 777 and cursor.rect.y > 329 and cursor.rect.y < 451 and self.instBool == False and self.modeBool == False:
                        pygame.display.flip()
                        game = Game()
                        game.run(self.curSel, self.selRange, self.selDiff, self.selSubtraction, self.text)
                        pygame.quit()
                            
                    #insturctions
                    if cursor.rect.x > 466 and cursor.rect.x < 777 and cursor.rect.y > 478 and cursor.rect.y < 600 and self.instBool == False and self.modeBool == False:
                        #pygame.display.flip()
                        self.instBool = True
                        self.menuImg.blit(self.instImg, (328,294))
                        self.addText()
                        pygame.display.flip()
                        
                    #close insturctions button
                    if cursor.rect.x > 798 and cursor.rect.x < 865 and cursor.rect.y > 573 and cursor.rect.y < 599 and self.instBool == True:
                        self.menuImg = load_image('bg.png')
                        self.screen.blit(self.menuImg, (0,0))
                        self.instBool = False
                        self.addText()
                        pygame.display.flip()

                    #Game modes
                    if cursor.rect.x > 466 and cursor.rect.x < 777 and cursor.rect.y > 623 and cursor.rect.y < 745 and self.instBool == False and self.modeBool == False:
                        self.menuImg.blit(self.gModes, (101,167))
                        self.modeBool = True
                        self.goodLoad = False
                        self.addText()
                        pygame.display.flip()

                    if self.modeBool == True and not self.goodLoad:
                        #which is selected?
                        if self.curSel == 1:
                            self.menuImg.blit(self.hi,(126,198))
                        elif self.curSel == 2:
                            self.menuImg.blit(self.hi,(126,377))
                        elif self.curSel == 3:
                            self.menuImg.blit(self.hi,(126,572))                        

                        #click on time attack
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 176 and cursor.rect.y < 354:
                            self.curSel = 1
                            self.menuImg.blit(self.gModes, (101,167))
                            #which is selected?
                            self.menuImg.blit(self.hi,(126,198))

                        #click on puzzle
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 366 and cursor.rect.y < 540:
                            self.curSel = 2
                            self.menuImg.blit(self.gModes, (101,167))
                            self.selDiff = 1
                            #which is selected?
                            self.menuImg.blit(self.hi,(126,377))

                        #click on story
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 550 and cursor.rect.y < 730:
                            self.curSel = 3
                            self.selDiff = 1
                            self.menuImg = load_image('bg.png')
                            self.menuImg.blit(self.gModes, (101,167))
                            #which is selected?
                            self.menuImg.blit(self.hi,(126,572))

                        #if time attack or puzzle mode is selected
                        if self.curSel == 1 or self.curSel == 2:
                            
                            numRange = pygame.font.Font(None,42).render("Select Number Range",1,(0,0,0))
                            self.menuImg.blit(numRange,(526,298))

                            difficulty = pygame.font.Font(None,42).render("Select Difficulty",1,(0,0,0))
                            self.menuImg.blit(difficulty,(526,498))

                            self.menuImg.blit(self.subAdd, (511,72))
                            self.menuImg.blit(self.leftArrow, (529,100))
                            self.menuImg.blit(self.rightArrow, (909,100))
                            self.menuImg.blit(self.leftArrow,(529,341))
                            self.menuImg.blit(self.rightArrow,(909,341))
                            self.menuImg.blit(self.leftArrow,(529,543))
                            self.menuImg.blit(self.rightArrow,(909,543))

                            #range left arrow
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 341 and cursor.rect.y < 383:
                                self.rangeChange(1)

                            #range right arrow
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 341 and cursor.rect.y < 383:
                                self.rangeChange(2)

                            #difficulty left arrow
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(1)

                            #difficulty right arrow
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(2)

                            #select addition or subtraction right
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 100 and cursor.rect.y < 142:
                                self.subChange()

                            #select addition or subtraction left
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 100 and cursor.rect.y < 142:
                                self.subChange()

                            #all are 25 by 42
                            #range left       529 341
                            #range right      909 341
                            #diff left        529 543
                            #diff right       909 543

                            #sub left         529 100
                            #sub right        909 100

                        #click on story mode
                        if self.curSel == 3:

                            self.menuImg.blit(self.leftArrow,(529,543))
                            self.menuImg.blit(self.rightArrow,(909,543))
                            self.menuImg.blit(self.button,(546,215))
                            
                            difficulty = pygame.font.Font(None,42).render("Select Difficulty",1,(0,0,0))
                            self.menuImg.blit(difficulty,(526,498))

                            boardEnter = pygame.font.Font(None,42).render("Enter the name of board",1,(0,0,0))
                            self.menuImg.blit(boardEnter,(526,350))

                            createText = pygame.font.Font(None,42).render("Create a board",1,(0,0,0))
                            self.menuImg.blit(createText,(570,225))
                            
                            #difficulty left arrow
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(1)

                            #difficulty right arrow
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(2)

                            #create a board button
                            if cursor.rect.x > 546 and cursor.rect.x < 806 and cursor.rect.y > 215 and cursor.rect.y < 265:
                                game = Game()
                                game.run(self.curSel, self.selRange, self.selDiff, self.selSubtraction, 'boardMaker')
                                pygame.quit()


                        #close gModes KEEP THIS LAST
                        if cursor.rect.x > 980 and cursor.rect.x < 1094 and cursor.rect.y > 684 and cursor.rect.y < 728:
                            if self.curSel == 3:
                                try:
                                   outfile = open("boards\\" + self.text + ".txt", "r")
                                   self.goodLoad = True
                                except IOError:
                                    self.goodLoad = False
                                    self.text = "File does not exist"
                                    continue
                            self.menuImg = load_image('bg.png')
                            self.screen.blit(self.menuImg, (0,0))
                            self.modeBool = False
                            self.addText()
                            pygame.display.flip()
                            
                    #exit button. exits the game
                    if cursor.rect.x > 466 and cursor.rect.x < 777 and cursor.rect.y > 765 and cursor.rect.y < 887 and self.instBool == False and self.modeBool == False:
                        pygame.quit()

                #textbox
                if self.curSel == 3 and self.modeBool == True:
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        self.text = self.text[0:-1]
                    elif event.type == KEYDOWN and event.key == K_RETURN:
                        print self.text
                    elif event.type == KEYDOWN:
                        self.text += event.unicode.encode("ascii")
                    display_box(self.menuImg,'' + self.text, 529,380)

                #display defaults
                if self.selSubtraction == 0 and self.modeBool == True and (self.curSel == 1 or self.curSel == 2):
                    self.selSub.change('Addition')
                else:
                    self.selSub.change('Subtraction')
                
                if self.modeBool == True and (self.curSel == 1 or self.curSel == 2):        
                    if self.selRange == 1:
                        self.selRng.change('Low')
                    elif self.selRange == 2:
                        self.selRng.change('Medium')
                    elif self.selRange == 3:
                        self.selRng.change('High')

                    if self.selDiff == 1:
                        self.selDifficulty.change('Easy')
                    elif self.selDiff == 2:
                        self.selDifficulty.change('Medium')
                    elif self.selDiff == 3:
                        self.selDifficulty.change('Hard')
                    elif self.selDiff == 4:
                        self.selDifficulty.change('Very Hard')
                        
                elif self.modeBool == True and self.curSel == 3:
                    self.selRng.change('')
                    self.selSub.change('')
                    if self.selDiff == 1:
                        self.selDifficulty.change('Easy')
                    elif self.selDiff == 2:
                        self.selDifficulty.change('Medium')
                else:
                    self.selRng.change('')
                    self.selDifficulty.change('')
                    self.selSub.change('')
                            
            
            #cursor.mouseMoved(mouse.get_pos())
            self.screen.blit(self.menuImg, (0,0))
            
            self.addText()
            allsprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    mMenu = MainMenu()
    pygame.quit()

#call the "main" function if python is running this script
if __name__ == '__main__':
    main()
