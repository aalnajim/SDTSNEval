
import random
import networkx as nx
import matplotlib.pyplot as plt
import TSNFlow
import TSNHost
import Path
import operation
import TimeSlot
import myThread
import myThread2
import math
from timeit import default_timer as timer
from itertools import islice
from TSNHost import TSNHost
from myThread import myThread
from myThread2 import myThread2




def rand(G,hosts, n):
    transmissionDelays = {}
    for i in G.nodes:
        tranmissionDelay = random.randint(1,90)
        transmissionDelays[i] = {'transmissionDelay':tranmissionDelay}

    linkMeasurments = {}
    for i in nx.edges(G,G.nodes):
        processingDelay = random.randint(1,3)
        nbOfTSN = 0
        bandwidth = 0
        linkMeasurments[i] = {'processingDelay': processingDelay, 'nbOfTSN': nbOfTSN, 'bandwidth':bandwidth}


    temp = []
    for i in G.nodes:
        temp.append(i)
    hostsList = []
    for i in range(hosts):
        linkedNode = random.choice(temp)
        id = n + i
        host = TSNHost(id,linkedNode)
        hostsList.append(host)

    return transmissionDelays,linkMeasurments, hostsList

# def findHost(hostsList, id):
#     for h in hostsList:
#         if (h.id == id):
#             return h




##############################
# this method is to calcualte the overall delay for each link based on (the link delay and the switch delays) 0 to split and 1 to combine
def convertProcDelayToComulativeDelay(G,x):
    #x has to be 0 or 1
    if (x ==0):
        for i in nx.edges(G, G.nodes):
            transmissionDelay = G.nodes[i[0]]['transmissionDelay']
            processingAndPropDelay = G[i[0]][i[1]]['processingDelay']
            G[i[0]][i[1]]['processingDelay'] = processingAndPropDelay - transmissionDelay

    elif(x==1):
        for i in nx.edges(G, G.nodes):
            transmissionDelay = G.nodes[i[0]]['transmissionDelay']
            processingAndPropDelay = G[i[0]][i[1]]['processingDelay']
            G[i[0]][i[1]]['processingDelay'] = transmissionDelay + processingAndPropDelay

    else:
        print('You have to enter 1 to combine or 0 to split')


#this method is added recently to find k shortest paths
def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


#this method is added recently to enhance K shortest path and use multithreading
# def findKthPathP(G,hostsList,k): speed
#     allPaths = {}  # all the paths between all the hosts
#
#     # Create new threads
#     thread1 = myThread(allPaths, G,hostsList,k, (0 * math.floor(len(hostsList) / 10)), ((1 * math.floor(len(hostsList) / 10))))
#     thread2 = myThread(allPaths, G,hostsList,k, (1 * math.floor(len(hostsList) / 10)), (2 * math.floor(len(hostsList) / 10)))
#     thread3 = myThread(allPaths, G,hostsList,k, (2 * math.floor(len(hostsList) / 10)), (3 * math.floor(len(hostsList) / 10)))
#     thread4 = myThread(allPaths, G,hostsList,k, (3 * math.floor(len(hostsList) / 10)), (4 * math.floor(len(hostsList) / 10)))
#     thread5 = myThread(allPaths, G,hostsList,k, (4 * math.floor(len(hostsList) / 10)), (5 * math.floor(len(hostsList) / 10)))
#     thread6 = myThread(allPaths, G,hostsList,k, (5 * math.floor(len(hostsList) / 10)), (6 * math.floor(len(hostsList) / 10)))
#     thread7 = myThread(allPaths, G,hostsList,k, (6 * math.floor(len(hostsList) / 10)), (7 * math.floor(len(hostsList) / 10)))
#     thread8 = myThread(allPaths, G,hostsList,k, (7 * math.floor(len(hostsList) / 10)), (8 * math.floor(len(hostsList) / 10)))
#     thread9 = myThread(allPaths, G,hostsList,k, (8 * math.floor(len(hostsList) / 10)), (9 * math.floor(len(hostsList) / 10)))
#     thread10 = myThread(allPaths, G,hostsList,k, (9 * math.floor(len(hostsList) / 10)), ((10 * math.floor(len(hostsList) / 10)) + len(hostsList) % 10))
#
#     # Start new Threads
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread4.start()
#     thread5.start()
#     thread6.start()
#     thread7.start()
#     thread8.start()
#     thread9.start()
#     thread10.start()
#
#     # join new Threads
#     thread1.join()
#     thread2.join()
#     thread3.join()
#     thread4.join()
#     thread5.join()
#     thread6.join()
#     thread7.join()
#     thread8.join()
#     thread9.join()
#     thread10.join()
#
#     print("done!")
#     return allPaths


