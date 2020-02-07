import pandas as pd
def printLines(self_loop,trust,distrust,triads,graph):
    #casting in int, incase just wanted to be secure and robust
    self_loop=int(self_loop)
    trust = int(trust)
    distrust=int(distrust)
    print("\n")
    print("Number of,")
    print("Self Loops:", self_loop)
    print("Total Edges:",trust+distrust)
    print("Total Nodes:", trust+distrust-self_loop)
    print("Trust Edges:", trust)
    print("Distrust Edges:", distrust)
    print("Nodes in triads:",calculateNodeInTriads(triads))
    print("Total Nodes:",len(graph.nodes()))

def calculateNodeInTriads(triads):
    count=1
    for i in triads:
        for j in i:
            count+=1
    return count

#this function deals with trust_category 
def trust_category(cell):
    display=list()
    categories = {(1,1,1) : "TTT",(-1,1,1) : "TTD",(-1,-1,1) : "TDD",(-1,-1,-1) : "DDD"}
    for row in cell:
        display.append(row[1])
    display = sorted(display)
    return categories[tuple(display)]

#this creates the table by using trustcategory and DataFrame refer  https://www.geeksforgeeks.org/python-pandas-dataframe/
def createTable(triadswithweights):
    for i in triadswithweights:
        i.append(trust_category(i))
    col_format = tuple(zip(*triadswithweights))
    row_format = tuple()
    table = pd.DataFrame({
        "trust_category": col_format[3],
        "edge_1": tuple(zip(*col_format[0]))[0],
        "trust_1": tuple(zip(*col_format[0]))[1],
        "edge_2": tuple(zip(*col_format[1]))[0],
        "trust_2": tuple(zip(*col_format[1]))[1],
        "edge_3": tuple(zip(*col_format[2]))[0],
        "trust_3": tuple(zip(*col_format[2]))[1]
    })
    triad_table_1=table
    for i in triad_table_1:
        for j in i:
            row_format=pd.DataFrame({
                "0":tuple(zip(*col_format[1]))[0],
                "1":tuple(zip(*col_format[1]))[0],
                "2":tuple(zip(*col_format[1]))[0],
                "3":tuple(zip(*col_format[1]))[0]
            })            
    triad_table = table.sort_values(['trust_category'],ascending=False).reset_index(drop=True)
    triad_table.trust_category.unique()
    return triad_table


#simply calculates the ttt, ttd, tdd, and ddd probabilities from triadTable and gives us the required probability
def printActual(triadTable):
    n_triads = len(triadTable)
    ttt_prob = 1
    ttd_prob=1
    tdd_prob=1
    ddd_prob=1
    for i in triadTable['trust_category']:
        if i =='TTT':
            ttt_prob+=1
        elif i=='TTD':
            ttd_prob+=1
        elif i=='TDD':
            tdd_prob+=1
        elif i=='DDD':
            ddd_prob+=1
    print("Actual distribution of TTT, TTD, TDD, and DDD are \n {}%,{}%,{}%,{}%".format(
                                                                    ((ttt_prob / n_triads)*100),
                                                                    ((ttd_prob / n_triads)*100),
                                                                    ((tdd_prob / n_triads)*100),
                                                                    ((ddd_prob / n_triads )*100)))

def printExpected(triadTable,probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4):
    ttt_prob =0
    ttd_prob =0
    tdd_prob =0
    ddd_prob =0
    for i in triadTable['trust_category']:
            if i =='TTT':
                ttt_prob+=1
            elif i=='TTD':
                ttd_prob+=1
            elif i=='TDD':
                tdd_prob+=1
            elif i=='DDD':
                ddd_prob+=1

    iterable=zip(
            (ttt_prob,    
            ttd_prob, 
            tdd_prob,    
            ddd_prob),
            (probability_for_type1,probability_for_type2,probability_for_type3,probability_for_type4))

    print("Expected distribution of TTT, TTD, TDD, and DDD triads are:\n")
    for i,x in iterable:
        print("number={}: percent={}%".format(i,x*100))
