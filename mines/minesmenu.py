import pygame
import pygame.freetype as fonts

class Button:
	def __init__(self, text, action=None):
		self.font = None

		self.size_w = 200
		self.size_h = 60
		self.size_t = 40

		self.text = text
		if action is None:
			self.action = text
		else:
			self.action = action

	def get_action(self):
		return self.action

	def draw(self):
		if self.font is None:
			self.font = fonts.SysFont('Courier New', self.size_t, True)

		# Create surface
		surf = pygame.Surface((self.size_w,self.size_h))
		# Fill Surface
		surf.fill((255,255,255))
		# Draw Text
		t_surf, t_rect = self.font.render(self.text, (0,0,0))
		y = self.size_h / 2 - t_rect[3] / 2
		x = self.size_w / 2 - t_rect[2] / 2
		surf.blit(t_surf, (x, y))

		return surf

class GameMenu:
	def __init__(self, screen, clock):
		self.screen = screen
		self.clock = clock

		self.running = True

		self.action = None

	# Perform an action from the menu
	def do(self, action):
		self.action = action
		self.running = False

	def run(self):
		options = []
		options.append(Button("Easy"))
		options.append(Button("Medium"))
		options.append(Button("Hard"))
		options.append(Button("Expert"))
		options.append(Button("Quit"))

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: return None
				if event.type == pygame.MOUSEBUTTONDOWN:
					x = event.pos[0]
					y = event.pos[1]

					# Button dimensions
					bw = 200
					bh = 60

					for b, button in enumerate(options):

						# Button position
						bx = 20
						by = 20 + 80*b
						
						# Determine if cursor in button
						if x > bx and x < bx+bw \
						and y > by and y < by+bh:
							self.do(button.get_action())


			# Clear the screen
			self.screen.fill((0,0,0))
			# Draw all the buttons
			for b, button in enumerate(options):
				x = 20
				y = 20 + 80*b
				b_surf = button.draw()
				self.screen.blit(b_surf,(x,y))
			# Flip the screen
			pygame.display.flip()
			# Wait a little
			self.clock.tick(60) 

		return self.action

