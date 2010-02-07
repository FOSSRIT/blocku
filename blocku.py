#!/usr/bin/python
import pygame, random, os.path
from pygame.locals import *
from pygame import *
#import gtk

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit, "Sorry, extended image module required"

#game constants
SCREENRECT     = Rect(0, 0, 640, 480)
KEYBOARDMOVESPEED = 10


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

class Block(pygame.sprite.Sprite):
    images = []
    def __init__(self, north=None, east=None, south=None, west=None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(300, 300)
        self.north = north
        self.east  = east
        self.south = south
        self.west  = west

    def update(self):
        pass
        #if (mouseMove)
        #    self.rect.move(mouseX-posRelX,mouseY-posRelY)
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
        #keep the block on the screen
        self.rect = self.rect.clamp(SCREENRECT)

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

        #set the screen up
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)


        # load images here
        # for gifs  img = load_image('filename.gif')
        # for bmps img = pygame.image.load('filename.bmp') but our function handles that for us
        # a note for graphics blit means copy pixels from screen.blit()
        iconImg = load_image('Blocku_Icon.gif')
        #background = load_image('background.gif')
        background = load_image('background.bmp')
        # load images to pipe to the sprite classes
        blockImg = load_image('block.bmp')
        Block.images = [blockImg]
        # the test will need rects and positions i sugest make some kind of default
        # this information can be held by each block as they are created but is made here

        #get the image and screen in the same format
        if background.get_bitsize() == 8:
            screen.set_palette(background.get_palette())
        else:
            background = background.convert()

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
        Block.containers = spriteBatch
        aBlock = Block()

        #see if there is a sprite font
        if pygame.font:
            spriteBatch.add(Text(text = 'helloworld'))
            spriteBatch.add(mouseUpdate())

        # it is important to note that like xna the origin is 0,0
        # the top left of the current window
        # and increases as you go down and to the right
        # pygame has a collision detector under pygame.sprite.spritecollide(group,group,dokill)
        # this will return a list of colliders, dokill will remove the colliders from the parrent group if true

        while self.running:
            # Pump GTK messages.
            #while gtk.events_pending():
            #    gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)

            # get the state of the keyboard for input
            keystate = pygame.key.get_pressed()
            # for key test use keystate[key] and a return of true will occur when key down

            # clear/erase the last drawn sprites
            spriteBatch.clear(screen, background)
            # update all the sprites
            spriteBatch.update()
            # handle player input
            if keystate[K_UP]:
                aBlock.move(0)
            if keystate[K_RIGHT]:
                aBlock.move(1)
            if keystate[K_DOWN]:
                aBlock.move(2)
            if keystate[K_LEFT]:
                aBlock.move(3)
            # note random here is random.random()
            # note foreach here is for object in

            # draw call for the screen
            draw = spriteBatch.draw(screen)
            pygame.display.update(draw)

            # Try to stay at 30 FPS
            self.clock.tick(30)

class Text(pygame.sprite.Sprite):
    def __init__(self,text="blank"):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('blue')
        self.update()
        self.rect = self.image.get_rect().move(50, 200)
        self.text = text

    def update(self):
        msg = 'Drawing call test'
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

