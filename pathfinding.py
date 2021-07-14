class Node:
	def __init__(self, h=None, neighbours=None):
		self.g = None  # int
		self.h = h  # int
		self.neighbours = neighbours  # list(point((int, int)))
		self.parent = None  # (point(int, int))


def move_cost(parent, child):
	return 14 if ((parent[0] - child[0]) + (parent[1] - child[1])) % 2 == 0 else 10


def a_star(graph, start):
	closed_list = []
	open_list = []
	node = start
	graph[node].g = 0
	open_list.append(node)
	
	while open_list:
		
		# return final path
		if graph[node].h == 0:
			path = [node]
			while graph[node].parent:
				path.append(graph[node].parent)
				node = graph[node].parent
			return path
		
		node = min(open_list, key=lambda x: graph[x].g + graph[x].h)
		
		open_list.remove(node)
		
		closed_list.append(node)
		
		for n in graph[node].neighbours:
			if n in closed_list:
				continue
			
			if n not in open_list:
				graph[n].g = graph[node].g + move_cost(node, n)
				graph[n].parent = node
				open_list.append(n)
			
			elif graph[node].g + move_cost(node, n) < graph[n].g:
				graph[n].g = graph[node].g + move_cost(node, n)
				graph[n].parent = node
