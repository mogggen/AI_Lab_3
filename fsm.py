import pathfinding


class BaseState:
    def Enter(self, agent):
        pass

    def Execute(self, agent):
        pass


class MoveState(BaseState):
    def Enter(self, agent):
        agent.pathToGoal = pathfinding.getAstarPath(agent)

    def Execute(self, agent):
        agent.move()