#this method is added recently to enhance K shortest path and use multithreading
# def findKthPathP2(G,hostsList,k): speed
#     allPaths = {}  # all the paths between all the hosts
#
#     # Create new threads
#     thread1 = myThread2(allPaths, G,hostsList,k, (0 * math.floor(len(hostsList) / 10)), ((1 * math.floor(len(hostsList) / 10))))
#     thread2 = myThread2(allPaths, G,hostsList,k, (1 * math.floor(len(hostsList) / 10)), (2 * math.floor(len(hostsList) / 10)))
#     thread3 = myThread2(allPaths, G,hostsList,k, (2 * math.floor(len(hostsList) / 10)), (3 * math.floor(len(hostsList) / 10)))
#     thread4 = myThread2(allPaths, G,hostsList,k, (3 * math.floor(len(hostsList) / 10)), (4 * math.floor(len(hostsList) / 10)))
#     thread5 = myThread2(allPaths, G,hostsList,k, (4 * math.floor(len(hostsList) / 10)), (5 * math.floor(len(hostsList) / 10)))
#     thread6 = myThread2(allPaths, G,hostsList,k, (5 * math.floor(len(hostsList) / 10)), (6 * math.floor(len(hostsList) / 10)))
#     thread7 = myThread2(allPaths, G,hostsList,k, (6 * math.floor(len(hostsList) / 10)), (7 * math.floor(len(hostsList) / 10)))
#     thread8 = myThread2(allPaths, G,hostsList,k, (7 * math.floor(len(hostsList) / 10)), (8 * math.floor(len(hostsList) / 10)))
#     thread9 = myThread2(allPaths, G,hostsList,k, (8 * math.floor(len(hostsList) / 10)), (9 * math.floor(len(hostsList) / 10)))
#     thread10 = myThread2(allPaths, G,hostsList,k, (9 * math.floor(len(hostsList) / 10)), ((10 * math.floor(len(hostsList) / 10)) + len(hostsList) % 10))
#
#     # Start new Threads
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread4.start()
#     thread5.start()
#     thread6.start()
#     thread7.start()
#     thread8.start()
#     thread9.start()
#     thread10.start()
#
#     # join new Threads
#     thread1.join()
#     thread2.join()
#     thread3.join()
#     thread4.join()
#     thread5.join()
#     thread6.join()
#     thread7.join()
#     thread8.join()
#     thread9.join()
#     thread10.join()
#
#     print("done!")
#     return allPaths

##############################



#def findAllPath(G,hostsList):
def findKthPath(G,hostsList,k):
    allPaths = {}  # all the paths between all the hosts
    for s in hostsList:
        for d in hostsList:
            paths = []
            paths2=[]
            if (s.id == d.id):
                continue
            if (s.accessPoint == d.accessPoint):
                tempNodes = [s, s.accessPoint,
                             d]  ############################################################################
                tempNodes2 = [d, d.accessPoint, s]
                tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint][
                    'transmissionDelay'] + d.processingDelay
                tempDelay2 = d.transmissonDelay + d.processingDelay + G.nodes[d.accessPoint][
                    'transmissionDelay'] + s.processingDelay
                tempPath = Path.Path(tempNodes, tempDelay)
                tempPath2 = Path.Path(tempNodes2, tempDelay2)
                paths.append(tempPath)
                paths2.append(tempPath2)
                allPaths[s.id, d.id] = paths
                allPaths[d.id, s.id] = paths2
                continue
            else:
                tempList = list(
                    islice(nx.shortest_simple_paths(G, s.accessPoint, d.accessPoint, weight='processingDelay'),
                           k))
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
                            tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                            tempDelay2 = tempDelay2 + G.nodes[list(path2).__getitem__(n)]['transmissionDelay']
                            if (i < len(path)):
                                tempDelay = tempDelay + \
                                            G[list(path).__getitem__(n)][list(path).__getitem__(n + 1)][
                                                'processingDelay'] - G.nodes[list(path).__getitem__(n)][
                                                'transmissionDelay']
                                tempDelay2 = tempDelay2 + \
                                             G[list(path2).__getitem__(n)][list(path2).__getitem__(n + 1)][
                                                 'processingDelay'] - G.nodes[list(path2).__getitem__(n)][
                                                 'transmissionDelay']
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
                        allPaths[s.id, d.id] = paths
                        allPaths[d.id, s.id] = paths2

                # for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
                #     if (len(path) < 8):
                #         tempNodes = [s] ############################################################################
                #         tempDelay = s.transmissonDelay + s.processingDelay
                #         i = 1
                #         for n in range(len(path)):
                #             tempNodes.append(list(path).__getitem__(n))
                #             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                #             if(i < len(path)):
                #                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
                #             i = i + 1
                #         tempNodes.append(d) ############################################################################
                #         tempDelay = tempDelay + d.processingDelay
                #         tempPath = Path.Path(tempNodes,tempDelay)
                #         paths.append(tempPath)
                #         allPaths[s.id, d.id] = paths

    return allPaths



