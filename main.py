
import random
import networkx as nx
import matplotlib.pyplot as plt
import TSNFlow
import TSNHost

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
                continue
            if (s.accessPoint == d.accessPoint):
                tempPath = [s.id, s.accessPoint, d.id]
                paths.append(tempPath)
                allPaths[s.id, d.id] = paths
                continue
            else:
                for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
                    if (len(path) < 8):
                        tempPath = [s.id]
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
    # for s in hostsList:
    #     for d in hostsList:
    #         paths = []
    #         if(s.id == d.id):
    #             continue
    #         if(s.accessPoint == d.accessPoint):
    #             tempPath = [s.id,s.accessPoint,d.id]
    #             paths.append(tempPath)
    #             allPaths[s.id,d.id] = paths
    #             continue
    #         else:
    #             for path in nx.all_simple_paths(G,s.accessPoint,d.accessPoint):
    #                 if(len(path)<8):
    #                     tempPath = [s.id]
    #                     for n in path:
    #                         tempPath.append(n)
    #                     tempPath.append(d.id)
    #                     paths.append(tempPath)
    #                     allPaths[s.id,d.id]= paths




    print(allPaths.keys())
    print(len(allPaths[5,6]))








    # for i in nx.edges(G, G.nodes):
    #     print(G[i[0]][i[1]]['processingDelay'])


    #print(nx.edges(G,G.nodes))
    # for i in G.nodes:
    #     print(G.nodes[i]['transmissionDelay'])


main()

# allPaths={} #all the paths between all the hosts
# for S in hostsList:
#     for D in hostsList:
#         paths = []  # all the paths between two hosts
#         if(S.id != D.id):
#             if(S.accessPoint == D.accessPoint):
#                 paths.append([S.id,S.accessPoint,D.id])
#                 break
#             for B in nx.neighbors(G, S.accessPoint):
#                 if D.accessPoint == B:
#                     paths.append([S.id,S.accessPoint,B,D.id])
#                     break
#                 for N in nx.neighbors(G, B):
#                     if (N == S.accessPoint):
#                         break
#                     if D.accessPoint == N:
#                         paths.append([S.id,S.accessPoint,B,N,D.id])
#                         break
#                     for U in nx.neighbors(G, N):
#                         if (U == S.accessPoint) or (U == B):
#                             break
#                         if D.accessPoint == U:
#                             paths.append([S.id,S.accessPoint,B,N,U,D.id])
#                             break
#                         for L in nx.neighbors(G, U):
#                             if (L == S.accessPoint) or (L == B) or (L == N):
#                                 break
#                             if D.accessPoint == L:
#                                 paths.append([S.id,S.accessPoint,B,N,U,L,D.id])
#                                 break
#                             for K in nx.neighbors(G, L):
#                                 if (K == S.accessPoint) or (K == B) or (K == N) or (K == U):
#                                     break
#                                 if D.accessPoint == K:
#                                     paths.append([S.id,S.accessPoint,B,N,U,L,K,D.id])
#                                     break
#                                 for R in nx.neighbors(G, K):
#                                     if (R == S.accessPoint) or (R == B) or (R == N) or (R == U) or (R == L):
#                                         break
#                                     if D.accessPoint == R:
#                                         paths.append([S.id,S.accessPoint,B,N,U,L,K,R,D.id])
#             print(paths.__getitem__(0))
#             allPaths[S.id,D.id] = paths



