import random
import fsm
import pathfinding
import goal

agents = ()


class AgentEnum:
    WORKER = 1
    SCOUT = 2
    BUILDER = 3
    MILLER = 4


class ItemEnum:
    none = 0
    tree = 1
    charcoal = 2


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.goal = GoalEnum.CHOPPING_GOAL
        self.goalPos = -1, -1

        self.agentType = AgentEnum.WORKER
        self.state = fsm.Change(self)
        self.holding = ItemEnum.none

    def ChangeState(self, newState):
        self.state.Exit(self)
        self.state = newState
        self.state.Enter(self)

