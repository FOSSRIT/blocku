#!/usr/bin/python
import pygame
#import gtk

class Block:
    pass

class Puzzle:
    def __init__(self, width, height, rule, edges, blocks=None):
        self.width  = width
        self.height = height
        self.rule   = rule
        self.edges  = edges
        self.blocks = blocks or []
        
    def add_block(self, block):
        self.blocks.push(block)

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
            
        screen = pygame.display.get_surface()

        while self.running:
            # Pump GTK messages.
            #while gtk.events_pending():
            #    gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
            
            
            
            # Try to stay at 30 FPS
            self.clock.tick(30)

# This function is called when the game is run directly from the command line:
# ./TestGame.py 
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = Game() 
    game.run()

if __name__ == '__main__':
    main()

