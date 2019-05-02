import random
import Path

class TSNFlow():
    id = 0
    source = 0
    destniation = 0
    flowMaxDelay = 0
    candidatePathCounter = 0
    path = []



    def __init__(self,id, source, destniation):
        self.id = id
        self.source = source
        self.destniation = destniation
        self.flowMaxDelay = random.randint(100,1500)