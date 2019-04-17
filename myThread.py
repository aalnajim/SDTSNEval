import threading
import Path
import networkx as nx
from itertools import islice

exitFlag = 0

class myThread (threading.Thread):
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

            for index in range(self.sta+1, len(self.hostList)):

                d = self.hostList[index]
                paths = []
                paths2 = []
                if (s.id == d.id):
                    continue
                if (s.accessPoint == d.accessPoint):
                    tempNodes = [s, s.accessPoint,
                                 d]  ############################################################################
                    tempNodes2 = [d, d.accessPoint,s]
                    tempDelay = s.transmissonDelay + s.processingDelay + self.G.nodes[s.accessPoint][
                        'transmissionDelay'] + d.processingDelay
                    tempDelay2 = d.transmissonDelay + d.processingDelay + self.G.nodes[d.accessPoint][
                        'transmissionDelay'] + s.processingDelay
                    tempPath = Path.Path(tempNodes, tempDelay)
                    tempPath2 = Path.Path(tempNodes2,tempDelay2)
                    paths.append(tempPath)
                    paths2.append(tempPath2)
                    self.allPaths[s.id, d.id] = paths
                    self.allPaths[d.id, s.id] = paths2
                    continue
                else:
                    tempList = list(islice(nx.shortest_simple_paths(self.G, s.accessPoint, d.accessPoint, weight='processingDelay'), self.k))
                    for path in tempList:
                        if (len(path) < 8):
                            path2 = path.copy()
                            path2.reverse()

                            tempNodes = [
                                s]  ############################################################################
                            tempNodes2 = [d]
                            tempDelay = s.transmissonDelay + s.processingDelay
                            tempDelay2 = d.transmissonDelay + d.processingDelay
                            i = 1
                            for n in range(len(path)):
                                tempNodes.append(list(path).__getitem__(n))
                                tempNodes2.append(list(path2).__getitem__(n))
                                tempDelay = tempDelay + self.G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                                tempDelay2 = tempDelay2 + self.G.nodes[list(path2).__getitem__(n)]['transmissionDelay']
                                if (i < len(path)):
                                    tempDelay = tempDelay + self.G[list(path).__getitem__(n)][list(path).__getitem__(n + 1)][
                                        'processingDelay'] - self.G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                                    tempDelay2 = tempDelay2 + \
                                                self.G[list(path2).__getitem__(n)][list(path2).__getitem__(n + 1)][
                                                    'processingDelay'] - self.G.nodes[list(path2).__getitem__(n)]['transmissionDelay']
                                i = i + 1
                            tempNodes.append(
                                d)  ############################################################################
                            tempNodes2.append(
                                s)
                            tempDelay = tempDelay + d.processingDelay
                            tempDelay2 = tempDelay2 + s.processingDelay
                            tempPath = Path.Path(tempNodes, tempDelay)
                            tempPath2 = Path.Path(tempNodes2, tempDelay2)
                            paths.append(tempPath)
                            paths2.append(tempPath2)
                            self.allPaths[s.id, d.id] = paths
                            self.allPaths[d.id, s.id] = paths2

            startpoint = startpoint + 1