import networkx
from itertools import combinations as comb

def calculatetriadsWithWeight(triads,edges):
    triads_with_weights=list()
    for triad in triads:
        outerList=list()
        for combination in comb(triad,2):
            innerList=list()
            innerList.append(combination)
            innerList.append(edges[combination])
            outerList.append(innerList)
        #append each iteration's minilists of like [  [23434,1],[23433,1],[2342,1]    ] to the main list down here
        triads_with_weights.append(outerList)
    return triads_with_weights
def formGraph(filename):
    graph = networkx.Graph()
    self_loops=0
    trust=0
    distrust=0
    #let's open the csv file and read line by line
    with open(filename,"r") as file:
        for row in file:
            rowelements=row.split(",")
            reviewer=rowelements[0]
            reviewee=rowelements[1]
            weight  =int(rowelements[2])
            if int(reviewer) == int(reviewee):
                self_loops+=1
            elif int(weight) == 1:
                trust+=1
            elif int(weight)==-1:
                distrust+=1
            graph.add_edge(reviewer,reviewee,weight=int(weight))
    # after calculating the graphs positive and negative count now it is time to calculate 
    # triads in the folllowing graph
    edges = networkx.get_edge_attributes(graph,"weight")
    triads=[]
    for triad in networkx.enumerate_all_cliques(graph):
        if len(triad)==3:
            triads.append(triad)
    #till here we got the triads for the following data
    triads_with_weights = calculatetriadsWithWeight(triads,edges)
    return triads_with_weights,self_loops,trust,distrust,graph,triads

def calculateProbability(trust,distrust,traids):  
    randList = list()  
    randList2=list()
    num_edges = trust + distrust
    trust_prob = trust / num_edges
    disttrust_prob = 1 - trust_prob
    #for normal traids
    for i in traids:
        randList.append(i)
        trusts = 8*(len(i)+3)/num_edges
        randList.append(trusts)
    #for types
    for j in traids:
        randList2.append(j)
        trusts = 8*(len(i)+3)/num_edges
        randList2.append(trusts)
    probability_for_type1 = trust_prob * trust_prob * trust_prob
    probability_for_type2 = 3 * (trust_prob * trust_prob * disttrust_prob)
    probability_for_type3 = 3 * (trust_prob * disttrust_prob * disttrust_prob)
    probability_for_type4 = disttrust_prob * disttrust_prob * disttrust_prob
    return trust_prob,disttrust_prob,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4