import sys, pygame
import random
import game

class Application:
	def main(self):
		pygame.init()
		self.resolution = 600, 800

		self.screen = pygame.display.set_mode(self.resolution)

		rec = pygame.Rect(100,100,40,40)
		speed = [2,2]

		width = self.resolution[0]
		height = self.resolution[1]

		clock = pygame.time.Clock()

		builder = game.GameInstanceBuilder(random, self.screen, clock)
		gameInstance = builder.make_instance(game.GameInstanceBuilder.DIFFICULTY_EASY)

		gameInstance.run()

if __name__ == '__main__':
	app = Application()
	app.main()
