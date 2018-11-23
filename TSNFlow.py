import random
import Path

class TSNFlow():
    path = []
    flowMaxDelay = 0
    id = 0

    def __init__(self,id):

        self.flowMaxDelay = random.randint(900,1500)
        self.id = id