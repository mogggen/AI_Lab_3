import agent


def getAstarPath(agent):
    if agent.type == agent.agentEnum.worker:
        # goal is always tree for worker
        findTree()


def astar(graph, node, end, g=0, par=None):
    global Found
    if not node[0] - end[0] + node[1] - end[1]: Found = True
    if graph[node][0] == "X" or Found: return
    if draw: rect([(node[0], node[1], "T")])

    if node not in visited:
        visited.append(node)
        g + 1
        improved = {}
        for neighbour in graph[node][1:]:
            improved[g + (neighbour[0] - end[0]) ** 2 + (neighbour[1] - end[1]) ** 2] = neighbour
        ud = improved
        improved = dict(sorted(ud.items(), reverse=False))
        print(improved)
        # - 1 + 2 * (par == neighbour)
        for best in improved:
            astar(graph, improved[best], end, g, node)