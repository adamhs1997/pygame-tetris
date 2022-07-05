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
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 550
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# The main function that controls the game
def main () :
  grid = Grid()
  looping = True
  last_update_time = 0
  lateral_last_update_time = 0
  lateral_update_time_interval = 300
  move_left = False
  move_right = False
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      # There are also events for keypresses, but only fired once (like onKeyDown)
      if event.type == QUIT :
        pygame.quit()
        sys.exit()

    if grid.new_cell_needed():
        grid.add_cell()
        last_update_time = pygame.time.get_ticks()

    keyPresses = pygame.key.get_pressed()
    if (keyPresses[K_RIGHT]):
        move_right = True
    if (keyPresses[K_LEFT]):
        move_left = True
        
    # Move the cell down one cell length every second (half second if down key held)
    update_time_interval = 500 if keyPresses[K_DOWN] else 1000
    current_time = pygame.time.get_ticks()
    if (current_time - lateral_last_update_time > lateral_update_time_interval):
        if move_right:
            grid.move_current_cell_right()
            move_right = False
        if move_left:
            grid.move_current_cell_left()
            move_left = False
        lateral_last_update_time = current_time
    if (current_time - last_update_time > update_time_interval):
        grid.move_current_cell_down()
        last_update_time = current_time
 
    # Render elements of the game
    WINDOW.fill(BACKGROUND)
    grid.draw(WINDOW)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