# #def findAllPath(G,hostsList): speed
# def findKthPath2(G,hostsList,k):
#     allPaths = {}  # all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             paths = []
#             if (s.id == d.id):
#                 continue
#             if (s.accessPoint == d.accessPoint):
#                 tempNodes = [s, s.accessPoint, d] ############################################################################
#                 tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint]['transmissionDelay'] + d.processingDelay
#                 tempPath = Path.Path(tempNodes,tempDelay)
#                 paths.append(tempPath)
#                 allPaths[s.id, d.id] = paths
#                 continue
#             else:
#                 tempList = list(islice(nx.shortest_simple_paths(G, s.accessPoint, d.accessPoint, weight='processingDelay'),k))
#                 for path in tempList:
#                     if(len(path) < 8):
#                         tempNodes = [s] ############################################################################
#                         tempDelay = s.transmissonDelay + s.processingDelay
#                         i = 1
#                         for n in range(len(path)):
#                             tempNodes.append(list(path).__getitem__(n))
#                             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                             if(i < len(path)):
#                                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']- G.nodes[list(path).__getitem__(n)]['transmissionDelay']  # we substracted because the delay is in combined mode((1))
#                             i = i + 1
#                         tempNodes.append(d) ############################################################################
#                         tempDelay = tempDelay + d.processingDelay
#                         tempPath = Path.Path(tempNodes,tempDelay)
#                         paths.append(tempPath)
#                         allPaths[s.id, d.id] = paths
#
#                 # for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
#                 #     if (len(path) < 8):
#                 #         tempNodes = [s] ############################################################################
#                 #         tempDelay = s.transmissonDelay + s.processingDelay
#                 #         i = 1
#                 #         for n in range(len(path)):
#                 #             tempNodes.append(list(path).__getitem__(n))
#                 #             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                 #             if(i < len(path)):
#                 #                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
#                 #             i = i + 1
#                 #         tempNodes.append(d) ############################################################################
#                 #         tempDelay = tempDelay + d.processingDelay
#                 #         tempPath = Path.Path(tempNodes,tempDelay)
#                 #         paths.append(tempPath)
#                 #         allPaths[s.id, d.id] = paths
#
#     return allPaths





###################################

# def findAllPath(G,hostsList):  speed
#     allPaths = {}  # all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             paths = []
#             if (s.id == d.id):
#                 continue
#             if (s.accessPoint == d.accessPoint):
#                 tempNodes = [s, s.accessPoint,
#                              d]  ############################################################################
#                 tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint][
#                     'transmissionDelay'] + d.processingDelay
#                 tempPath = Path.Path(tempNodes, tempDelay)
#                 paths.append(tempPath)
#                 allPaths[s.id, d.id] = paths
#                 continue
#             else:
#                 for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
#                     if (len(path) < 8):
#                         tempNodes = [s] ############################################################################
#                         tempDelay = s.transmissonDelay + s.processingDelay
#                         i = 1
#                         for n in range(len(path)):
#                             tempNodes.append(list(path).__getitem__(n))
#                             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                             if(i < len(path)):
#                                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
#                             i = i + 1
#                         tempNodes.append(d) ############################################################################
#                         tempDelay = tempDelay + d.processingDelay
#                         tempPath = Path.Path(tempNodes,tempDelay)
#                         paths.append(tempPath)
#                         allPaths[s.id, d.id] = paths
#
#     return allPaths



# def findKthPathold(G, hostsList,K): speed
#     allPaths = findAllPath(G,hostsList)   #all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             if (s.id == d.id):
#                 continue
#             else:
#                 if(s.id, d.id) in allPaths.keys():
#                     paths = allPaths[s.id, d.id]
#                     paths.sort(key= lambda x: x.delay)
#                     if(len(paths)>K):
#                         gap = len(paths) - K
#                         for i in range(gap):
#                             paths.pop()
#
#     return allPaths



def changeLinksBandwidth(G):

    for i in nx.edges(G, G.nodes):
        bandwidth = random.randint(500,1000)
        G[i[0]][i[1]]['bandwidth']= bandwidth


def findcandidatePaths(paths,delay):
    candidatePaths = []
    for path in paths:
        if(path.delay<= delay):
            candidatePaths.append(path)
        else:
            break

    return candidatePaths

def computeMeasurments(G, candidatePaths):
    for path in candidatePaths:
        TSNCounter = 0
        bandwidth = 3000

        for index in range(len(path.nodes)):
            if(index == 0 or index > len(path.nodes)-3):
                continue
            if (G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index + 1)]['nbOfTSN'] > TSNCounter):
                TSNCounter = G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index + 1)]['nbOfTSN']
            if(G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index+1)]['bandwidth']< bandwidth):
                bandwidth = G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index+1)]['bandwidth']
        path.TSNFlowCounter = TSNCounter
        path.bandwidth = bandwidth

def BestValues(candidatePaths):
    maxBandwidth = 0
    minHopCount = 1000
    minTSNCount = 10000
    for path in candidatePaths:
        if(path.bandwidth>maxBandwidth):
            maxBandwidth = path.bandwidth
        if(path.hopCount<minHopCount):
            minHopCount = path.hopCount
        if(path.TSNFlowCounter<minTSNCount):
            minTSNCount = path.TSNFlowCounter

    return maxBandwidth,minHopCount,minTSNCount


