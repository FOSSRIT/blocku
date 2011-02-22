"""Main Blocku game logic class

import every thing that the activity needs and run game code

Original creators: Fran Rogers and Ariel Zamparini
Developed by: Kai Ito
"""

#!/usr/bin/python
import pygame, random, os.path, os, sys, re

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

def load_image(file, alpha=False):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    if alpha:
        return surface.convert_alpha()
    else:
        return surface.convert()

def display_box(screen, message, x, y, w, h, size):
	"Print a message in a box in the middle of the screen"
	font = pygame.font.Font(None, size)
	rect = pygame.Rect([x, y, w, h])

	#center = screen.get_rect().center
	#rect.center = center

	pygame.draw.rect(screen, (255, 255, 255), rect, 0)
	pygame.draw.rect(screen, (0,0,0), rect, 1)

	screen.blit(font.render(message, 1, (0,0,0)), rect.topleft)
	
	pygame.display.flip()

def ask(screen, question, x, y, w, h, size, numOnly, limit, allow=True):
    pygame.font.init()  
    text = ""
    display_box(screen, question + ": " + text,x,y,w,h,size)

    while 1:
        pygame.time.wait(50)
        event = pygame.event.poll()

        if not numOnly:
            if event.type == QUIT:
                sys.exit()
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                text = text[0:-1]
            elif event.key == K_RETURN:
                break
            elif event.key == K_SPACE and not allow:
                continue
            elif len(text) < limit:
                text += event.unicode.encode("ascii")
        else:
            if event.type == QUIT:
                sys.exit()
            if event.type != KEYDOWN:
                continue
            if event.key == K_BACKSPACE:
                text = text[0:-1]
            elif event.key == K_RETURN:
                break
            elif len(text) < 6 and (event.key == K_0 or event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4 or event.key == K_5 or event.key == K_6 or event.key == K_7 or event.key == K_8 or event.key == K_9):
                text += event.unicode.encode("ascii")
                
        display_box(screen, question + ": " + text,x,y,w,h,size)
    if text == '':
        text = '0'
    return text

    
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
def LoadBoard(nm, directory='boards'):
    # File format:
    # ---------------
    # Number of blocks in board
    # X-Pos Y-Pos N S W E
    # NSWE = directions
    try:
        file = open(directory + os.sep + nm + ".txt", "r")
        numLines = file.readline()
        #print(numLines)
        blocks = list([] for i in range(int(numLines)))
        # read in each line and split it
        for i in range(int(numLines)):
            line = file.readline()
            args = line.rsplit()
	    #save file is (x,y,n,e,s,w)
            #blocks are Block(n,e,s,w,x,y) xy= starting position
            blocks[i] = Block(args[2], args[3], args[4], args[5], int(args[0]), int(args[1]))

        file.close()
    except:
        return "Can't load board"
    
    return blocks


# Will grab the last line of the file
def LastLine(nm, directory='boards'):
    try:
        file = open(directory + os.sep + nm + ".txt", 'r')
        lines = file.readlines()
        file.close()
    except:
        lines = 'Solve for: X + Y = 42'
    val = lines[len(lines)-1]
    val = ''.join([c for c in val if c in '!@#$%^& 	*()_+=-`~[]{}\|;\':\",<>/?\\/*1234567890.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'])
    return val

    
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

#Dictionary load in for different language strings
def loadDictionary(language):
    lang = {}
    tempLines = []
    tempKey = ''
    tempVal = ''
    f = open('data' + os.sep + language, 'r')
    tempLines = f.readlines()
    f.close()
    for line in tempLines:
        tempKey = line.rsplit('<>')[0]
        tempVal = line.rsplit('<>')[1][1:-2]
        #tempVal = ''.join([c for c in tempVal if c in '\"'])
        lang[tempKey] = tempVal
    return lang

        
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
    text = ''
    
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
        self.image.blit(self.font.render(str(self.north), 0, self.color),(39,3))
        if self.east < 10:
            self.rangeRender = 65
        else:
            self.rangeRender = 57
        self.image.blit(self.font.render(str(self.east), 0, self.color),(self.rangeRender,42))
        self.image.blit(self.font.render(str(self.south), 0, self.color),(39,75))
        self.image.blit(self.font.render(str(self.west), 0, self.color),(5,42))

    def edit(self, n, e, s, w):
        #print (str(self.rect.x) + ", " + str(self.rect.y))
        self.north = n
        self.east = e
        self.south = s
        self.west = w

        self.update()

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

