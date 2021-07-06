import random

import enums
import pathfinding
from enums import AgentEnum, ItemEnum
import terrain
import color
import pygame
from time import time

r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)

charCoal = 0

# workers = []  # the rest
# explorers = []  # 3
# craftsmen = []  # 1 total

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Land:
	def __init__(self, terrain_enum, trees=0):
		self.terrain = terrain_enum
		self.trees = trees  # yields 1 tree after 30 seconds


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
karta = terrain.init_map()
startingPoint = terrain.place_agents(discovered)
agents = []
for a in range(1):
	agents.append(Agent(startingPoint[:]))

terr = 'V', 'B', 'G', 'M', 'T'
buildings = 'C',  # placed on 'M'

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
		square = pygame.Rect(x, y, 2, 2)
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


def draw_connections():
	xy = 0, 0
	while xy[0] < 100 and xy[1] < 100:
		for g in karta[xy][1:]:
			new_c = color.terrainColor[(karta[g[:2]][0]).upper()]
			pygame.draw.aaline(screen, new_c, (xy[0] * s + s / 2, xy[1] * s + s / 2),
			                   (g[0] * s + s / 2, g[1] * s + s / 2), 1)
		xy = (xy[0] + 1, xy[1]) if xy[0] != 99 else (0, xy[1] + 1)


def draw_trees(pos: tuple[int, int], amount: int):
	if amount <= 0:
		return
	rect([pos + (karta[pos][0],)])
	
	loc = [29, 43, 75, 54, 31]
	for T in loc[:amount]:
		square = pygame.Rect(pos[0] * 10 + T // 10, pos[1] * 10 + T % 10, 2, 2)
		pygame.draw.rect(screen, color.terrainColor['G'], square, 1)
		screen.fill(color.terrainColor['G'], square)


def find_trees(land):
	global karta
	
	for g in karta:
		if karta[g][0] == 'T':  # FIXME should be uppercase so only the discovered treeTiles draw trees
			land.trees = 5
		draw_trees(g, land.trees)


def update_map():
	global discovered
	global agents
	
	# for i in lands:
	#	draw_trees(i, lands[i].trees)
	
	# find trees
	for g in karta:
		if karta[g][0].isupper():
			discovered[g] = karta[g][0]
			if lands[g].trees:
				treeTiles.append(g)  # = lands[g].trees
			rect([g + (karta[g][0],)])
			draw_trees(g, lands[g].trees)
	
	draw_players(agents)
	
	# draw_connections()
	
	pygame.display.flip()


previousDeltaCalculationTime = 0
shortestTimeRemaining = time()


# nodesToTraverse = pathfinding.convertLandToNodes(lands)


def graph_to_nodes(goal, information, graph=karta):
	nodelist = {}
	for g in graph:
		if information == AgentEnum.SCOUT and graph[g][0].upper() in ('T', 'G', 'M') or graph[g][0] in ('T', 'G', 'M'):
			tmp = []
			for o in graph[g][1:]:
				tmp.append(o[:2])
			nodelist[g] = pathfinding.Node(int((((g[0] - goal[0]) ** 2 + (g[1] - goal[1]) ** 2) ** .5) * 10), tmp)
	return nodelist


# game loop
while charCoal < 200:
	for a in agents:
		if (a.agentType in (AgentEnum.SCOUT, AgentEnum.WORKER)) and a.timer < shortestTimeRemaining:
			shortestTimeRemaining = a.timer
	# shortestTimeRemaining = min(agents, key=lambda t: t.timer).timer
	workers = 0
	scouts = 0
	craftsmen = 0
	millers = 0
	for a in agents:
		if a.agentType == AgentEnum.WORKER:
			workers += 1
		if a.agentType == AgentEnum.SCOUT:
			scouts += 1
		if a.agentType == AgentEnum.BUILDER:
			craftsmen += 1
		if a.agentType == AgentEnum.MILLER:
			millers += 1
		
		if time() > a.timer:
			if a.agentType == AgentEnum.WORKER:
				if scouts < 3:
					a.timer = time() + 60
					a.agentType = AgentEnum.SCOUT
					scouts += 1
				elif craftsmen < 1:
					a.timer = time() + 120
					a.agentType = AgentEnum.BUILDER
					craftsmen += 1
				elif millers < 1:
					a.timer = time() + 120
					a.agentType = AgentEnum.MILLER
					millers += 1
				
				if a.pathToGoal:
					a.timer = pathfinding.move_cost(a.pos, a.pathToGoal[0]) * \
					          (1 + bool((karta[a.pos][0]).upper() == (terrain.walkables[0]).upper()))
					a.pos = a.pathToGoal.pop(0)
				
				# find a new path
				else:
					# check if the workers have already reached the goal
					if karta[a.pos][0].upper() == 'T' and a.holding != ItemEnum.none:
						lands[a.pos].trees -= 1
						draw_trees(a.pos, lands[a.pos].trees)
						a.holding = ItemEnum.tree
						a.timer = time() + 30
						
						to_traverse = graph_to_nodes(startingPoint[:], AgentEnum.WORKER, discovered)
						saved_time = time() + 100
						a.pathToGoal = pathfinding.a_star(to_traverse, a.pos, saved_time)
					else:
						for train in treeTiles:
							if lands[train].trees > 0:  # all we had todo was to followed the damn train CJ
								to_traverse = graph_to_nodes(train, AgentEnum.WORKER, discovered)
								saved_time = time() + 100
								a.pathToGoal = pathfinding.a_star(to_traverse, a.pos, saved_time)
							else:
								# dispose of empty tree tiles from the list
								treeTiles.pop(0)
								break
			if a.agentType == AgentEnum.SCOUT:
				
				# something with pos, g, h
				if a.pathToGoal:
					a.timer = pathfinding.move_cost(a.pos, a.pathToGoal[0])
					a.pos = a.pathToGoal.pop(0)
				else:
					# TODO perform conversion here
					rng_undiscovered = terrain.find_scout_goal()
					
					to_traverse = graph_to_nodes(rng_undiscovered, a.agentType)
					saved_time = time() + 100
					a.pathToGoal = pathfinding.a_star(to_traverse, a.pos, saved_time)
					print(rng_undiscovered)
					print(int(a.timer), a.pathToGoal)
				
				for n in r + ((0, 0),):
					neigh = a.pos[0] + n[0], a.pos[1] + n[1]
					karta[neigh][0] = (karta[neigh][0]).upper()
					discovered[neigh] = [lands[neigh].terrain, lands[neigh].trees]
			
			if a.agentType == AgentEnum.BUILDER:
				if karta[a.pos][0] == 'M' and lands[a.pos].trees >= 10:
					lands[a.pos].trees -= 10
					karta[a.pos][0] = 'K'
					a.timer = time() + 60
			
			if a.agentType == AgentEnum.MILLER:
				if karta[a.pos] == 'K' and lands[a.pos].trees >= 2:
					lands[a.pos].trees -= 2
					charCoal += 1
					a.timer = time() + 30
	
	# if int(agents[0].timer - time()) % 10 == 0:
	# print(workers, scouts, craftsmen, millers, "time: ", (int(agents[0].timer - time())) if int(agents[0].timer - time()) < shortestTimeRemaining else shortestTimeRemaining)
	# print("charCoal:", charCoal / 200, "%")
	
	update_map()
