import pygame
import sys
from pygame.locals import *

pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400


def main():
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
				pygame.quit()

		screen.fill((68, 68, 68));
		pygame.display.update()


main()
