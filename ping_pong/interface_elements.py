import pygame
import pygame.sprite as sprite
import pygame.font as font


class ScoreBoard(sprite.Sprite):
	""""The game scoreboard. It shows the user the points, every time
	the ball hits a target."""

	def __init__(self, screen):
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.points = 0
		self.font = font.SysFont("Arial", bold=True, size=12)
		self.text_format = f"POINTS: {self.points}"
		self.colour = (255, 255, 255)
		self.image = self.font.render(self.text_format, True, self.colour)
		self.rect = self.image.get_rect()

		# ScoreBoard Positioning
		self.rect.bottomleft = self.screen_rect.bottomleft

	def draw(self):
		"""Draws the scoreboard on the screen."""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Updates the score and the scoreboard everytime the user make
		points."""
		self.text_format = f"POINTS: {self.points}"
		self.image = self.font.render(self.text_format, True, self.colour)


class LifeRemaining(sprite.Sprite):
	"""A dynamic label that shows the user how many lives the paddle
	has. And it's a necessary condition to end the game when necessary.
	"""

	class LifeUnit(sprite.Sprite):
		"""A simple life unit."""

		def __init__(self, screen):
			super().__init__()
			self.screen = screen
			self.screen_rect = screen.get_rect()
			self.image = pygame.Surface((15, 15))
			self.image.fill((167, 0, 0))
			self.rect = self.image.get_rect()

		def draw(self):
			"""Draws the life unit."""

			self.screen.blit(self.image, self.rect)

	def __init__(self, screen):
		super().__init__()
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.group = []
		self.fill()

	def draw(self):
		"""Draws the remaining life on the screen."""
		padding = 2
		row = 30
		for life in self.group:
			life.rect.x = self.screen.get_width() - (row + padding)
			life.rect.y = self.screen.get_height() - (30 + padding)
			life.draw()
			row += 30

	def update(self):
		"""Updates this object image. It's responsible to get events
		like when the user loses one live.
		"""
		pass

	def poll(self):
		"""Take out one unit of life. It will self update."""
		self.group.pop(0)

	def fill(self):
		"""Fill the group with three lives."""
		for c in range(3):
			life_unit = self.LifeUnit(self.screen)
			self.group.append(life_unit)
