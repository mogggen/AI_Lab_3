import agent


def getAstarPath(agent):
    if agent.type == agent.agentEnum.worker:
        # goal is always tree for worker
        findTree()
