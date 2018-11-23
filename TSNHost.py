import random


class TSNHost():
    id = 0
    transmissonDelay = 0
    processingDelay = 0
    accessPoint = 0

    def __init__(self,id,accessPoint):
        self.id = id
        self.transmissonDelay = random.randint(1,90)
        self.processingDelay = random.randint(1,2)
        self.accessPoint = accessPoint
