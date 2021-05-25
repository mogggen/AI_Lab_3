import enums
import pathfinding
import time
import karta from main

trees = []

r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)

class BaseState:
    def Enter(self, agent):
        pass

    def Execute(self, agent):
        pass

    def Exit(self, agent):
        pass


class IdleState(BaseState):
    def Enter(self, agent):
        agent.goalPos = trees.pop()
        agent.changeState(MoveState)


class MoveState(BaseState):
    def Enter(self, agent):
        agent.pathToGoal = pathfinding.getAstarPath(agent)[:-1]

    def Execute(self, agent):
        agent.move()


class ChoppingState(BaseState):
    def Enter(self, agent):
        agent.startTime = time.time() + 30

    def Execute(self, agent):
        if time.time() >= agent.timer:
            agent.holding = enums.ItemEnum.tree
            # don't carry it for now
            agent.changeState(MoveState)


class ExploreState(BaseState):
    def Enter(self, agent):
        pass

    def Execute(self, agent):
        for n in r:
            if main.karta[agent.pos[0] + n[0], agent.pos[1] + n[1]][0] == 'T':
                main.trees.append(main.karta[agent.pos[0] + n[0], agent.pos[1] + n[1]])

        agent.pathToGoal = pathfinding.getAstarPath(agent)