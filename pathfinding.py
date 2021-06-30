from time import time


class Node:
	def __init__(self, h=None, neighbours=None):
		self.g = None  # int
		self.h = h  # int
		self.neighbours = neighbours  # list(point((int, int)))
		self.parent = None  # (point(int, int))
# points used as graph[key]


def move_cost(parent, child):
	return 14 if ((parent[0] - child[0]) + (parent[1] - child[1])) % 2 == 0 else 10


# shan't be called by workers if none of them are holding tree or none of them can see a tree
def a_star(graph, start, end, end_time):
	closed_list = []
	open_list = []
	node = start
	
	open_list.append(node)
	
	delta = time()
	while open_list:
		delta = time() - delta
		
		# return final path or if the time to compute the next edge is too long
		if graph[node].h == 0 or delta >= end_time:  # FIXME fit the node format so that the A* can operate on said graph
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
