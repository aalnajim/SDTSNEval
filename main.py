
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



def findAllPath(G,hostsList):

    allPaths = {}  # all the paths between all the hosts

    for s in hostsList:
        for d in hostsList:
            paths = []
            if (s.id == d.id):
                continues
            if (s.accessPoint == d.accessPoint):
                tempNodes = [s.id, s.accessPoint, d.id]
                tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint]['transmissionDelay'] + d.processingDelay
                tempPath = Path(tempNodes,tempDelay)
                paths.append(tempPath)
                allPaths[s.id, d.id] = paths
                continue
            else:
                for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
                    if (len(path) < 8):
                        tempNodes = [s.id]
                        tempDelay = tempDelay + 1
                        for n in path:
                            tempPath.append(n)
                        tempPath.append(d.id)
                        paths.append(tempPath)
                        allPaths[s.id, d.id] = paths

    return allPaths



def main():

    # Reading the simulation parameters #
    ##########################################
    # n = int(input('Enter the value of n: '))
    # p = float(input('Enter the value of p: '))
    ##########################################


    # Setting the simulation parameters #
    ##########################################
    n= 5
    hosts = 3
    p= 0.5
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


    allPaths = findAllPath(G,hostsList)           #all the paths between all the hosts
    # print(allPaths.keys())
    # print(len(allPaths[5,6]))




    l1 = [1,2,3,4,5]
    print(l1.__getitem__(4))
    print(len(l1))







    # for i in nx.edges(G, G.nodes):
    #     print(G[i[0]][i[1]]['processingDelay'])


    #print(nx.edges(G,G.nodes))
    # for i in G.nodes:
    #     print(G.nodes[i]['transmissionDelay'])


main()