class Highlight(pygame.sprite.Sprite):
    def __init__(self,x=1300,y=1000):
        pygame.sprite.Sprite.__init__(self)
        img = load_image('hilite.png',True)
        self.image = img
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = pygame.Rect(x,y,120,120)

    def setpos(self, pos):
        x, y = pos;
        globX=x
        globY=y
        #remember the offset here is 48 as this will center the mouse in our 120 pixel image
        newPos = self.rect.move((x,y))
        self.rect.left = x-12
        self.rect.top = y-12

#the main game class
class Game:
    strings = {}
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.paused = False
        self.strings = loadDictionary('bl_english.txt')

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self, curMode, rng, dif, sub, name, cas):
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
        """upSound = load_sound('up.ogg')
        downSound = load_sound('down.ogg')"""
        
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
            
        #Board generation depending on mode selected
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
            if name == 'boardMaker':
                editMode = True
                allBlocks = LoadBoard(name, 'data')
            else:
                allBlocks = LoadBoard(name)
            
            
        gridpos = GenerateGrid(allBlocks)
        if not editMode:
            if curMode == 1 or curMode == 3:
                Randomize(allBlocks)
                if curMode == 3 and dif == 2:
                    for block in allBlocks:
                        for i in range(0, random.randint(1, 6)):
                            block.rotate()
            elif curMode == 2:
                for block in allBlocks:
                    for i in range(0, random.randint(1, 6)):
                        block.rotate()
                        numRotateTotal += 1
        cursor = mouseUpdate(mouse.get_pos())

        #in game text
        if pygame.font:
            objective = Text('',253,174,'black',46)
            if sub == 0:
                if curMode == 3:
                    if name == 'boardMaker':
                        objective.change(LastLine(name,'data'))
                    else:
                        objective.change(LastLine(name))
                elif curMode == 1 and dif < 3:
                     objective.change(self.strings['arrangeAddition'] + str(answer))
                elif curMode == 1 and dif > 2:
                    objective.change(self.strings['arrangeAdditionRotate'] + str(answer))
                elif curMode == 2:
                    objective.change(self.strings['rotateAddition'] + str(answer))
            else:
                if curMode == 3:
                    if name == 'boardMaker':
                        objective.change(LastLine(name,'data'))
                    else:
                        objective.change(LastLine(name))
                elif curMode == 1 and dif < 3:
                     objective.change(self.strings['arrangeSubtraction'] + str(answer))
                elif curMode == 1 and dif > 2:
                    objective.change(self.strings['arrangeSubtractionRotate'] + str(answer))
                elif curMode == 2:
                    objective.change(self.strings['rotateSubtraction'] + str(answer))
            solved = Text('',400,240,'red',142)  #Text for when solved
            timeText = Text('',375,25,'black',89) #text to display time elapsed
            puzGoal = Text('',20,242,'black',42) #Text for puzzle mode goal

            font = pygame.font.Font(None, 42)
            toMenu = font.render(self.strings['mainMenu'], 1, (0,0,0))
            if curMode == 2:
                goal = font.render(self.strings['tryToBeat'], 1, (0,0,0))
            elif curMode == 1 or curMode == 3:
                goal = font.render(self.strings['recentTime'], 1, (0,0,0))
                
            if not editMode:
                background.blit(goal,[20,200])
                check = font.render(self.strings['checkAnswer'], 1, (0,0,0))
            else:
                check = font.render(self.strings['saveBoard'], 1, (0,0,0))
            background.blit(toMenu,[30,840])
            background.blit(check,[978,840])
            pygame.display.flip()

        highScores = []

        #high scores
        if not editMode:
            if not curMode == 2:
                if curMode == 1:
                    ff = open("scores" + os.sep + "timeRecent.txt", 'r')
                else:
                    ff = open("scores" + os.sep + name + "Scores.txt", 'r')
                for i in range(5):
                    highScores.append(ff.readline())
                for i in range(len(highScores)):
                    highScores[i] = highScores[i].rstrip('\n')
		    if curMode == 1:
			highScores[i] = highScores[i][:-1]
                    rec = font.render(highScores[i],1,(0,0,0))
                    background.blit(rec,[25,240+(40*i)])
                ff.close()

            elif curMode == 2:
                puzGoal.change(str(numRotateTotal) + self.strings['rotations'])

        #highlight for visual cue
        hi = Highlight()

        #actually displays everything
        allsprites = pygame.sprite.LayeredUpdates()
        for block in allBlocks:
            allsprites.add(block)
        allsprites.add(hi)
        allsprites.add((timeText, objective, puzGoal))
        allsprites.add(solved)
        allsprites.add(cursor)
        
        #Blit a grid piece to each block before they get scrambled
        for i in range(len(gridpos)):
            background.blit(gridImg1, gridpos[i])

        screen.blit(background,(0,0))
        pygame.display.flip()

        #to set the icon up and to decorate the game window
        icon = pygame.transform.scale(iconImg, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Blocku')
        

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
        nname = 'null'

        #if goign against time, set up time limits
        if cas == 0:
            if dif == 1:
                mins = 5
                timer = 59
            elif dif == 2:
                mins = 11
                timer = 59
            elif dif == 3:
                mins = 17
                timer = 59
            elif dif == 4:
                mins = 23
                timer = 59
            origMin = mins
            origSec = timer

        #for block editing
        n = 0
        east = 0
        s = 0
        w = 0

        failed = False
	
	#for block saving
        numBlocks = 0
        blocksToWrite = []
        blocksToWrite.append(["0"])

        while 1:
	    #Ran out of time
            if mins == 0 and timer == 0 and cas == 0:
                completed = True
                failed = True        
            loopCounter += 1
            #timer code

            #for the sake of a leading zero
            emptyMin = ''
            emptySec = ''
            curTime = ''
            if mins < 10:
                emptyMin = '0'
            if timer < 10:
                emptySec = '0'

            if not editMode:
                if not curMode == 2 and cas == 1:
                    if not completed:
                        counter += 1
                        if counter > 30:
                            timer += 1
                            counter = 0
                        if timer > 59:
                            mins += 1
                            timer = 0
                    curTime = emptyMin + str(mins) + ':' + emptySec + str(timer)
                    timeText.change(self.strings['timeElapsed'] + curTime)
                elif not curMode == 2 and cas == 0:
                    #dif 1 2 3 4
                    if not completed:
                        counter += 1
                        if counter > 30:
                            timer -= 1
                            counter = 0
                        if timer < 0:
                            mins -= 1
                            timer = 59
                    curTime = emptyMin + str(mins) + ':' + emptySec + str(timer)
                    if not completed:
                        timeText.change(self.strings['timeRemaining'] + curTime)
                elif curMode == 2:
                    timeText.change(self.strings['numOfRotations'] + str(numRotate))

            #clear the incomplete text after a moment
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
            #x is 240
            
            for e in event.get():
                #hit escape to quit
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    pygame.quit()
                elif e.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(e.size, pygame.RESIZABLE)

                #on click of the check answer button
                if e.type == MOUSEBUTTONDOWN:
                    event.set_grab(1)
                    mousePossible = True
                    if not editMode:
                        if not completed:
                            #check answer button
                            if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                                    result = Solve(allBlocks)
                                    if result == 'Solved!':
                                        solved.change(self.strings['win'])
                                        completed = True
                                    else:
                                        loopCounter = 0
                                        solved.change(self.strings['incomplete'])

                       
                    #save custom created board
                    else:
			#blocksToWrite.append["0"]
                        if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                            for block in allBlocks:
                                if (not int(block.north) == 0) and (not int(block.east) == 0) and (not int(block.south) == 0) and (not int(block.west) == 0):
                                    blocksToWrite.append(str(block.rect.x) + " " + str(block.rect.y) + " " + str(block.north) + " " + str(block.east) + " " + str(block.south) + " " + str(block.west))
                                    numBlocks += 1
                            if numBlocks > 0:
				#blocksToWrite.append["0"]
                                boardName = ask(self.screen, self.strings['boardName'], 529, 10, 450, 30, 42, False, 10, False)
                                allsprites.update()
                                screen.blit(background, (0,0))
                                allsprites.draw(screen)
                                pygame.display.flip()
                                objText = ask(self.screen, self.strings['objectiveText'], 250, 10, 750, 30, 30, False, 60)
                                
                                blocksToWrite[0] = str(numBlocks)
                                blocksToWrite.append(objText)
		
				#add teh board to the list of available boards
                                temp = open("data" + os.sep + "boardList.txt", 'r')
                                tempList = (temp.read()).rsplit('\n')
                                tempList = tempList[:-1]
                                temp = file("data" + os.sep + "boardList.txt", 'w')
                                temp.write(boardName + '\n')
                                for line in tempList:
                                    temp.write(line + '\n')
                                temp.close()
				#write the actual board itself
                                f = open("boards" + os.sep + boardName + ".txt", 'w')
                                for line in blocksToWrite:
				    #print line
                                    f.write(line + "\n")
                                f.close()
                            else:
                                timeText.change(self.strings['atLeastOne'])
                                
                     #main menu button
                    if cursor.rect.x > 0 and cursor.rect.x < 240 and cursor.rect.y > 809 and cursor.rect.y < 900:
                        mainMenu = MainMenu()
                                
                elif e.type == MOUSEBUTTONUP:
                    event.set_grab(0)
                if e.type == KEYDOWN:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        event.set_grab(1)
                #on click of the check answer button if done with keyboard
                elif e.type == KEYUP:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        event.set_grab(0)
                        if not editMode:
                            if not completed:
                            #check answer button
                                if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                                        result = Solve(allBlocks)
                                        if result == 'Solved!':
                                            solved.change(self.strings['win'])
                                            completed = True
                                        else:
                                            loopCounter = 0
                                            solved.change(self.strings['incomplete'])

                            
                        #save custom created board
                        else:
                            #blocksToWrite.append["0"]
                            if cursor.rect.x > 954 and cursor.rect.x < 1200 and cursor.rect.y > 809 and cursor.rect.y < 900:
                                for block in allBlocks:
                                    if (not int(block.north) == 0) and (not int(block.east) == 0) and (not int(block.south) == 0) and (not int(block.west) == 0):
                                        blocksToWrite.append(str(block.rect.x) + " " + str(block.rect.y) + " " + str(block.north) + " " + str(block.east) + " " + str(block.south) + " " + str(block.west))
                                        numBlocks += 1
                                if numBlocks > 0:
			    	    #blocksToWrite.append["0"]
                                    boardName = ask(self.screen, self.strings['boardName'], 529, 10, 450, 30, 42, False, 10, False)
                                    allsprites.update()
                                    screen.blit(background, (0,0))
                                    allsprites.draw(screen)
                                    pygame.display.flip()
                                    objText = ask(self.screen, self.strings['objectiveText'], 250, 10, 750, 30, 30, False, 60)
                                    
                                    blocksToWrite[0] = str(numBlocks)
                                    blocksToWrite.append(objText)
				    
				    #add the boardname to the list of boards available
                                    temp = open("data" + os.sep + "boardList.txt", 'r')
                                    tempList = (temp.read()).rsplit('\n')
                                    tempList = tempList[:-1]
                                    temp = file("data" + os.sep + "boardList.txt", 'w')
                                    temp.write(boardName + '\n')
                                    for line in tempList:
                                        temp.write(line + '\n')
                                    temp.close()
				    
   			  	    #write the board itself
                                    f = open("boards" + os.sep + boardName + ".txt", 'w')
                                    for line in blocksToWrite:
				        #print line
                                        f.write(line + "\n")
                                    f.close()
                                else:
                                    timeText.change(self.strings['atLeastOne'])
                       #main menu button
                        if cursor.rect.x > 0 and cursor.rect.x < 240 and cursor.rect.y > 809 and cursor.rect.y < 900:
                            mainMenu = MainMenu()


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
                
            #let cursor follow mouse again
            if mousePossible == True:
                cursor.mouseMoved(mouse.get_pos())
            
            if not (keystate[K_KP1] or keystate[K_RETURN]):
                keyDown = False

            #main game logic. drag and drop, snap to grid, rotation
            if not editMode and not completed:
                for block in allBlocks:
                    #Block rotation when pressing enter
                    if (curMode == 1 and not (dif == 1 or dif == 2)) or curMode == 2 or (curMode == 3 and not dif == 1):
                        if block.isLast == 1 and (keystate[K_KP1] or keystate[K_RETURN]) and not keyDown:
                            block.rotate()
                            numRotate += 1
                            keyDown = True
                    isLast = block

                    #For block dragging
                    if event.get_grab():
                        #debugText += ' holding mouse button 1'
                        # and block.isGrabbed() == False
                        allsprites.move_to_front(block)
                        allsprites.move_to_front(solved)
                        allsprites.move_to_front(hi)
                        allsprites.move_to_front(cursor)
                        if block.rect.collidepoint([cursor.rect.x,cursor.rect.y]):
                            anotherBlock = 0
                            hi.setpos([block.rect.x,block.rect.y])
                            for blockB in allBlocks:
                                if blockB.isMoving == True and blockB != block:
                                    anotherBlock = 1
                                    break
                            if anotherBlock == 0:
                                if curMode == 1 or curMode == 3:
                                    block.grab([cursor.rect.x, cursor.rect.y])
                                    hi.setpos([block.rect.x,block.rect.y])
                                block.setGrabbed(True)
                                for tempblock in allBlocks:
                                    tempblock.isLast = 0
                                block.isLast = 1
                                isRan = 1
                                break
                        elif block.isMoving == True and (curMode == 1 or curMode == 3):
                            block.grab([cursor.rect.x, cursor.rect.y])
                    #snapping to grid
                    elif isRan == 1 and block.isLast == 1:
                        for piece in gridpos:
                            if cursor.rect.x > piece[0] and cursor.rect.x < piece[0]+108 and cursor.rect.y > piece[1] and cursor.rect.y < piece[1]+108 and block.isMoving == True and (curMode == 1 or curMode == 3):
                                place = piece[0] + 54, piece[1] + 54
                                isLast.grab(place)
                                isRan = 0
                        block.setGrabbed(False)
                    if block.rect.collidepoint([cursor.rect.x,cursor.rect.y]) and event.get_grab():
                        hi.setpos([block.rect.x,block.rect.y])
                    """else:
                        hi.setpos([block.rect.x,block.rect.y])
                        continue"""
                    #else:
                    #    hi.setpos([1300,900])
                    #elif not (cursor.rect.x > block.rect.x and cursor.rect.x < block.rect.x +96 and cursor.rect.y > block.rect.y and cursor.rect.y < block.rect.y + 96):
                    #    hi.setpos([1300,900])
            #board editor
            elif editMode:
                if event.get_grab():
                    for block in allBlocks:
                        if block.rect.collidepoint([cursor.rect.x,cursor.rect.y]):
                            timeText.change('')
                            #Edit each side individually
                            n = ask(self.screen, "Enter North", 529, 30, 300, 30, 42, True, 6)
                            east = ask(self.screen, "Enter East", 529, 30, 300, 30, 42, True, 6)
                            s = ask(self.screen, "Enter South", 529, 30, 300, 30, 42, True, 6)
                            w = ask(self.screen, "Enter West", 529, 30, 300, 30, 42, True, 6)
                            block.edit(n,east,s,w)
                            event.set_grab(0)

            # note random here is random.random()
            # note foreach here is for object in
            allsprites.update()
            allsprites.draw(screen)
            pygame.display.flip()
            if not event.get_grab():
                hi.setpos([1300,900])
            
            if completed and nname == 'null' and not failed:
                wName = load_image('winName.png')
                screen.blit(wName,(374,231))
                nname = ask(self.screen, "Name", 400, 382, 300, 30, 42, False, 8)

                if not curMode == 2:
                    #rewrites the highscores so most recent is at top, and only 5 total are ever written
                    highScores[4] = highScores[3]
                    highScores[3] = highScores[2]
                    highScores[2] = highScores[1]
                    highScores[1] = highScores[0]
                    if cas == 1:
                        highScores[0] = nname + ' ' + curTime
                    #if against time, calculate time taken, and add leading zeroes if necessary
                    else:
                        mins = origMin - mins
                        timer = origSec - timer + 1
                        if mins < 10:
                            mins = str("0" + str(mins))
                        if timer < 10:
                            timer = str("0" + str(timer))
                        mins = str(mins)
                        timer = str(timer)
                        curTime = mins + ":" + timer
                        highScores[0] = nname + ' ' + curTime
                        timeText.change('Time Taken  ' + curTime)
                    if curMode == 1:
                        scores = open("scores" + os.sep + "timeRecent.txt", 'w')
                    elif curMode == 3:
                        scores = open("scores" + os.sep + name + "Scores.txt", 'w')
                    for score in highScores:
                        scores.write(score + '\n')
                    scores.close()
            elif failed:
                solved.change("Out of time")

            #update everything
            allsprites.update()
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)
            
