# original python code found at https://www.geeksforgeeks.org/hierholzers-algorithm-directed-graph/

import numpy as np
import sys
import random
import pandas as pd
from datetime import datetime

def printCircuit(adj):

    # adj represents the adjacency list of
    # the directed graph
    # edge_count represents the number of edges
    # emerging from a vertex
    # edge_weight represents the number of times the edge
    # is visited (starts at 0, +1 at each visit)
    edge_count = dict()
    edge_weight = dict()

    for i in adj.keys():

        # find the count of edges to keep track
        # of unused edges
        edge_count[i] = len(adj.get(i))
        edge_weight[i] = 0

    if len(adj) == 0:
        return # empty graph

    # Maintain a stack to keep vertices
    curr_path = []

    # vector to store final circuit
    circuit = []

    # start from any vertex
    curr_v = random.choice([x for x in graph_dict.keys()]) # Current vertex
    curr_path.append(curr_v)


    while len(curr_path):

        # If there's remaining edge
        if edge_count[curr_v]:

            # Push the vertex
            curr_path.append(curr_v)

            # choices of possible vertices
            next_v_choices = adj[curr_v]


            # if the current path is long enough (more than 2 vertices visited),
            # and the previous-previous vertex is among the choices,
            # do not consider this option (to avoid 180 turns).
            # There must be more than 1 choice
            if (len(curr_path) > 2) & (len(next_v_choices)>1):
                for v in next_v_choices:
                    if curr_path[-2] == v:
                        next_v_choices.remove(v)
                        #break

            # weight of all choices
            next_v_weights = [edge_weight[x] for x in next_v_choices]

            min_weight = min(next_v_weights)

            # ideally we chose the vertex with the smallest weight, i.e. that has been visited the least
            min_weight_idx = [i for i, x in enumerate(next_v_weights) if x == min_weight]
            # we chose one vertex randomly among those with minimum weight

            next_v = random.choice([next_v_choices[i] for i in min_weight_idx])

            # and remove that edge
            edge_count[curr_v] -= 1
            edge_weight[curr_v] += 1
            #adj[curr_v].remove(next_v)


            # Move to next vertex
            curr_v = next_v

        # back-track to find remaining circuit
        else:
            circuit.append(curr_v)

            # Back-tracking
            curr_v = curr_path[-1]
            curr_path.pop()

    # we've got the circuit, now print it in reverse
    directions = [circuit[-1]]
    for i in range(len(circuit) - 1, -1, -1):
        print(circuit[i], end = "")
        if directions[-1] != circuit[i]:
            directions.append(circuit[i])
        if i:
            print(" -> ", end = "")


    return directions


if __name__ == "__main__":

    file_in = sys.argv[1]
    graph_csv = pd.read_csv(file_in, sep = ';')
    graph_csv['connections'] = graph_csv['connections'].apply(lambda x : [int(i) for i in x.split(',')])
    graph_dict = dict(zip(graph_csv['edge'], graph_csv['connections']))

    directions = printCircuit(graph_dict)
    print() # print solution in terms of labels of vertices


# xy coordinates of the vertices in EPSG:4326 are stored in the following csv file
coors = pd.read_csv('data/sion_nodes_XY.csv')

now = datetime.now()
dt_string = now.strftime("-%Y%m%d-%H%M%S-")

# export the list of coordinates -> copy-paste in a web mapping service such as Google Maps or Bing Maps
with open(file_in.replace('.csv','') + dt_string + 'directions.txt','w') as f:
    for stop in directions:
        f.write('%f, %f\n' % (coors[coors['id'] == stop]['Y'], coors[coors['id'] == stop]['X']))
