import enums
import fsm


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.sub = 4, 4
        self.pathToGoal = []
        self.goalPos = -1, -1

        self.agentType = enums.AgentEnum.WORKER
        self.state = fsm.BaseState()
        self.timer = 0
        self.holding = enums.ItemEnum.none

    def changeState(self, newState):
        self.state.Exit(self)
        self.state = newState
        self.state.Enter(self, newState)

    # move from center to center # runs every execute
    def move(self):
        self.pathToGoal[-1]
        # you have arrived at the neighbouring tile
        if self.pos == self.pathToGoal[0] and self.sub == (4, 4):

            self.pathToGoal.pop(0)

            if not len(self.pathToGoal):
                return
            # find tree
            # changeState ... (MoveToHQ)
            return
        
        self.sub = self.pathToGoal[0][0] - self.pos[0], self.pathToGoal[0][1] - self.pos[0]
        # is diagonal move
        self.timer = karta[self.pos]

        
        
