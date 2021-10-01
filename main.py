import enums
import pathfinding
from enums import AgentEnum, ItemEnum
import terrain
import color
import pygame
from time import time

r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Land:
	def __init__(self, terrain_enum, trees=0):
		self.terrain = terrain_enum
		self.trees = trees


class Agent:
	def __init__(self, pos):
		self.pos = pos
		self.pathToGoal = []
		
		self.agentType = AgentEnum.WORKER
		self.timer = 0
		self.holding = ItemEnum.none


lands = {}
discovered = {}

treeTiles = []
millTiles = []

karta = terrain.init_map()
startingPoint = terrain.place_agents(discovered)
agents = []
for _ in range(50):
	agents.append(Agent(startingPoint[:]))

terr = 'V', 'B', 'G', 'M', 'T'

for L in karta:
	lands[L] = Land(karta[L][0])
	if karta[L][0].upper() == terr[-1]:
		lands[L].terrain = terr[-2]
		lands[L].trees = 5

s = 10


# destination
def draw_players(p):
	for i in p:
		x, y = i.pos[0] * s + s // 2, i.pos[1] * s + s // 2
		
		# what type of agent should be rendered
		if i.agentType == enums.AgentEnum.WORKER:
			c = color.agentColor[0]
		elif i.agentType == enums.AgentEnum.SCOUT:
			c = color.agentColor[1]
		elif i.agentType == enums.AgentEnum.BUILDER:
			c = color.agentColor[2]
		elif i.agentType == enums.AgentEnum.MILLER:
			c = color.agentColor[3]
		else:
			raise NotImplementedError
		square = pygame.Rect(x, y, 4, 4)
		pygame.draw.rect(screen, c, square, 1)
		screen.fill(c, square)


def rect(p):
	for i in p:
		if i[2].islower():
			continue
		x = i[0] * s
		y = i[1] * s
		c = i[2].upper()
		square = pygame.Rect(x, y, s, s)
		pygame.draw.rect(screen, color.terrainColor[c], square, 1)  # draw it here
		screen.fill(color.terrainColor[c], square)


def draw_trees(pos, amount):
	if amount <= 0:
		return
	rect([pos + (karta[pos][0],)])
	
	loc = [29, 43, 75, 54, 31]
	for T in loc[:amount]:
		square = pygame.Rect(pos[0] * 10 + T // 10, pos[1] * 10 + T % 10, 3, 3)
		pygame.draw.rect(screen, color.terrainColor['W'], square, 1)
		screen.fill(color.terrainColor['W'], square)


def find_trees(land):
	global karta
	
	for g in karta:
		if karta[g][0] == 'T':
			land.trees = 5
		draw_trees(g, land.trees)


def update_map():
	global discovered
	global agents
	
	for g in karta:
		if karta[g][0].isupper():
			discovered[g] = karta[g]
			
			if lands[g].trees > 0 and g not in treeTiles and g != startingPoint:  # xd
				treeTiles.append(g)
			elif g in treeTiles:
				treeTiles.remove(g)
			
			rect([g + (karta[g][0],)])
			draw_trees(g, lands[g].trees)
	
	draw_players(agents)
	
	pygame.display.flip()


def graph_to_nodes(goal, current_agent_enum):
	nodelist = {}
	if current_agent_enum == AgentEnum.SCOUT:
		for g in karta:
			if karta[g][0].upper() in ('T', 'G', 'M'):
				nodelist[g] = pathfinding.Node(int((((g[0] - goal[0]) ** 2 + (g[1] - goal[1]) ** 2) ** .5) * 10), karta[g][1:])
	
	else:
		for g in discovered:
			if karta[g][0] in ('T', 'G', 'M'):
				walk = []
				for n in karta[g][1:]:
					if n in discovered:
						walk.append(n)
				nodelist[g] = pathfinding.Node(int((((g[0] - goal[0]) ** 2 + (g[1] - goal[1]) ** 2) ** .5) * 10), walk)
	
	return nodelist


# game loop
def ai_lab_3(without_traversing_delays=True):
	baseTrees = 0
	charCoal = 0
	
	while charCoal < 200:
		workers = 0
		scouts = 0
		craftsmen = 0
		for a in agents:
			if a.agentType == AgentEnum.WORKER: workers += 1
			if a.agentType == AgentEnum.SCOUT: scouts += 1
			if a.agentType == AgentEnum.BUILDER: craftsmen += 1
			
			if without_traversing_delays or time() > a.timer:
				if a.agentType == AgentEnum.WORKER:
					if scouts < 3:
						a.timer = time() + 60
						a.agentType = AgentEnum.SCOUT
						scouts += 1
						continue
					elif craftsmen < 1:
						a.timer = time() + 120
						a.agentType = AgentEnum.BUILDER
						craftsmen += 1
						continue

					if lands[a.pos].trees > 0 and a.holding != ItemEnum.tree:
						lands[a.pos].trees -= 1
						a.holding = ItemEnum.tree
						a.timer = time() + 30
						a.pathToGoal = []
						
					# something with pos, g, h
					if a.pathToGoal:
						a.timer = time() + pathfinding.move_cost(a.pos, a.pathToGoal[-1])
						a.pos = a.pathToGoal.pop()
					
					# move to goal
					elif a.pos == startingPoint and len(treeTiles):
						if a.holding == ItemEnum.tree:
							baseTrees += 1
							print("Trees In inventory:", baseTrees)
							a.holding = ItemEnum.none
						to_traverse = graph_to_nodes(treeTiles[0], a.agentType)
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos)
					
					# return to starting point
					else:
						lands[a.pos].trees -= 1
						a.holding = ItemEnum.tree
						a.timer = time() + 30
						
						to_traverse = graph_to_nodes(startingPoint, a.agentType)
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos)
				
				if a.agentType == AgentEnum.SCOUT:
					
					# something with pos, g, h
					if a.pathToGoal:
						a.timer = time() + pathfinding.move_cost(a.pos, a.pathToGoal[0])
						a.pos = a.pathToGoal.pop()
					
					# move to goal
					elif a.pos == startingPoint:
						rng_undiscovered = terrain.find_scout_goal()
						
						to_traverse = graph_to_nodes(rng_undiscovered, a.agentType)
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos)
					
					# return to starting point
					else:
						to_traverse = graph_to_nodes(startingPoint, a.agentType)
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos)
					
					for n in r + ((0, 0),):
						neigh = a.pos[0] + n[0], a.pos[1] + n[1]
						karta[neigh][0] = (karta[neigh][0]).upper()
						discovered[neigh] = karta[neigh]
				
				if a.agentType == AgentEnum.BUILDER:
					
					# Build a coalMill if there is none
					if karta[a.pos][0] == 'M' and baseTrees >= 10 and a.pos not in millTiles:
						baseTrees -= 10
						millTiles.append(a.pos)
						a.timer = time() + 60
					
					# if the miller is standing in the millTiles and has enough resources to smelt
					if a.pos in millTiles and baseTrees >= 2:
						baseTrees -= 2
						charCoal += 1
						print("charCoal:", charCoal)
						a.timer = time() + 30
					
					#
					if len(a.pathToGoal) > 0:
						a.timer = time() + pathfinding.move_cost(a.pos, a.pathToGoal[-1])
						a.pos = a.pathToGoal.pop()
					
					elif a.pos not in millTiles and len(millTiles) > 0:
						builder_goal = terrain.find_builder_goal()
						to_traverse = graph_to_nodes(builder_goal, AgentEnum.BUILDER)
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos)
		
		update_map()


ai_lab_3()
