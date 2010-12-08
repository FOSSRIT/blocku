
"""Main Blocku game logic class

import every thing that the activity needs and run game code

Authored by Fran Rogers and Ariel Zamparini
"""

#!/usr/bin/python
import pygame, random, os.path, os
from pygame.locals import *
from pygame import *

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

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

# num - number of blocks on one side of grid (ex: pass in 3 for a 3x3 grid)
def GenerateAddition(num, answer):
    rows = list([] for i in range(num))
    blocks = list([] for i in range(num * num))
    for i in range(num):
        rows[i] = list([] for i in range(num))

    # x and y positions of starting point of grid
    x = 204
    y = 204
    # answer to solve for

    # populate the list with blocks
    #blocks are Block(n,s,e,w,x,y) xy= starting position
    for i in range(num):
        for k in range(num):
            temp = Block(-1, -1, -1, -1, (x + (i * 108)), (y + (k * 108)))
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

def Solve(blocks):
    for block in blocks:
        # checks original position
        if (block.rect.x != block.origX or block.rect.y != block.origY):
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
def LoadBoard():
    # File format:
    # ---------------
    # Number of blocks in board
    # X-Pos Y-Pos BlockHeight N S W E R G B
    # NSWE = directions
    # RGB = color of the block in RGB
    
    # For now, we'll ignore the block height and color
    try:
        file = open("boards\\testFile.txt", "r")
        numLines = file.readline()
        #print(numLines)
        blocks = list([] for i in range(int(numLines)))
        # read in each line and split it
        for i in range(int(numLines)):
            line = file.readline()
            args = line.rsplit()
            #blocks are Block(n,e,s,w,x,y) xy= starting position
            blocks[i] = Block(args[3], args[6], args[4], args[5], int(args[0]), int(args[1]))

        file.close()
    except:
        blocks = blocks[0] = Block(1, 2, 3, 4, int(5), int(6))
    
    return blocks

# Will grab the last line of the file
def LastLine(read_size = 1024):
    try:
        file = open("boards\\testFile.txt", 'rU')
        lines = file.readlines()
        file.close()
    except:
        lines = 'Solve for: X + Y = 61'

    return lines[len(lines)-1]

    
def GenerateGrid(blocks):
    gridPos = list([] for i in range(len(blocks)))

    for k in range(len(blocks)):
        gridPos[k] = (blocks[k].rect.x - 4 + 100, blocks[k].rect.y - 4 + 50)

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
    def __init__(self, n='', e='', s='', w='', x='', y=''):
        self.image = self.images[0].copy()
        self.blankImage = self.image.copy()
        Block.images = self.images[1:]
        if len(Block.images) == 0:
            Block.images = Block.permImages
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        #Block.images = Block.images[1:]
        self.rect = pygame.Rect(x,y,96,96)
        self.origX = x
        self.origY = y
        self.font = pygame.font.Font(None, 30)
        #self.font.set_italic(1)
        self.color = Color('black')
        self.update()
        self.north = n
        self.east  = e
        self.south = s
        self.west  = w
        self.origNorth = n
        self.origEast = e
        self.origSouth = s
        self.origWest = w

    def update(self):
        #keep the block on the screen
        self.rect = self.rect.clamp(SCREENRECT)
        #self.image = self.images[0].copy()
        self.image = self.blankImage.copy()
        self.image.blit(self.font.render(str(self.north), 0, self.color),(39,3))
        self.image.blit(self.font.render(str(self.east), 0, self.color),(65,42))
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
        #print x , y
        #print self.rect.left, self.rect.top
        #self.rect = self.rect.move(x, y)
        #remember the offset here is 48 as this will center the mouse in our 96 pixel image
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
        #print self.north, self.east, self.south, self.west

class Puzzle:
    def __init__(self):
        #self.rule   = rule
        self.blocks = {}

    def add_block(self, block, coords):
        self.blocks[coords] = block

    def get_blocks(self):
        return self.blocks

    def shuffle(self):
        pass


