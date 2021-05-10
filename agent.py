import enums
import fsm


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.objective = enums.GoalEnum.CHOPPING_GOAL
        self.pathToGoal = []
        self.goalPos = -1, -1

        self.agentType = enums.AgentEnum.WORKER
        self.state = fsm.BaseState()
        self.timer = 0
        self.holding = enums.ItemEnum.none

    def changeState(self, newState):
        self.state.Exit(self)
        self.state = newState
        self.state.Enter(self)


