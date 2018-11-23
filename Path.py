


class Path():
    nodes = []
    delay = 0
    TSNFlowCounter = 0
    bandwidth = 0
    hopCount = 0

    def __init__(self,nodes,delay):
        self.nodes = nodes
        self.delay = delay