def pathSelection(G, tempTSNFlow, firstKthPaths, TSNCountWeight, bandwidthWeight, hopCountWeight):
    if((tempTSNFlow.source.id,tempTSNFlow.destniation.id) not in firstKthPaths.keys()):
        return False
    paths = firstKthPaths[tempTSNFlow.source.id,tempTSNFlow.destniation.id]
    candidatePaths = findcandidatePaths(paths,tempTSNFlow.flowMaxDelay)

    if len(candidatePaths)==0:
        return False,candidatePaths
    elif (len(candidatePaths)==1):
        tempTSNFlow.path = candidatePaths.__getitem__(0)
        tempTSNFlow.candidatePathCounter = 1
        return True,candidatePaths
    else:
        tempTSNFlow.candidatePathCounter = len(candidatePaths)
        computeMeasurments(G, candidatePaths)
        maxBandwidth, minHopCount, minTSNCount = BestValues(candidatePaths)
        maxDelta = 0
        for path in candidatePaths:
            hopCountRelativeValue = minHopCount/path.hopCount
            bandwidthRelativeValue = path.bandwidth/maxBandwidth
            if(path.TSNFlowCounter ==0):
                TSNCounterRaltiveValue = 1
            else:
                TSNCounterRaltiveValue = minTSNCount/path.TSNFlowCounter


            Delta = (hopCountWeight * hopCountRelativeValue) + (bandwidthWeight * bandwidthRelativeValue) + (TSNCountWeight * TSNCounterRaltiveValue)
            if(Delta>maxDelta):
                maxDelta = Delta
                tempTSNFlow.path = path
        return True,candidatePaths

    return False,candidatePaths


def computeTimeSlotLength(G, hostLists, firstKthPaths):
    maxDelay = 0
    for s in hostLists:
        for d in hostLists:
            if s.id == d.id:
                continue
            if((s.id,d.id)in firstKthPaths.keys()):
                paths = firstKthPaths[s.id,d.id]
                for path in paths:
                    if(path.delay>maxDelay):
                        maxDelay = path.delay



    return maxDelay


def createTimeSlots(nbOfTimeSlots):
    timeSlots = []
    for index in range(nbOfTimeSlots):
        tempTimeSlot = TimeSlot.TimeSlot(index,[])
        timeSlots.append(tempTimeSlot)
    return timeSlots



def map(G,tempTSNFlow,startTime):
    operations=[]
    cmulativeTime = startTime
    path = tempTSNFlow.path
    for i in range(len(tempTSNFlow.path.nodes)):
        if (i == 0):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).transmissonDelay
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 2):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G[tempTSNFlow.path.nodes.__getitem__(i)][tempTSNFlow.path.nodes.__getitem__(i+1)]['processingDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 1):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1).id)
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        else:
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i-1),tempTSNFlow.path.nodes.__getitem__(i).id)
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)

    return operations




def SWOTS(G, tempTSNFlow,scheduledFlowsSWOTS,CLength):
    startTime = 0

    if(len(scheduledFlowsSWOTS)!=0):
        operations = map(G, tempTSNFlow,startTime)
        index = 2
        for operation in operations[2::2]:
            for scheduledItem in scheduledFlowsSWOTS:
                SF = scheduledItem.__getitem__(0)
                SST = scheduledItem.__getitem__(1)
                SFO = map(G,SF,SST)
                for SO in SFO[2::2]:
                    if(SO.id == operation.id):
                        gap = SO.cumulativeDelay - operations.__getitem__(index-1).cumulativeDelay
                        if (gap>startTime):
                            startTime = gap
                        break

            index = index + 2
        if((startTime + operations.__getitem__(len(operations)-2).cumulativeDelay)<=CLength):
            scheduledFlowsSWOTS.append((tempTSNFlow,startTime))
            return True



    else:
        scheduledFlowsSWOTS.append((tempTSNFlow,startTime))
        return(True)


    return False

