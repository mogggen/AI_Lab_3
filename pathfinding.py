from time import time


class Node:
    def __init__(self, h=None, neighbours=None):
        self.g = None
        self.h = h
        self.neighbours = neighbours
        self.parent = None


def convertGraphToNodes(graph):
    if not graph:
        return
    finish = None
    node_list = {}
    for g in graph:
        if graph[g][0] == 'G':
            finish = g
            break

    for g in graph:
        node_list[g] = Node(round((((finish[0] - g[0]) ** 2 + (finish[1] - g[1]) ** 2) ** .5) * 10), graph[g][1:])
        if graph[g][0] == 'S':
            node_list[g].g = 0

    return node_list


def moveCost(parent, child):
    return 14 if ((parent[0] - child[0]) + (parent[1] - child[1])) % 2 == 0 else 10


def aStar(graph, outOfTime, open_list=[], closed_list=[]):
    node = 1, 1

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