#the main game class
class Game:
    
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.puzzle = Puzzle()
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
    def run(self):
        pygame.mouse.set_visible(False)
        self.running = True
        isRan = 0
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        # load a test sound
        #pygame.mixer.music.load("sounds\\trololo.ogg")
        
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        
        squares = load_image('square.png')
        background = load_image('background.png')
        iconImg = load_image('blocku.png')
        self.screen = pygame.display.set_mode((1200,900))
        spriteBatch = pygame.sprite.RenderUpdates()
        
        # load images here
        # for gifs  img = load_image('filename.gif')
        # for bmps img = pygame.image.load('filename.bmp') but our function handles that for us
        # a note for graphics blit means copy pixels from screen.blit()
        

        
        # the test will need rects and positions i sugest make some kind of default
        # this information can be held by each block as they are created but is made here


        # load images to pipe to the sprite classes
        
        #Block.images = allBlockImages
        
        tempImages = [load_image('c1.png'),load_image('c2.png'),load_image('c3.png'),load_image('c4.png'),load_image('c5.png'),load_image('c6.png'),load_image('c7.png'),load_image('c8.png'),load_image('c9.png')]
        Block.images = tempImages
        Block.permImages = tempImages
        gridImg1 = squares
        gridImg2 = squares
        gridImg3 = squares
        gridImg4 = squares
        gridImg5 = squares
        gridImg6 = squares
        gridImg7 = squares
        gridImg8 = squares
        gridImg9 = squares
        allGrid = [gridImg1,gridImg2,gridImg3,gridImg4,gridImg5,gridImg6,gridImg7,gridImg8,gridImg9]


        
        
        #generate random number between 20 and 99 for the answer to equal
        answer = random.randint(20, 99)
        global debugText
        debugText = 'Arrange blocks so that addition equals ' + str(answer)
        #debugText = answerStr
        #see if there is a sprite font
        

        #main blocku code structs
        blocks = pygame.sprite.Group()
        Block.containers = blocks,spriteBatch
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
        allBlocks = GenerateAddition(3, answer) #*
        #allBlocks = LoadBoard() ##
        gridpos = GenerateGrid(allBlocks)
        answerStr = LastLine()  ##
        #answerStr = 'Arrange blocks so that addition equals ' + str(answer) #*
        #print(answerStr)
        Randomize(allBlocks)
        #print(allBlocks)

        # Default grid positions - handled now by GenerateGrid()
        #gridpos = [(200,200),(272,200),(344,200),(200,272),(272,272),(344,272),(200,344),(272,344),(344,344)]
        #print(gridpos[0][0])
        
        for i in range(len(gridpos)):
            background.blit(gridImg1, gridpos[i])


        #get the image and screen in the same format
        if background.get_bitsize() == 8:
            set_palette(background.get_palette())
        else:
            background.convert()

        screen.blit(background,(0,0))

        pygame.display.flip()

        #to set the icon up and to decorate the game window
        icon = pygame.transform.scale(iconImg, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Blocku')

        #this next call is sort of like sprite batch . drawf

        pygame.display.flip()
        
        #if a key is down
        global keyDown

        cursor = mouseUpdate()
        if pygame.font:
            spriteBatch.add(Text(''))
            
            #spriteBatch.add(mainText())
        spriteBatch.add(cursor)
        
        # it is important to note that like xna the origin is 0,0
        # the top left of the current window
        # print is trace in console
        # and increases as you go down and to the right
        # pygame has a collision detector under pygame.sprite.spritecollide(group,group,dokill)
        # this will return a list of colliders, dokill will remove the colliders from the parrent group if true
        mousePossible = True
        while self.running:
            keyDown = False
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
                elif e.type == MOUSEBUTTONUP:
                    event.set_grab(0)
                if e.type == KEYDOWN:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        print'still down'
                        event.set_grab(1)
                elif e.type == KEYUP:
                    if(e.key == K_SPACE) or (e.key == K_KP3):
                        print'going up'
                        event.set_grab(0)

            # get the state of the keyboard for input
            
            if not keystate[K_RETURN] or keystate[K_KP1]:
                keyDown = False
            # Checks to see if the puzzle is solved
            if keystate[K_a]:
                result = Solve(allBlocks)
                print(result)
                if (result == "Solved!"):
                    pygame.mixer.music.play()

            #if keystate[K_b]:
               # pygame.mixer.music.play()
            # for key test use keystate[key] and a return of true will occur when key down
            # clear/erase the last drawn sprites
            spriteBatch.clear(screen, background)
            # update all the sprites
            spriteBatch.update()

            #for block in blocks:
            x = cursor.rect.x
            y = cursor.rect.y

            
            #pygame.event.get()
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
            
            for block in allBlocks:
                #Block rotation when pressing enter
                if block.isLast == 1 and (keystate[K_RETURN] or keystate[K_KP1]) and not keyDown:
                    block.rotate()
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
                            block.grab([cursor.rect.x, cursor.rect.y])
                            block.setGrabbed(True)
                            #debugText += ' grabbed a Block'
                            for tempblock in allBlocks:
                                tempblock.isLast = 0
                            block.isLast = 1
                            isRan = 1
                            break
                    elif block.isMoving == True:
                        block.grab([cursor.rect.x, cursor.rect.y])
                elif isRan == 1 and block.isLast == 1:
                    for piece in gridpos:
                        if cursor.rect.x > piece[0] and cursor.rect.x< piece[0]+108 and cursor.rect.y > piece[1] and cursor.rect.y< piece[1]+108 and block.isMoving == True:
                            place = piece[0] + 54, piece[1] + 54
                            isLast.grab(place)
                            isRan = 0
                    block.setGrabbed(False)

            # note random here is random.random()
            # note foreach here is for object in

            # draw call for the screen
            draw = spriteBatch.draw(screen)
            pygame.display.update(draw)


            # Try to stay at 30 FPS
            self.clock.tick(30)

class Text(pygame.sprite.Sprite):
    text = ''
    def __init__(self,txt=''):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 38)
        #self.font.set_italic(1)
        self.color = Color('blue')
        self.update()
        self.rect = self.image.get_rect().move(253, 174)
        self.text = txt

    def update(self):
        global debugText
        msg = self.text + debugText
        self.image = self.font.render(msg, 0, self.color)

