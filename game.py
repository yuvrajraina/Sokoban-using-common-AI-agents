import os
import pygame
from sokoban import State
from helper import readLevel
from agent import DoNothingAgent, RandomAgent, BFSAgent, DFSAgent, AStarAgent, HillClimberAgent, GeneticAgent, MCTSAgent
import argparse
import random

#show the game screen for sokoban
class GameScreen():
	def __init__(self,init_state,lvlno=1):
		self.state = init_state

		#set the sprites
		self._graphics = {
			#"empty": Image.open(os.path.dirname(__file__) + "/assets/graphics/empty.png").convert('RGBA'),
			"solid": pygame.image.load("assets/graphics/solid.png"),
			"player": pygame.image.load("assets/graphics/player.png"),
			"crate": pygame.image.load("assets/graphics/crate.png"),
			"target": pygame.image.load("assets/graphics/target.png")
		}
		self.size = 64	#allow for sprite rescaling

		#setup the game screen
		pygame.init()
		self.gameDisplay = pygame.display.set_mode((init_state.width*self.size,init_state.height*self.size))
		pygame.display.set_caption('Sokoban Lvl ' + str(lvlno))

	#show the level on a pygame window
	def render(self):
		#fill with background empty color first
		self.gameDisplay.fill(pygame.Color(89,86,82))  

		#draw sprites at their coordinates
		for y in range(self.state.height):
			for x in range(self.state.width):
				img = ''
				img2 = ''

				if self.state.solid[y][x]:											#draw wall
					img = 'solid'
				elif self.state._checkTargetLocation(x,y) is not None:				#draw target
					img = 'target'

				if self.state.player["x"] == x and self.state.player["y"] == y:		#draw player
					img2 = 'player'
				elif self.state._checkCrateLocation(x,y) is not None:				#draw crate
					img2 = 'crate'

				#draw the images (resized accordingly)
				if img != '':
					self.gameDisplay.blit(pygame.transform.scale(self._graphics[img], (self.size,self.size)),(x*self.size,y*self.size))
				if img2 != '':
					self.gameDisplay.blit(pygame.transform.scale(self._graphics[img2], (self.size,self.size)),(x*self.size,y*self.size))


		pygame.display.update()

# allow human to play the sokoban level
#  arrow keys - move player
#  R - reset level
def human_play(lvlNumber):
	state = readLevel(lvlNumber)
	screen = GameScreen(state, lvlNumber)

	#while the game is still being played
	solved = False
	status = '--GAME WON--'
	tot_steps = 0
	while not solved:
		for event in pygame.event.get():
			#exit button at top of window
			if event.type == pygame.QUIT:
				solved = True
				status = '--GAME ENDED BY USER--'

			#keyboard press
			elif event.type == pygame.KEYDOWN:
				#rrow keys to update state
				if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
					x = 0
					y = 0
					if event.key == pygame.K_LEFT:
						x = -1
					elif event.key == pygame.K_RIGHT:
						x = 1
					elif event.key == pygame.K_UP:
						y = -1
					elif event.key == pygame.K_DOWN:
						y = 1


					screen.state.update(x, y)

					tot_steps+=1

					#check if the game has been solved
					solved = screen.state.checkWin()

				#reset the game
				elif event.key == pygame.K_r:
					state = readLevel(lvlNumber)
					screen = GameScreen(state, lvlNumber)
					tot_steps = 0


		screen.render()

	#game is finished
	if(status == '--GAME WON--'):
		print("--GAME WON IN [ " + str(tot_steps) + " ] MOVES--")
	else:
		print(status)
	pygame.quit()
	quit()

#have bot solve the game
def ai_play(lvlNumber, bot, maxIter, delayTime=2000, no_render=False):
	render_game = False if no_render else True

	state = readLevel(lvlNumber)

	if render_game:
		screen = GameScreen(state, lvlNumber)
	print('> Calculating solution...')
	sol = bot.getSolution(state, maxIterations=maxIter)

	status = ''
	finish = False

	if render_game:
		print('> Demonstrating solution...')

	#rollout the steps in the solution found
	for s in sol:

		if render_game:
			#exit button at top of window
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					status = '--GAME ENDED BY USER--'
					finish = True

			if finish:
				break

			#show action results
			screen.state.update(s['x'], s['y'])
			screen.render()

			#wait a certain time
			pygame.time.delay(delayTime)

		#just update the state
		else:
			state.update(s['x'],s['y'])


		


	#get status upon finish of the game
	if status == '':
		if (render_game and screen.state.checkWin()) or (state.checkWin()):
			print('--GAME WON IN [ ' + str(len(sol)) + ' ] MOVES--')
		else:
			print('--SOLUTION NOT FOUND--')
	else:
		print(status)


	pygame.quit()
	quit()


if __name__ == '__main__':
	#establish parameters
	parser = argparse.ArgumentParser(description='PyGame wrapper for Sokoban')
	parser.add_argument('-p','--play', action='store_true', dest='play', default=False, help='Allow human play')
	parser.add_argument('-n', '--no_render', action='store_true', dest='no_rend', default=False, help='Turn off rendering the game screen when showing the AI solution')
	parser.add_argument('-l','--level', action='store', dest='levelNo', default='random', type=str, help='Which level to play (0-99) or [random] for a randomly selected level')
	parser.add_argument('-a', '--agent', action='store', dest='agent', default='Random', help='Which agent algorithm to use (DoNothing, Random, BFS, DFS, AStar, HillClimber, Genetic, MCTS)')
	parser.add_argument('-i', '--iterations', action='store', dest='maxIter', default=3000, type=int, help='Number of iterations for the agent to search a solution for')
	parser.add_argument('-s', '--solve_speed', action='store', dest='speed', default=250, type=int, help='How fast to show each step of the solution in ms')

	args = parser.parse_args()


	#check if random level
	if (args.levelNo == 'random'):
		args.levelNo = random.randint(0,99)

	args.levelNo = int(args.levelNo)

	#human solve
	if args.play or args.agent == 'Human':
		print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] AS HUMAN PLAYER--")
		print("\n** CONTROLS **")
		print("Arrow Keys\t- Move")
		print("R\t\t- Reset\n")
		human_play(args.levelNo)

	#agent solve
	else:
		if args.agent == 'DoNothing':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ DO-NOTHING AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, DoNothingAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'Random':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ RANDOM AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, RandomAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'BFS':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ BFS AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, BFSAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'DFS':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ DFS AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, DFSAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'AStar':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ ASTAR AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, AStarAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'HillClimber':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ HILLCLIMBER AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, HillClimberAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'Genetic':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ GENETIC AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, GeneticAgent(), args.maxIter, args.speed, args.no_rend)
		elif args.agent == 'MCTS':
			print("--SOLVING LEVEL [ " + str(args.levelNo) + " ] WITH [ MCTS AGENT ] for [ " + str(args.maxIter) + " ] ITERATIONS--")
			ai_play(args.levelNo, MCTSAgent(), args.maxIter, args.speed, args.no_rend)
		else:
			print("!!! UNKNOWN AGENT '" + args.agent +"' !!!\n")
			parser.print_help()



