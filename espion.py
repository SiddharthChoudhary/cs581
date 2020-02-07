""" 
                                    Assigment done by SIDDHARTH CHOUDHARY


This assignment deals with traversing the csv file and then converting it into a graph and then calculating the following
attributes like: trust, distrust edges, total no of edges, triads, Expected attributes and actual distribution 

RUN THE PROGRAM:-

1.) pip install -r requirements.txt (in case you don't have pandas or netowrkx installed)
2.) python epinion.py

and that's it, now you would be prompted for the filename and please enter that
For example:

    ENTER THE CSV FILE NAME:  epinions_small.csv

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

#this creates a graph by running networkx and then gives triads-with-weights structure and other important details required
triads_with_weights,self_loop,trust,distrust,graph,triads = formGraph(filename)
#print the lines for normal calculation by 
printLines(self_loop,trust,distrust,triads,graph)

#creates a triadTable which helps generating the expected and actual probability
triadTable= createTable(triads_with_weights)

#this calculates probability and gives us all the probability related stuff
trust_prob,distrust_prob,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4   =   calculateProbability(trust,distrust,triads)


print("probability p:", trust_prob)
print("probability 1-p:", distrust_prob)

print("\n")
printExpected(triadTable,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4)

print("\n")
printActual(triadTable)