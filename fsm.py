import agent
class baseState:
    def Enter(self, agent):
        pass

    def Execute(self, agent):
        pass

    def Exit(self, agent):
        pass

class MoveState(baseState):
    def Enter(self, agent):
        #goto goal
    def Execute(self, agent):
        if goal is in resources
