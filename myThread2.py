import threading
import Path
import networkx as nx
from itertools import islice

exitFlag = 0

class myThread2 (threading.Thread):
    sta = -1
    end = -1
    G = nx.erdos_renyi_graph(3,0.4)
    hostsList = []
    k = -1
    allPaths = {}
    def __init__(self,allPaths,G,hostsList,k,s,e):
        threading.Thread.__init__(self)
        self.allPaths = allPaths
        self.G = G
        self.hostList = hostsList
        self.k = k
        self.sta = s
        self.end = e

    def run(self):
        startpoint = self.sta
        while(startpoint<self.end):
            #print(self.getName())
            s = self.hostList[startpoint]

            # self.l[n]= n
            for d in self.hostList:
                paths = []
                if (s.id == d.id):
                    continue
                if (s.accessPoint == d.accessPoint):
                    tempNodes = [s, s.accessPoint,
                                 d]  ############################################################################
                    tempDelay = s.transmissonDelay + s.processingDelay + self.G.nodes[s.accessPoint][
                        'transmissionDelay'] + d.processingDelay
                    tempPath = Path.Path(tempNodes, tempDelay)
                    paths.append(tempPath)
                    self.allPaths[s.id, d.id] = paths
                    continue
                else:
                    tempList = list(islice(nx.shortest_simple_paths(self.G, s.accessPoint, d.accessPoint, weight='processingDelay'), self.k))
                    for path in tempList:
                        if (len(path) < 8):
                            tempNodes = [
                                s]  ############################################################################
                            tempDelay = s.transmissonDelay + s.processingDelay
                            i = 1
                            for n in range(len(path)):
                                tempNodes.append(list(path).__getitem__(n))
                                tempDelay = tempDelay + self.G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                                if (i < len(path)):
                                    tempDelay = tempDelay + self.G[list(path).__getitem__(n)][list(path).__getitem__(n + 1)][
                                        'processingDelay']
                                i = i + 1
                            tempNodes.append(
                                d)  ############################################################################
                            tempDelay = tempDelay + d.processingDelay
                            tempPath = Path.Path(tempNodes, tempDelay)
                            paths.append(tempPath)
                            self.allPaths[s.id, d.id] = paths

            startpoint = startpoint + 1