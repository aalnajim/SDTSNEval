
import random
import networkx as nx
import matplotlib.pyplot as plt
import TSNFlow
import TSNHost
import Path

from TSNHost import TSNHost


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

def findHost(hostsList, id):
    for h in hostsList:
        if (h.id == id):
            return h


def findAllPath(G,hostsList):

    allPaths = {}  # all the paths between all the hosts

    for s in hostsList:
        for d in hostsList:
            paths = []
            if (s.id == d.id):
                continue
            if (s.accessPoint == d.accessPoint):
                tempNodes = [s.id, s.accessPoint, d.id]
                tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint]['transmissionDelay'] + d.processingDelay
                tempPath = Path.Path(tempNodes,tempDelay)
                paths.append(tempPath)
                allPaths[s.id, d.id] = paths
                continue
            else:
                for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
                    if (len(path) < 8):
                        tempNodes = [s.id]
                        tempDelay = s.transmissonDelay + s.processingDelay
                        i = 1
                        for n in range(len(path)):
                            tempNodes.append(list(path).__getitem__(n))
                            tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                            if(i < len(path)):
                                tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
                            i = i + 1
                        tempNodes.append(d.id)
                        tempDelay = tempDelay + d.processingDelay
                        tempPath = Path.Path(tempNodes,tempDelay)
                        paths.append(tempPath)
                        allPaths[s.id, d.id] = paths

    return allPaths


def findKthPath(G, hostsList,K):
    allPaths = findAllPath(G,hostsList)   #all the paths between all the hosts
    for s in hostsList:
        for d in hostsList:
            if (s.id == d.id):
                continue
            else:
                if(s.id, d.id) in allPaths.keys():
                    paths = allPaths[s.id, d.id]
                    paths.sort(key= lambda x: x.delay)
                    if(len(paths)>K):
                        gap = len(paths) - K
                        for i in range(gap):
                            paths.pop()

    return allPaths




def main():

    # Reading the simulation parameters #
    ##########################################
    # n = int(input('Enter the value of n: '))
    # p = float(input('Enter the value of p: '))
    ##########################################


    # Setting the simulation parameters #
    ##########################################
    n= 6
    hosts = 4
    p= 0.5
    k = 5
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


    firstKthPaths = findKthPath(G,hostsList,k) # The first kth paths between all the hosts (based on path delay)















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
    #     print(G[i[0]][i[1]]['processingDelay'])


    #print(nx.edges(G,G.nodes))
    # for i in G.nodes:
    #     print(G.nodes[i]['transmissionDelay'])


main()





