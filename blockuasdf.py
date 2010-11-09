
"""Main Blocku game logic class

import every thing that the activity needs and run game code

Authored by Fran Rogers and Ariel Zamparini
"""

#!/usr/bin/python
import pygame, random, os.path
from pygame.locals import *
from pygame import *

try: import gtk
except ImportError: gtk = None

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#game constants
SCREENRECT     = Rect(0, 0, 640, 480)
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

class Block(pygame.sprite.Sprite):
    images = []
    north=''
    east=''
    south=''
    west=''
    isLast = 0
    isMoving = False
    globX=1
    globY=1
    def __init__(self, n='', e='', s='', w='', x='', y=''):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0].copy()
        self.rect = pygame.Rect(x,y,64,64)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update()
        self.north = n
        self.east  = e
        self.south = s
        self.west  = w

    def update(self):
        #keep the block on the screen
        self.rect = self.rect.clamp(SCREENRECT)
        self.image = self.images[0].copy()
        self.image.blit(self.font.render(str(self.north), 0, self.color),(26,3))
        self.image.blit(self.font.render(str(self.east), 0, self.color),(47,25))
        self.image.blit(self.font.render(str(self.south), 0, self.color),(26,47))
        self.image.blit(self.font.render(str(self.west), 0, self.color),(5,25))
        # game logic here for snapping to grid ...?
        # when the block is snapped to the grid clamp the rect there
    def move(self, direction):
        # up = 0, right = 1, down = 2, left = 3
        if direction == 0:
            self.rect.move_ip(0,-KEYBOARDMOVESPEED)
        if direction == 1:
            self.rect.move_ip(KEYBOARDMOVESPEED,0)
        if direction == 2:
            self.rect.move_ip(0,KEYBOARDMOVESPEED)
        if direction == 3:
            self.rect.move_ip(-KEYBOARDMOVESPEED,0)
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
        #remember the offset here is 32 as this will center the mouse in our 64pixel image
        self.rect.left = x-32
        self.rect.top = y-32
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
        self.running = True
        isRan = 0
        if pygame.mixer and not pygame.mixer.get_init():
            print('Warning, no sound')
            pygame.mixer = None

        #set the screen up
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)


        # load images here
        # for gifs  img = load_image('filename.gif')
        # for bmps img = pygame.image.load('filename.bmp') but our function handles that for us
        # a note for graphics blit means copy pixels from screen.blit()
        iconImg = load_image('blocku.png')
        background = load_image('background.png')
        # load images to pipe to the sprite classes
        blockImg = load_image('block.png')
        Block.images = [blockImg]
        gridImg1 = load_image('square.png')
        gridImg2 = load_image('square.png')
        gridImg3 = load_image('square.png')
        gridImg4 = load_image('square.png')
        gridImg5 = load_image('square.png')
        gridImg6 = load_image('square.png')
        gridImg7 = load_image('square.png')
        gridImg8 = load_image('square.png')
        gridImg9 = load_image('square.png')

        allGrid = [gridImg1,gridImg2,gridImg3,gridImg4,gridImg5,gridImg6,gridImg7,gridImg8,gridImg9]
        
        # the test will need rects and positions i sugest make some kind of default
        # this information can be held by each block as they are created but is made here

        #get the image and screen in the same format
        if background.get_bitsize() == 8:
            screen.set_palette(background.get_palette())
        else:
            background = background.convert()
        gridpos = [(200,200),(272,200),(344,200),(200,272),(272,272),(344,272),(200,344),(272,344),(344,344)]
        background.blit(gridImg1, gridpos[0])
        background.blit(gridImg2, gridpos[1])
        background.blit(gridImg3, gridpos[2])
        background.blit(gridImg4, gridpos[3])
        background.blit(gridImg5, gridpos[4])
        background.blit(gridImg6, gridpos[5])
        background.blit(gridImg7, gridpos[6])
        background.blit(gridImg8, gridpos[7])
        background.blit(gridImg9, gridpos[8])
        
        screen.blit(background,(0,0))
        pygame.display.flip()

        #to set the icon up and to decorate the game window
        icon = pygame.transform.scale(iconImg, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Blocku')

        #this next call is sort of like sprite batch . draw
        spriteBatch = pygame.sprite.RenderUpdates()

        #main blocku code structs
        blocks = pygame.sprite.Group()
        Block.containers = blocks,spriteBatch
        #blocks are Block(n,s,e,w,x,y) xy= starting position
        
        aBlock = Block(1,2,3,4,200,200)
        bBlock = Block(5,6,7,8,300,300)
        cBlock = Block(9,1,2,3,250,250)
        dBlock = Block(4,5,6,7,350,350)
        eBlock = Block(2,1,9,8,400,400)
        fBlock = Block(3,4,5,6,450,450)
        gBlock = Block(1,9,8,7,500,500)
        hBlock = Block(2,3,4,5,550,550)
        iBlock = Block(9,8,7,6,150,150)
        allBlocks=[aBlock,bBlock,cBlock,dBlock,eBlock,fBlock,gBlock,hBlock,iBlock]

        global debugText
        debugText = ''
        #see if there is a sprite font
        if pygame.font:
            spriteBatch.add(Text('Drawing call test '))
            spriteBatch.add(mouseUpdate())

        #if a key is down
        global keyDown
        keyDown = False
        # it is important to note that like xna the origin is 0,0
        # the top left of the current window
        # print is trace in console
        # and increases as you go down and to the right
        # pygame has a collision detector under pygame.sprite.spritecollide(group,group,dokill)
        # this will return a list of colliders, dokill will remove the colliders from the parrent group if true

        while self.running:
            # Pump GTK messages.
            while gtk and gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for e in event.get():
                if e.type == QUIT or \
                    (e.type == KEYDOWN and e.key == K_ESCAPE):
                        return
                elif e.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(e.size, pygame.RESIZABLE)
                if e.type == MOUSEBUTTONDOWN:
                    event.set_grab(1)
                elif e.type == MOUSEBUTTONUP:
                    event.set_grab(0)

            # get the state of the keyboard for input
            keystate = pygame.key.get_pressed()
            if not keystate[K_SPACE]:
                keyDown = False
            # for key test use keystate[key] and a return of true will occur when key down
            # clear/erase the last drawn sprites
            spriteBatch.clear(screen, background)
            # update all the sprites
            spriteBatch.update()
            
            #for block in blocks:
            x, y = mouse.get_pos()
            
            for block in allBlocks:
               # if keystate[K_SPACE] and not keyDown:
               #     block.rotate()
               #     keyDown = True
                if block.isGrabbed() == True:
                    debugText='ZOMG TORRENT PLZ'
                isLast = block
                if event.get_grab():
                    debugText += ' holding mouse button 1'
                    # and block.isGrabbed() == False
                    if block.rect.collidepoint(x,y):
                        block.grab(mouse.get_pos())
                        block.setGrabbed(True)
                        debugText += ' grabbed a Block'
                        for tempblock in allBlocks:
                            tempblock.isLast = 0
                        block.isLast = 1
                        isRan = 1
                        break
                elif isRan == 1 and block.isLast == 1:
                    debugText = ''
                    block.setGrabbed(False)
                    #block.left = 250
                    for piece in gridpos:
                        if mouse.get_pos()[0] > piece[0] and mouse.get_pos()[0]< piece[0]+72 and mouse.get_pos()[1] > piece[1] and mouse.get_pos()[1]< piece[1]+72:
                            debugText=str(piece)
                            place = piece[0] + 36, piece[1] + 36
                            isLast.grab(place)
                            isRan = 0

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
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update()
        self.rect = self.image.get_rect().move(55, 80)
        self.text = txt

    def update(self):
        global debugText
        msg = self.text + debugText
        self.image = self.font.render(msg, 0, self.color)

class mouseUpdate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update()
        self.rect = self.image.get_rect().move(50, 220)

    def update(self):
        msg = 'Mouse Position %s, %s' % mouse.get_pos()
        self.image = self.font.render(msg, 0, self.color)

# This function is called when the game is run directly from the command line:
# ./TestGame.py 
def main():
    # Initialize pygame
    pygame.init()

    # Initializa game
    game = Game()

    # Run the game
    game.run()

#call the "main" function if python is running this script
if __name__ == '__main__':
    main()

