import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# The main function that controls the game
def main () :
  looping = True
  xPos = 10
  yPos = 10
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      # There are also events for keypresses, but only fired once (like onKeyDown)
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
        
    keyPresses = pygame.key.get_pressed()
    if (keyPresses[K_RIGHT]):
        xPos = min(xPos + 1, WINDOW_WIDTH)
    if (keyPresses[K_LEFT]):
        xPos = max(xPos - 1, 0)
    if (keyPresses[K_UP]):
        yPos = min(yPos - 1, WINDOW_HEIGHT)
    if (keyPresses[K_DOWN]):
        yPos = max(yPos + 1, 0)    
    
    # Processing
    rect = pygame.Rect(xPos, yPos, 10, 10)
 
    # Render elements of the game
    WINDOW.fill(BACKGROUND)
    pygame.draw.rect(WINDOW, (255, 0, 0), rect)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
