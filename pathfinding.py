from time import time


class Node:
    def __init__(self, h=None, neighbours=None):
        self.g = None
        self.h = h
        self.neighbours = neighbours
        self.parent = None


def convertLandToNodes(graph):
    if not graph:
        return
    node_list = {}

    for g in graph:
        node_list[g] = Node()

    return node_list


def moveCost(parent, child):
    return 14 if ((parent[0] - child[0]) + (parent[1] - child[1])) % 2 == 0 else 10

# shan't be called by workers if none of them are holding tree or none of them can see a tree
def aStar(graph, start, endTime):
    closed_list = []
    open_list = []
    node = start

    open_list.append(node)

    while open_list:
        node = min(open_list, key=lambda x: graph[x].g + graph[x].h)

        # return final path
        if graph[node].h == 0 or not open_list:
            path = [node]
            while graph[node].parent:
                path.append(graph[node].parent)
                node = graph[node].parent
            open_list[:] = closed_list[:] = []
            return path

        open_list.remove(node)

        closed_list.append(node)
        rect(node, "black")

        for n in graph[node].neighbours:
            if n in closed_list:
                continue

            rect(n)
            if n not in open_list:
                graph[n].g = graph[node].g + moveCost(node, n)
                graph[n].parent = node
                open_list.append(n)

            elif graph[node].g + moveCost(node, n) < graph[n].g:
                graph[n].g = graph[node].g + moveCost(node, n)
                graph[n].parent = node
