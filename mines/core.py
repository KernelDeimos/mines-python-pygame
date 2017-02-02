import sys, pygame
import random
import game
import minesmenu

class Application:
	def main(self):
		pygame.init()
		self.resolution = 1280, 1024

		rec = pygame.Rect(100,100,40,40)
		speed = [2,2]

		width = self.resolution[0]
		height = self.resolution[1]

		clock = pygame.time.Clock()

		while 1:

			menu = minesmenu.GameMenu(clock)
			action = menu.run()
			
			if action == "Quit":
				return

			difficulty = None
			if action == "Easy":
				difficulty = game.GameInstanceBuilder.DIFFICULTY_EASY
			elif action == "Medium":
				difficulty = game.GameInstanceBuilder.DIFFICULTY_MEDIUM
			elif action == "Hard":
				difficulty = game.GameInstanceBuilder.DIFFICULTY_HARD
			elif action == "Expert":
				difficulty = game.GameInstanceBuilder.DIFFICULTY_EXPERT

			builder = game.GameInstanceBuilder(random, clock)
			gameInstance = builder.make_instance(difficulty)
			gameInstance.run()

if __name__ == '__main__':
	app = Application()
	app.main()
