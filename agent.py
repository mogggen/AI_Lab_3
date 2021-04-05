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