class mouseUpdate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        thisImg = load_image('mouse.png')
        self.image = thisImg
        self.update()
        self.rect = self.image.get_rect().move(50, 220)

    def update(self):
        self.image = load_image('mouse.png')

    def grab(self, pos):
        x, y = pos;
        globX=x
        globY=y
        self.rect.left = x-14
        self.rect.top = y-16

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
    def __init__(self):
        self.paused = False

        #set the screen up
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)


        pygame.display.set_caption('Blocku')
        self.menuImg = load_image('bg.png')
        self.background = load_image('background.png')
        self.instImg = load_image('instructions.png')

        self.screen = pygame.display.set_mode((1200,900))
        #self.screen.blit(self.menuImg,(0,0))
        #get the image and screen in the same format
        if self.background.get_bitsize() == 8:
            set_palette(self.background.get_palette())
        else:
            self.background.convert()

        screen.blit(self.menuImg, (0,0))
        
        self.addText()
        pygame.display.flip()

        self.loop()

    def addText(self):
        if pygame.font:
            font = pygame.font.Font(None, 50)

            #Exit
            exitt = font.render("Exit", 1, (255,255,255))
            self.screen.blit(exitt,[570,810])

            #instructions panel
            if self.instBool == True:
                newFont = pygame.font.Font(None, 100)
                instTitle = newFont.render("Instructions", 1, (255,0,0))
                self.screen.blit(instTitle,[390,314])

                closeF = pygame.font.Font(None, 28)
                close = closeF.render("Close",1,(255,0,0))
                self.screen.blit(close,[800,577])
                
            else:
                #New Game
                new = font.render("New Game", 1, (255, 255, 255))
                self.screen.blit(new, [530,375])

                #Game Modes
                gMode = font.render("Game Modes", 1, (255,255,255))
                self.screen.blit(gMode,[520,660])

                #Instructions
                instructs = font.render("Instructions", 1, (255,255,255))
                self.screen.blit(instructs,[520,520])

    def loop(self):
                
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:

                        #new game button is at (382,269) and is 311,122 pixels
                        #x gain of 84
                        #y gain of 60
                        #insturctions button is at (382, 392) and is 311,122 pixels
                        #game mode is at (382, 510) and is 311,122 pixels
                        #exit is at (382,625) and is 311,122 pixels
                        #220,212
                        #688,492    67,26
                        #new game. launches into a new game of blocku, with current default behavior of creating a new random grid
                        if event.pos[0] > 466 and event.pos[0] < 777 and event.pos[1] > 329 and event.pos[1] < 451 and self.instBool == False:
                            pygame.display.flip()
                            game = Game()
                            game.run()
                            pygame.quit()
                            
                        #insturctions
                        if event.pos[0] > 466 and event.pos[0] < 777 and event.pos[1] > 478 and event.pos[1] < 600 and self.instBool == False:
                            #pygame.display.flip()
                            self.instBool = True
                            self.screen.blit(self.instImg, (328,294))
                            self.addText()
                            pygame.display.flip()
                        
                        #close insturctions button
                        if event.pos[0] > 798 and event.pos[0] < 865 and event.pos[1] > 573 and event.pos[1] < 599 and self.instBool == True:
                            self.screen.blit(self.menuImg, (0,0))
                            self.instBool = False
                            self.addText()
                            pygame.display.flip()
                            

                        #exit button. exits the game
                        if event.pos[0] > 466 and event.pos[0] < 777 and event.pos[1] > 765 and event.pos[1] < 887 and self.instBool == False:
                            pygame.quit()



# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    mMenu = MainMenu()
    pygame.quit()
    #mMenu.run()
    # Initialize pygame
    #pygame.init()

    # Initialize a game
    #game = Game()

    #mainMenu()

    # Run the game
    #game.run()
    #pygame.quit()

#call the "main" function if python is running this script
if __name__ == '__main__':
    main()

