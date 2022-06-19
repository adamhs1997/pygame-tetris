import pygame, sys, random
from pygame.locals import *

from grid import Grid
pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
GRID_WIDTH = 10 # Cells
GRID_HEIGHT = 22 # Top 2 hidden
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 550
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# The main function that controls the game
def main () :
  grid = Grid()
  looping = True
  last_update_time = 0
  xPos = 0
  yPos = 0
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      # There are also events for keypresses, but only fired once (like onKeyDown)
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
        
    keyPresses = pygame.key.get_pressed()
    # if (keyPresses[K_RIGHT]):
        # xPos = min(xPos + CELL_SIZE, WINDOW_WIDTH)
    # if (keyPresses[K_LEFT]):
        # xPos = max(xPos - CELL_SIZE, 0)
    # if (keyPresses[K_UP]):
        # yPos = min(yPos - CELL_SIZE, WINDOW_HEIGHT)
    # if (keyPresses[K_DOWN]):
        # yPos = max(yPos + CELL_SIZE, 0)    

    if grid.new_cell_needed():
        print("adding cell")
        grid.add_cell()
        last_update_time = pygame.time.get_ticks()
        
    # Move the cell down one cell length every second (half second if down key held)
    update_time_interval = 500 if keyPresses[K_DOWN] else 1000
    current_time = pygame.time.get_ticks()
    if (current_time - last_update_time > update_time_interval):
        print("moving cell")
        grid.move_current_cell()
        last_update_time = current_time
 
    # Render elements of the game
    WINDOW.fill(BACKGROUND)
    grid.draw(WINDOW)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
