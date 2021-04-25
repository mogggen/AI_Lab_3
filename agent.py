import fsm
import enums

agents = []


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.goal = enums.GoalEnum.CHOPPING_GOAL
        self.pathToGoal = []
        self.goalPos = -1, -1

        self.agentType = enums.AgentEnum.WORKER
        self.state = self.ChangeState(fsm.BaseState())
        self.startTime = 0
        self.holding = enums.ItemEnum.none

    def ChangeState(self, newState):
        self.state = newState
        self.state.Enter(self)

for i in range(9):
    n = p.X - 1 + i % 3, p.Y - 1 + i / 3 # p is agent
    if i == 4:
        if karta[n.X, n.Y].land.BackColor == closed: # if the child node is in the openlist
            continue
        else:
            karta[n.X, n.Y].land.BackColor = open # append to openlist
            step = 14 if ((p.X - n.X + (p.Y - n.Y)) % 2 == 0) else 10 # straight or diagonal step
            if karta[p.X, p.Y].gCost + step < karta[n.X, n.Y].gCost or karta[n.X, n.Y].gCost == 0: # is better or is not the starting node
                karta[n.X, n.Y].gCost = karta[p.X, p.Y].gCost + step # new improved gCost
                karta[n.X, n.Y].parent = b # new parent position

            #prints the gCost
            karta[n.X, n.Y].fCost = karta[n.X, n.Y].gCost + karta[n.X, n.Y].hCost
