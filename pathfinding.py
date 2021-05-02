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
        # - 1 + 2 * (par == neighbour)
        for best in improved:
            astar(graph, improved[best], end, g, node)

# for i in range(9):
#     n = p.X - 1 + i % 3, p.Y - 1 + i / 3 # p is agent
#     if i == 4:
#         if karta[n.X, n.Y].land.BackColor == closed: # if the child node is in the openlist
#             continue
#         else:
#             karta[n.X, n.Y].land.BackColor = open # append to openlist
#             step = 14 if ((p.X - n.X + (p.Y - n.Y)) % 2 == 0) else 10 # straight or diagonal step
#             if karta[p.X, p.Y].gCost + step < karta[n.X, n.Y].gCost or karta[n.X, n.Y].gCost == 0: # is better or is not the starting node
#                 karta[n.X, n.Y].gCost = karta[p.X, p.Y].gCost + step # new improved gCost
#                 karta[n.X, n.Y].parent = b # new parent position
#
#             #prints the gCost
#             karta[n.X, n.Y].fCost = karta[n.X, n.Y].gCost + karta[n.X, n.Y].hCost