class Text(pygame.sprite.Sprite):
    text = ' '
    def __init__(self,txt=' ',x=0,y=0,clr='black',size=42):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, size)
        self.color = Color(clr)
        self.update()
        self.rect = self.image.get_rect().move(x, y)
        self.text = txt

    def update(self):
        msg = self.text
        self.image = self.font.render(msg, 1, self.color)

    def change(self, new=' '):
        self.text = new
        self.update()
    
class mouseUpdate(pygame.sprite.Sprite):
    def __init__(self, pos):
        x,y = pos
        pygame.sprite.Sprite.__init__(self)
        thisImg = load_image('mouse.png', True)
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
    cas = 1
    text = ""
    goodLoad = False
    boardList = []
    listCounter = 0
    strings = {}
    def __init__(self):
        self.paused = False
        self.clock = pygame.time.Clock()
	

	#load language strings
        self.strings = loadDictionary('bl_english.txt')

        #set the screen up
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        self.loadList()
	#for l in self.boardList:
	#    print l
        self.text = self.boardList[0]

        pygame.display.set_caption('Blocku')
        self.menuImg = load_image('bg.png')
        self.instImg = load_image('instructions.png')
        self.menuWI = load_image('menuWithInst.png')
        self.subAdd = load_image('subAdd.png')
        self.gModes = load_image('modesMain.png')
        self.hi = load_image('mainhi.png', True)
        self.leftArrow = load_image('left.png')
        self.rightArrow = load_image('right.png')
        self.button = load_image('button.png')
        self.delButton = load_image('del.png')

        if pygame.font:
            self.selRng = Text('',575,400,'black',42)
            self.selRng2 = Text('',575,350,'black',42)
            self.selDifficulty = Text('',575,550,'black',42)
            self.selSub = Text('',575,105,'black',42)
            self.selCas = Text('',575,260,'black',42)

        self.screen = pygame.display.set_mode((1200,900))
        #self.screen.blit(self.menuImg,(0,0))
        #get the image and screen in the same format

        screen.blit(self.menuImg, (0,0))

        text = pygame.font.Font(None, 42)
        self.welp = self.wrapline(self.strings['instructions'],text,500)
        
        self.addText()
        pygame.display.flip()
        self.loop()

    def loadList(self):
        ff = open('data' + os.sep + 'boardList.txt', 'r')
        temp = ff.read()
        self.boardList = temp.split('\n')
        self.boardList = self.boardList[:-1]

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
            exitt = font.render(self.strings['exit'], 1, (255,255,255))
            self.screen.blit(exitt,[570,810])

            if self.modeBool == False:
                #Game Modes
                gMode = font.render(self.strings['gModes'], 1, (255,255,255))
                self.screen.blit(gMode,[520,660])
            else:
                #apply and close for gModes
                closeG = pygame.font.Font(None, 38)
                close = closeG.render(self.strings['apply'],1,(0,0,0))
                self.screen.blit(close,[995,692])

                #Time attack       126,198
                tAttack = pygame.font.Font(None, 55)
                time = tAttack.render(self.strings['timeAttack'],1,(0,0,0))
                self.screen.blit(time,[149,250])

                #Puzzle            126,377
                puzzle = pygame.font.Font(None, 55)
                puz = puzzle.render(self.strings['puzzle'],1,(0,0,0))
                self.screen.blit(puz,[149,430])

                #Story Mode              126,572
                stryMode = pygame.font.Font(None, 55)
                stry = stryMode.render(self.strings['custom'],1,(0,0,0))
                self.screen.blit(stry,[149,625])

            #instructions panel
            if self.instBool == True:
                newFont = pygame.font.Font(None, 100)
                instTitle = newFont.render(self.strings['inst'], 1, (255,0,0))
                self.screen.blit(instTitle,[390,310])
                
                for i in range(len(self.welp)):
                    newTxt=pygame.font.Font(None,42)
                    newInst = newTxt.render(self.welp[i],1,(0,0,0))
                    self.screen.blit(newInst,[370,370+(28*i)])

                closeF = pygame.font.Font(None, 28)
                close = closeF.render(self.strings['close'],1,(255,0,0))
                self.screen.blit(close,[800,577])
                
            elif self.modeBool == False:
                #New Game
                new = font.render(self.strings['newGame'], 1, (255, 255, 255))
                self.screen.blit(new, [530,375])

                #Instructions
                instructs = font.render(self.strings['inst'], 1, (255,255,255))
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

    def casChange(self):
        if self.cas == 0:
            self.cas = 1
        else:
            self.cas = 0

    def fileChange(self, change):
        if change == 0:
            self.listCounter -= 1
        else:
            self.listCounter += 1

        if self.listCounter > (len(self.boardList) - 2):
            self.listCounter = 0
        if self.listCounter < 0:
            self.listCounter = len(self.boardList) - 2

        self.text = self.boardList[self.listCounter]

    def loop(self):
        pygame.mouse.set_visible(False)
        cursor = mouseUpdate(mouse.get_pos())
        allsprites = pygame.sprite.LayeredUpdates()
        allsprites.add((self.selRng, self.selDifficulty, self.selSub, self.selRng2, self.selCas))
        allsprites.add(cursor)
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
                mousePossible = False
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
                        pygame.quit()
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
                        game.run(self.curSel, self.selRange, self.selDiff, self.selSubtraction, self.text, self.cas)
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
                            self.menuImg.blit(self.hi,(127,220))
                        elif self.curSel == 2:
                            self.menuImg.blit(self.hi,(127,399))
                        elif self.curSel == 3:
                            self.menuImg.blit(self.hi,(127,594))                        

                        #click on time attack
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 176 and cursor.rect.y < 354:
                            self.curSel = 1
                            self.menuImg.blit(self.gModes, (101,167))
                            #which is selected?
                            self.menuImg.blit(self.hi,(127,220))

                        #click on puzzle
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 366 and cursor.rect.y < 540:
                            self.curSel = 2
                            self.menuImg.blit(self.gModes, (101,167))
                            self.selDiff = 1
                            #which is selected?
                            self.menuImg.blit(self.hi,(127,399))

                        #click on story
                        if cursor.rect.x > 109 and cursor.rect.x < 435 and cursor.rect.y > 550 and cursor.rect.y < 730:
                            self.curSel = 3
                            self.selDiff = 1
                            self.menuImg = load_image('bg.png')
                            self.menuImg.blit(self.gModes, (101,167))
                            #which is selected?
                            self.menuImg.blit(self.hi,(127,594))

                        #if time attack or puzzle mode is selected
                        if self.curSel == 1 or self.curSel == 2:
                            
                            difficulty = pygame.font.Font(None,42).render(self.strings['selectDifficulty'],1,(0,0,0))
                            self.menuImg.blit(difficulty,(526,498))

                            self.menuImg.blit(self.subAdd, (511,72))
                            self.menuImg.blit(self.leftArrow, (529,100))
                            self.menuImg.blit(self.rightArrow, (909,100))
                            self.menuImg.blit(self.leftArrow,(529,543))
                            self.menuImg.blit(self.rightArrow,(909,543))

                            if self.curSel == 1:
                                numRange = pygame.font.Font(None,42).render(self.strings['selectNumber'],1,(0,0,0))
                                self.menuImg.blit(numRange,(526,348))
                                self.menuImg.blit(self.leftArrow,(529,391))
                                self.menuImg.blit(self.rightArrow,(909,391))
                                self.menuImg.blit(self.leftArrow,(529,254))
                                self.menuImg.blit(self.rightArrow,(909,254))
                                
                                #range left arrow
                                if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 391 and cursor.rect.y < 433:
                                    self.rangeChange(1)

                                #range right arrow
                                if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 391 and cursor.rect.y < 433:
                                    self.rangeChange(2)

                                #casual left arrow
                                if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 254 and cursor.rect.y < 296:
                                    self.casChange()

                                #casual right arrow
                                if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 254 and cursor.rect.y < 296:
                                    self.casChange()
                            else:
                                numRange = pygame.font.Font(None,42).render(self.strings['selectNumber'],1,(0,0,0))
                                self.menuImg.blit(numRange,(526,298))
                                self.menuImg.blit(self.leftArrow,(529,341))
                                self.menuImg.blit(self.rightArrow,(909,341))
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
			    #self.loadList()
			    #self.text = self.boardList[0]

                            #difficulty buttons
                            self.menuImg.blit(self.leftArrow,(529,543))
                            self.menuImg.blit(self.rightArrow,(909,543))

                            #board name buttons
                            self.menuImg.blit(self.leftArrow,(529,375))
                            self.menuImg.blit(self.rightArrow,(909,375))
                            
                            self.menuImg.blit(self.button,(546,215))
                            
                            difficulty = pygame.font.Font(None,42).render(self.strings['selectDifficulty'],1,(0,0,0))
                            self.menuImg.blit(difficulty,(526,498))

                            boardEnter = pygame.font.Font(None,42).render(self.strings['enterBoardName'],1,(0,0,0))
                            self.menuImg.blit(boardEnter,(526,350))

                            createText = pygame.font.Font(None,42).render(self.strings['createBoard'],1,(0,0,0))
                            self.menuImg.blit(createText,(570,225))

                            #delete button
                            delText = pygame.font.Font(None,40).render(self.strings['delete'],1,(0,0,0))
                            self.menuImg.blit(self.delButton,(981,371))
                            self.menuImg.blit(delText,(985,380))
                            
                            #difficulty left arrow
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(1)

                            #difficulty right arrow
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 543 and cursor.rect.y < 585:
                                self.diffChange(2)

                            #board left
                            if cursor.rect.x > 529 and cursor.rect.x < 554 and cursor.rect.y > 375 and cursor.rect.y < 417:
                                #next in array
                                self.fileChange(0)

                            #board right
                            if cursor.rect.x > 909 and cursor.rect.x < 934 and cursor.rect.y > 375 and cursor.rect.y < 417:
                                #next in array
                                self.fileChange(1)

                            #delete button
                            if cursor.rect.x > 981 and cursor.rect.x < 1095 and cursor.rect.y > 371 and cursor.rect.y < 418:
                                tempList = self.boardList
                                toDeleteFile = file('data' + os.sep + 'boardList.txt', 'w')
                                for i in range(len(self.boardList)-1):
                                    if not self.boardList[i] == self.text:
                                        toDeleteFile.write(self.boardList[i]+'\n')
                                toDeleteFile.write('\n')
                                toDeleteFile.close()
                                os.remove("boards" + os.sep + self.text + ".txt")
                                if os.path.isfile("scores" + os.sep + self.text + "Scores.txt"):
                                    os.remove("scores" + os.sep + self.text + "Scores.txt")
                                self.loadList()
                                self.fileChange(1)

                            #create a board button
                            if cursor.rect.x > 546 and cursor.rect.x < 806 and cursor.rect.y > 215 and cursor.rect.y < 265:
                                game = Game()
                                game.run(self.curSel, self.selRange, self.selDiff, self.selSubtraction, 'boardMaker', 0)
                                pygame.quit()


                        #close gModes KEEP THIS LAST
                        if cursor.rect.x > 980 and cursor.rect.x < 1094 and cursor.rect.y > 684 and cursor.rect.y < 728:
                            if self.curSel == 3:
                                if os.path.isfile("boards" + os.sep + self.text + ".txt"):
                                    self.goodLoad = True
                                    if not os.path.isfile("scores" + os.sep + self.text + "Scores.txt"):
                                        ff = file("scores" + os.sep + self.text + "Scores.txt", 'w')
                                        for i in range(4):
                                            ff.write("Kaeedo 0:42 \n")
                                        ff.close()
                                else:
                                    self.goodLoad = False
                                    self.text = self.strings['noExist']
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
                        self.text = self.text[:-1]
                    elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
                        pass
                    elif event.type == KEYDOWN:
                        self.text += event.unicode.encode("ascii")
                    display_box(self.menuImg,'' + self.text, 575,380, 300, 30, 42)

                #display defaults
                if self.selSubtraction == 0 and self.modeBool == True and (self.curSel == 1 or self.curSel == 2):
                    self.selSub.change(self.strings['add'])
                else:
                    self.selSub.change(self.strings['sub'])
                    
                if self.modeBool == True and (self.curSel == 1 or self.curSel == 2):
                    if self.curSel == 2:
                        self.selRng.change('')
                        self.selCas.change('')
                        if self.selRange == 1:
                            self.selRng2.change('15 - 40')
                        elif self.selRange == 2:
                            self.selRng2.change('30 - 99')
                        elif self.selRange == 3:
                            self.selRng2.change('100 - 999')
                    else:
                        self.selRng2.change('')
                        if self.selRange == 1:
                            self.selRng.change('15 - 40')
                        elif self.selRange == 2:
                            self.selRng.change('30 - 99')
                        elif self.selRange == 3:
                            self.selRng.change('100 - 999')
                            
                        if self.cas == 1:
                            self.selCas.change(self.strings['casual'])
                        else:
                            self.selCas.change(self.strings['againstTime'])

                    if self.curSel == 1:
                        if self.selDiff == 1:
                            self.selDifficulty.change(self.strings['sNoRotation'])
                        elif self.selDiff == 2:
                            self.selDifficulty.change(self.strings['lNoRotation'])
                        elif self.selDiff == 3:
                            self.selDifficulty.change(self.strings['sWithRotation'])
                        elif self.selDiff == 4:
                            self.selDifficulty.change(self.strings['lWithRotation'])
                    else:
                        if self.selDiff == 1:
                            self.selDifficulty.change(self.strings['sWithRotation'])
                        elif self.selDiff == 2:
                            self.selDifficulty.change(self.strings['lWithRotation'])
                        
                elif self.modeBool == True and self.curSel == 3:
                    self.selRng.change('')
                    self.selSub.change('')
                    self.selCas.change('')
                    self.selRng2.change('')
                    if self.selDiff == 1:
                        self.selDifficulty.change(self.strings['noRotation'])
                    elif self.selDiff == 2:
                        self.selDifficulty.change(self.strings['withRotation'])
                else:
                    self.selRng2.change('')
                    self.selRng.change('')
                    self.selDifficulty.change('')
                    self.selSub.change('')
                    self.selCas.change('')
                            
            
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
