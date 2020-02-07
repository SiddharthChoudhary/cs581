""" 
                                    Assigment done by SIDDHARTH CHOUDHARY


This assignment deals with traversing the csv file and then converting it into a graph and then calculating the following
attributes like: trust, distrust edges, total no of edges, triads, Expected attributes and actual distribution 


"""


from itertools import combinations as comb
import networkx
from pprint import pprint
import pandas as pd
from formGraph import formGraph,calculateProbability
from pprint import pprint
from printing import printLines,createTable,printActual,printExpected

# self_loop_count, pos_count, neg_count, G,triadsSid = graph_and_stats("epinions_small.csv")
filename = raw_input("ENTER THE CSV FILE NAME:  ")
triads_with_weights,self_loop,trust,distrust,graph,triads = formGraph(filename)

printLines(self_loop,trust,distrust,triads,graph)

triadTable= createTable(triads_with_weights)

trust_prob,distrust_prob,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4   =   calculateProbability(trust,distrust,triads)


print("probability p:", trust_prob)
print("probability 1-p:", distrust_prob)

print("\n")
printExpected(triadTable,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4)

print("\n")
printActual(triadTable)