#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 10:56:22 2017

@author: christy
"""

import networkx as nx
import csv 
import sys
import numpy as np

def create_graph(m,file):
    G=nx.Graph()
    node_list=[i for i in range(m)]
    G.add_nodes_from(node_list)
    
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        G.add_edge(a,b,label=counter)
        counter=counter+1
    f.close()
    return G
    
def create_edge_map(index,file):
    edge_map=-1*np.ones((10,10))
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        c=int(edge[2])
        d=int(edge[3])
        if index==0:
            edge_map[c,d]=a
            edge_map[d,c]=a
        elif index==1:
            edge_map[c,d]=b
            edge_map[d,c]=b
    return edge_map


if __name__ == '__main__':
    m=6
    k=2
    pop_ideal=m/float(k)
    G_dual=create_graph(m,"simple_graph_dual.csv")
    m_primal=9
    G_primal=create_graph(m_primal,"simple_graph_primal.csv")
    
    edge_map_0=create_edge_map(0,"simple_graph_edge_map.csv")
    edge_map_1=create_edge_map(1,"simple_graph_edge_map.csv")
    
    boundary_nodes_primal=[0,1,2,3,4]

    print('primal')
    print(G_primal.edges())
    
    
    districtings=[]
    for node1 in boundary_nodes_primal:
        for node2 in boundary_nodes_primal:
            if node1<node2:
                print('here a')
                print(node1)
                print(node2)
                simple_paths=list(nx.all_simple_paths(G_primal,node1,node2))
                for simple_path in simple_paths:
                    print('here b')
                    print(simple_path)
                    G2=G_dual.copy()
                    districting=np.zeros(m)
                    for index in range(len(simple_path)-1):
                        edge=(simple_path[index],simple_path[index+1])
                        print(edge)
                        edge2=(edge_map_0[edge[0],edge[1]],edge_map_1[edge[0],edge[1]])
                        print(edge2)
                        G2.remove_edge(edge2[0],edge2[1])
                    G2_districts=list(nx.connected_components(G2))
                    print('here c')
                    print(G2_districts)
                    for k in range(2):
                        for node in G2_districts[k]:
                            districting[node]=k
                    districtings.append(districting)
                    print('districting:')
                    print(districting)
                    

        

 

     

