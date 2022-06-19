import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (0, 0, 0)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sprite Test')

 
# The main function that controls the game
def main () :
  looping = True
  
  sprites = pygame.image.load("sprites.png").convert_alpha()
  
  startX = 0
  startY = 150
  cropX = 0
  cropY = 60
  cropWidth = 240
  cropHeight = 60
  
  # The main game loop
  while looping :
    # TODO: Blit different sprite on spacebar
    

 
    # Render elements of the game
    WINDOW.fill(BACKGROUND)
    WINDOW.blit(sprites, (startX, startY), (cropX, cropY, cropWidth, cropHeight))
    # pygame.draw.rect(WINDOW, (255, 0, 0), rect)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