def SWTS(G, tempTSNFlow,scheduledFlowsSWTS ,CLength,timeSlots, now, FTT):
    path = tempTSNFlow.path
    isScheduled = False
    publishTime = 15000 + 1000              #state-of-the-art SDN switches could insert forwaring entry in 15 ms (15000 microseconds), 1 ms for sending the configuration from the controller
    slotLength = CLength/len(timeSlots)
    nextSlot = (math.floor(((now-FTT+publishTime)%CLength)/slotLength)+1)%len(timeSlots)
    counter = 1
    pathEdges = []
    for index in range(len(path.nodes)):
        if (index == 0):
            # tempLink = '({},{})'.format(path.nodes.__getitem__(index).id, path.nodes.__getitem__(index + 1))
            # pathEdges.append(tempLink)
            continue
        elif(index <len(path.nodes)-2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index), path.nodes.__getitem__(index + 1))
            pathEdges.append(tempLink)
        elif(index ==len(path.nodes)-2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index), path.nodes.__getitem__(index + 1).id)
            pathEdges.append(tempLink)
    while True:
        tempSlot = timeSlots.__getitem__(nextSlot)
        isScheduled = True
        for edge in pathEdges:
            if(tempSlot.Scheduledlinks.__contains__(edge)):
                isScheduled = False
                break
        if(isScheduled or counter>len(timeSlots)):
            break
        counter = counter + 1
        nextSlot = (nextSlot + 1)%len(timeSlots)
    if(isScheduled):
        tempSlot = timeSlots.__getitem__(nextSlot)
        for edge in pathEdges:
            tempSlot.Scheduledlinks.append(edge)
        scheduledFlowsSWTS.append((tempTSNFlow,nextSlot))

    return isScheduled


def display(path):
    text = '[ '
    for n in range(len(path.nodes)):
        if (n == 0):
            text = text + '{}, '.format(path.nodes.__getitem__(n).id)
        elif(n== len(path.nodes)-1):
            text = text + '{} ] '.format(path.nodes.__getitem__(n).id)
        else:
            text = text + '{}, '.format(path.nodes.__getitem__(n))

    return text

def findFlowArrivalTime(flow, flowsList):
    arrivalTime = -1
    for index in range(len(flowsList)):
        tempStoredItem = list(flowsList).__getitem__(index)
        if(tempStoredItem.__getitem__(0).id == flow.id):
            return tempStoredItem.__getitem__(1)


    return arrivalTime


def countGates(G, scheduledSWOTS):
    numberOfGates = 0
    numberOfMergedGates = 0
    index = 0
    for scheduledItem in scheduledSWOTS[0:len(scheduledSWOTS):]:
        operations = map(G,scheduledItem.__getitem__(0),scheduledItem.__getitem__(1))
        for operation in operations[2:len(operations):2]:
            numberOfGates = numberOfGates + 1
            for tempScheduledItem in scheduledSWOTS[index+1:len(scheduledSWOTS):]:
                tempOperations = map(G,tempScheduledItem.__getitem__(0),tempScheduledItem.__getitem__(1))
                index2 = 2
                for tempOperation in tempOperations[2:len(tempOperations):2]:
                    if((operation.id == tempOperation.id) and (operation.cumulativeDelay-tempOperations.__getitem__(index2-1).cumulativeDelay ==0)):
                        numberOfMergedGates = numberOfMergedGates + 1

                    index2 = index2 + 2







        index = index + 1


    return numberOfGates,numberOfMergedGates



























def main():

    # Reading the simulation parameters #
    ##########################################
    # n = int(input('Enter the value of n: '))
    # p = float(input('Enter the value of p: '))
    ##########################################


    # Setting the simulation parameters #
    ##########################################
    n= 10                   #number of switches
    hosts = 15              #number of hosts
    nbOfTSNFlows = 100      #number of TSN flows
    pFlow = 0.1             #the probability that a flow will arrive at each time unit
    p= 0.3                  #the probability of having an edge between any two nodes
    k = 10                  #the number of paths that will be chosen between each source and destination
    timeSlotsAmount = 5     #how many time slots in the schedule --> the length of the schedule
    TSNCountWeight = 1/3
    bandwidthWeight = 1/3
    hopCountWeight = 1/3
    ##########################################

    # Creating the graphs #
    ##########################################
    G = nx.erdos_renyi_graph(n,p)
    for node in range(n):
        if(nx.degree(G,node)==0):
            G.remove_node(node)
    ##########################################

    # Draw the graph #
    ##########################################
    plt.subplot(121)
    nx.draw(G,with_labels = True)
    plt.subplot(122)
    nx.draw(G, with_labels = True, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
    plt.show()
    ##########################################


    # Filling the values randomly #
    ##########################################
    transmissionDelays, linkMeasurments, hostsList = rand(G, hosts,n)
    nx.set_node_attributes(G, transmissionDelays)
    nx.set_edge_attributes(G,linkMeasurments)
    ##########################################

    G = G.to_directed(False)

    # pre-routing phase #
    ##########################################
    # oldStart = timer() speed
    # oldFirstKthPaths = findKthPathold(G, hostsList, k)
    # oldEnd = timer()
    # oldThelongestTimeEver = oldEnd - oldStart

    convertProcDelayToComulativeDelay(G,1)  # after this statment procDelay = proc Delay of next hop + trans Delay of next hop + progation delay of the link
    start = timer()
    firstKthPaths = findKthPath(G,hostsList,k) # The first kth paths between all the hosts (based on path delay)
    end = timer()
    preRoutingPhaseTime = end - start

    # start2 = timer() speed
    # firstKthPaths2 = findKthPath2(G,hostsList,k) # The first kth paths between all the hosts (based on path delay)
    # end2 = timer()
    # ThelongestTimeEver2 = end2 - start2

    # anotherStart = timer() speed
    # anotherFirstKthPaths = findKthPathP(G,hostsList,k)
    # anotherEnd= timer()
    # anotherThelongestTimeEver = anotherEnd - anotherStart

    # anotherStart2 = timer() speed
    # anotherFirstKthPaths2 = findKthPathP2(G,hostsList,k)
    # anotherEnd2= timer()
    # anotherThelongestTimeEver2 = anotherEnd2 - anotherStart2
    convertProcDelayToComulativeDelay(G,0) #after this statment procDelay = proc Delay of next hop + propgation Delay of the link

    # convertProcDelayToComulativeDelay(G,
    #                                   1)  # after this statment procDelay = proc Delay of next hop + trans Delay of next hop + progation delay of the link
    # convertProcDelayToComulativeDelay(G,0) #after this statment procDelay = proc Delay of next hop + propgation Delay of the link
    # print(((end-start)/60)/60)


    ##########################################

    ##########################################

    CLength = 0           #the schedule cycle length
    timeSlotLength = 0    #the length of each time slot

    #Setting the values:
    timeSlotLength = computeTimeSlotLength(G,hostsList, firstKthPaths)
    CLength = timeSlotsAmount * timeSlotLength







    timeSlots = createTimeSlots(timeSlotsAmount)    #the list of time slots
    flowsList = []                                  #list of all created TSN flows
    scheduledFlowsSWOTS = []                        #list of all scheduled TSN flows using SWOTS
    scheduledFlowsSWTS =[]                          #list of all scheduled TSN flows using SWTS
    counter = 0                                     #count the created TSN flows
    scheduledCounterSWOTS = 0                       #count the scheduled TSN flows (routed and scheduled) using SWOTS
    scheduledCounterSWTS = 0                        #count the scheduled TSN flows (routed and scheduled) using SWTS
    routedCounter = 0                               #count the routed TSN flows, but not scheduled
    time = 0                                        #Track the arrival time of TSN flows
    routingExecutionTimes = []                      #a list of the execution times of the routing algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    SWOTSSchedulingExectionTimes = []               #a list of the execution times of the SWOTS algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    SWTSSchedulingExectionTimes = []                #a list of the execution times of the SWTS algorithm for all flows in microseconds [(1.3,True),(0.7,False)]



    while(True):
        if counter >= nbOfTSNFlows:
            break
        changeLinksBandwidth(G)             #change the link bandwidth randomly, in future it will be based on the best effort streams
        x = random.random()
        if(x<=pFlow):


            # # this for loop to update the paths measurments
            # for s in hostsList:
            #     for d in hostsList:
            #         if(s.id == d.id):
            #             continue
            #         paths = firstKthPaths[s.id,d.id]
            #         computeMeasurments(G,paths)



            s=0
            d=0
            while s==d:
                s = random.choice(hostsList)
                d = random.choice(hostsList)
            tempTSNFlow = TSNFlow.TSNFlow(counter,s,d)
            flowsList.append((tempTSNFlow,time))
            counter = counter + 1
            # Path-Selection phase #
            ##########################################
            start = timer()
            tempRouted, candidatePaths = pathSelection(G, tempTSNFlow, firstKthPaths, TSNCountWeight, bandwidthWeight, hopCountWeight)
            end = timer()
            routingExecutionTimes.append((((end - start) * 1000 * 1000),tempRouted))
            ##########################################


            if(tempRouted):
                routedCounter = routedCounter + 1

                # print('Flow ({}) from Source ({}) to destination ({}) with maximum delay = ({}) routed through {}'.format(tempTSNFlow.id,tempTSNFlow.source.id,tempTSNFlow.destniation.id,tempTSNFlow.flowMaxDelay,tempTSNFlow.path.nodes))
                # if len(candidatePaths) == 0:
                #     print('there is no candidate paths')
                # elif (len(candidatePaths) == 1):
                #     print('this is the only available path')
                #     for index in range(len(tempTSNFlow.path.nodes)):
                #         if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                #             continue
                #         G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)]['nbOfTSN'] = G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)]['nbOfTSN'] +1
                #
                # else:
                #     tempTSNFlow.candidatePathCounter = len(candidatePaths)
                #     computeMeasurments(G, candidatePaths)
                #     maxBandwidth, minHopCount, minTSNCount = BestValues(candidatePaths)
                #     maxDelta = 0
                #     print('Here is the other paths values:')
                #     i = 1
                #     for path in candidatePaths:
                #
                #
                #         hopCountRelativeValue = minHopCount / path.hopCount
                #         bandwidthRelativeValue = path.bandwidth / maxBandwidth
                #         if (path.TSNFlowCounter == 0):
                #             TSNCounterRaltiveValue = 1
                #         else:
                #             TSNCounterRaltiveValue = minTSNCount / path.TSNFlowCounter
                #
                #         Delta = (hopCountWeight * hopCountRelativeValue) + (
                #                         bandwidthWeight * bandwidthRelativeValue) + (
                #                                 TSNCountWeight * TSNCounterRaltiveValue)
                #         print('path ({}) is {} has delay = ({}), bandwidth = ({}),hop counts = ({}), and TSN count = ({}). The resulted Delta = ({})'.format(i,
                #                                                                                                      path.nodes,
                #                                                                                                      path.delay,
                #                                                                                                      path.bandwidth,
                #                                                                                                      path.hopCount,path.TSNFlowCounter,
                #                                                                                                                                 Delta))
                #         i = i +1
                #         if (Delta > maxDelta):
                #             maxDelta = Delta
                #             #tempTSNFlow.path = path
                #     for index in range(len(tempTSNFlow.path.nodes)):
                #         if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                #             continue
                #         G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)]['nbOfTSN'] = G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)]['nbOfTSN'] +1
                # print('==========================')




            # Scheduling WithOut Time Slots (SWOTS) #
            ##########################################
            start = timer()
            tempScheduledSWOTS = SWOTS(G, tempTSNFlow, scheduledFlowsSWOTS, CLength)
            end = timer()
            SWOTSSchedulingExectionTimes.append((((end - start) * 1000 * 1000), tempScheduledSWOTS))
            ##########################################
            print((end - start) * 1000 * 1000)

            if(tempScheduledSWOTS):
                scheduledCounterSWOTS = scheduledCounterSWOTS + 1
                for index in range(len(tempTSNFlow.path.nodes)):
                    if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                        continue
                    G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)][
                        'nbOfTSN'] = \
                    G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)][
                        'nbOfTSN'] + 1


            if(len(flowsList) == 0):
                FTT = time
            else:
                FTT = flowsList.__getitem__(0).__getitem__(1)


            # Scheduling With Time Slots (SWTS) #
            ##########################################
            start = timer()
            tempScheduledSWTS = SWTS(G, tempTSNFlow, scheduledFlowsSWTS, CLength, timeSlots, time, FTT)
            end = timer()
            SWTSSchedulingExectionTimes.append((((end - start) * 1000 * 1000), tempScheduledSWTS))
            ##########################################


            if(tempScheduledSWTS):
                scheduledCounterSWTS = scheduledCounterSWTS + 1
                for index in range(len(tempTSNFlow.path.nodes)):
                    if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                        continue
                    G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)][
                        'nbOfTSN'] = \
                    G[tempTSNFlow.path.nodes.__getitem__(index)][tempTSNFlow.path.nodes.__getitem__(index + 1)][
                        'nbOfTSN'] + 1








            # i = 3
            # b = 5
            # text = '{},{}'.format(i,b)
            # print(text)
            # x =3
            # w =4
            # zag = '{},{}'.format(x,w)
            # if(text == zag):
            #     print('yes')



        time = time + 1



    # nbOfGates, nbOfmergedGates = countGates(G,scheduledFlowsSWOTS)
    # print(nbOfGates)
    # print(nbOfmergedGates)
    # reducePrecentage = (nbOfmergedGates/nbOfGates)*100
    print('The total number of flows: {}'.format(nbOfTSNFlows))
    # print('The percentage of reduced gates: {}%'.format(reducePrecentage))
    # print('nb of scheduled flows using SWOTS: {}'.format(scheduledCounterSWOTS))
    print('nb of scheduled flows using SWTS: {}'.format(scheduledCounterSWTS))
    ##
    total = 0
    for x in routingExecutionTimes:
        total = total +x.__getitem__(0)
    averageRoutingTime = total/len(routingExecutionTimes)
    print('Average routing Time: {}'.format(averageRoutingTime))


    total = 0
    for x in SWTSSchedulingExectionTimes:
        total = total +x.__getitem__(0)
    averageSWTSTime = total/len(routingExecutionTimes)
    print('Average SWTS Time: {}'.format(averageSWTSTime))
    print('The pre routing phase: {}'.format(preRoutingPhaseTime))
    # print('The pre routing phase2: {}'.format(ThelongestTimeEver2)) speed
    # print('The pre routing phase with multithreading: {}'.format(anotherThelongestTimeEver))
    # print('The pre routing phase with multithreading2: {}'.format(anotherThelongestTimeEver2))
    # print('The pre routing phase with old: {}'.format(oldThelongestTimeEver))



    # total = 0
    # for x in SWOTSSchedulingExectionTimes:
    #     total = total +x.__getitem__(0)
    # averageSWOTSTime = total/len(SWOTSSchedulingExectionTimes)
    # print('Average SWOTS Time: {}'.format(averageSWOTSTime))


    ##





    # print(routingExecutionTimes)
    # print(SWOTSSchedulingExectionTimes)
    # print(SWTSSchedulingExectionTimes)
    #
    #
    # print(routedCounter)
    # print(scheduledCounterSWOTS)
    # print(scheduledCounterSWTS)



    # print('Total = ({}) \nRouted = ({}) \nSWOTS = ({}) \nSWTS = ({})'.format(len(flowsList),routedCounter,scheduledCounterSWOTS,scheduledCounterSWTS))
    # for time in timeSlots:
    #     print(time.Scheduledlinks)






    # for scheduledItem in scheduledFlowsSWOTS:
    #     tempFlow = scheduledItem.__getitem__(0)
    #     tempStartTime = scheduledItem.__getitem__(1)
    #     tempPath = tempFlow.path
    #     displayPath = display(tempPath)
    #     print('Flow ({}) arrived at time ({}), routed through {}, scheduled at ({})'.format(tempFlow.id, findFlowArrivalTime(tempFlow,flowsList),displayPath, tempStartTime))


















    # dict = {}
    # x = 4
    # y = 8
    # z = 5
    # dict[x,y] = [1,2,3]
    # if((x,y) in dict.keys()):
    #     print(dict[x,y])


    # for s in hostsList:
    #     for d in hostsList:
    #         if((s.id,d.id) in allPaths.keys()):
    #             paths = allPaths[s.id, d.id]
    #             for path in paths:
    #                 print(path.nodes)
    #                 print(path.delay)
    #                 text = ''
    #                 for i in range(len(path.nodes)):
    #                     if(i ==0):
    #                         text = text + str(list(path.nodes).__getitem__(i)) + 'transmission delay =' + str(findHost(hostsList,list(path.nodes).__getitem__(i)).transmissonDelay) + 'processing delay =' + str(findHost(hostsList,list(path.nodes).__getitem__(i)).processingDelay) + '\n'
    #                     elif(i<len(path.nodes)-2):
    #                         text = text + str(list(path.nodes).__getitem__(i)) + 'transmission delay =' + str(G.nodes[list(path.nodes).__getitem__(i)]['transmissionDelay']) + 'processing delay =' + str(G[list(path.nodes).__getitem__(i)][list(path.nodes).__getitem__(i+1)]['processingDelay']) + '\n'
    #                     elif(i<len(path.nodes)-1):
    #                         text = text + str(list(path.nodes).__getitem__(i)) + 'transmission delay =' + str(G.nodes[list(path.nodes).__getitem__(i)]['transmissionDelay']) + '\n'
    #                     else:
    #                         text = text + str(list(path.nodes).__getitem__(i)) + 'processing delay =' + str(findHost(hostsList,list(path.nodes).__getitem__(i)).processingDelay) + '\n'
    #                 print(text)





    # for i in nx.edges(G, G.nodes):
    #     print(G[i[0]][i[1]]['nbOfTSN'])


    #print(nx.edges(G,G.nodes))
    # for i in G.nodes:
    #     print(G.nodes[i]['transmissionDelay'])









    # pathslist = [] speed
    # for s in hostsList:
    #     for d in hostsList:
    #         if((s.id,d.id) in firstKthPaths.keys()):
    #             paths = firstKthPaths[s.id, d.id]
    #
    #             for path in paths:
    #                 textTemp = '('
    #                 for index in range (len(path.nodes)):
    #                     if(index ==0):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ', '
    #                     elif(index == len(path.nodes)-1):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ')[delay={}]'.format(path.delay)
    #                     else:
    #                         textTemp = textTemp + '{}'.format(path.nodes[index]) + ', '
    #                 pathslist.append(textTemp)
    #
    # print(pathslist)
    #
    #
    # pathslist2 = []
    # for s in hostsList:
    #     for d in hostsList:
    #         if((s.id,d.id) in anotherFirstKthPaths.keys()):
    #             paths = anotherFirstKthPaths[s.id, d.id]
    #
    #             for path in paths:
    #                 textTemp = '('
    #                 for index in range (len(path.nodes)):
    #                     if(index ==0):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ', '
    #                     elif(index == len(path.nodes)-1):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ')[delay={}]'.format(path.delay)
    #                     else:
    #                         textTemp = textTemp + '{}'.format(path.nodes[index]) + ', '
    #                 pathslist2.append(textTemp)
    #
    # print(pathslist2)
    #
    #
    # pathslist3 = []
    # for s in hostsList:
    #     for d in hostsList:
    #         if((s.id,d.id) in oldFirstKthPaths.keys()):
    #             paths = oldFirstKthPaths[s.id, d.id]
    #
    #
    #             for path in paths:
    #                 textTemp = '('
    #                 for index in range (len(path.nodes)):
    #                     if(index ==0):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ', '
    #                     elif(index == len(path.nodes)-1):
    #                         textTemp = textTemp + '{}'.format(path.nodes[index].id) + ')[delay={}]'.format(path.delay)
    #                     else:
    #                         textTemp = textTemp + '{}'.format(path.nodes[index]) + ', '
    #                 pathslist3.append(textTemp)
    #
    # print(pathslist3)
    #
    # print(pathslist == pathslist2)
    # print(pathslist == pathslist3)
    # print(pathslist2 == pathslist3)



main()
