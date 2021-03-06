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
import matplotlib.pyplot as plt

def create_graph(m,file):
    G=nx.Graph()
    
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
    f.close()
    return edge_map
    
def get_population_data(m,file):
    population_data=np.zeros(m)
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for node in reader:
        pop=int(node[0])
        population_data[counter]=pop
        counter=counter+1
    return population_data
    
def compute_population_score(m,k,population_ideal,population_data,districting):
    district_populations=np.zeros(k)
    for index in range(m):
        district_populations[int(districting[index])]+=population_data[index]
    pop_score=sum((district_populations-population_ideal)**2)
    return pop_score
    
def compute_compactness_score(m,k,area_data,perimeter_data,districting):
    return 0
    
    
def get_area_data(m,file):
    area_data=np.zeros(m)
    f = open(file)
    reader = csv.reader(f)
    counter=0
    for node in reader:
        area=int(node[0])
        area_data[counter]=area
        counter=counter+1
    return area_data
    
def get_perimeter_data(m_primal,file):
    perimeter_data=np.zeros((m_primal,m_primal))
    f = open(file)
    reader = csv.reader(f)
    for edge in reader:
        a=int(edge[0])
        b=int(edge[1])
        p=int(edge[2])
        perimeter_data[a][b]=p
        perimeter_data[b][a]=p
    return perimeter_data


if __name__ == '__main__':
    m=6
    k=2
    pop_ideal=m/float(k)
    G_dual=create_graph(m,"simple_graph_dual.csv") #first two columns of simple_graph_edge_map
    m_primal=10
    G_primal=create_graph(m_primal,"simple_graph_primal.csv") #last two columns of simple_graph_edge_map
    
    edge_map_0=create_edge_map(0,"simple_graph_edge_map.csv")
    edge_map_1=create_edge_map(1,"simple_graph_edge_map.csv")
    
    population_data=get_population_data(m,"simple_graph_population.csv")
    area_data=get_area_data(m,"simple_graph_area.csv")
    perimeter_data=get_perimeter_data(m_primal,"simple_graph_perimeter.csv")
    population_total=sum(population_data)
    population_ideal=population_total/float(k)
    
    boundary_nodes_primal=[0,1,2,3,4]

    print('primal')
    print(G_primal.edges())
    
    
    districtings=[]
    for node1 in boundary_nodes_primal:
        for node2 in boundary_nodes_primal:
            if node1<node2:
                #print('here a')
                #print(node1)
                #print(node2)
                simple_paths=list(nx.all_simple_paths(G_primal,node1,node2))
                for simple_path in simple_paths:
                    #print('here b')
                    #print(simple_path)
                    G2=G_dual.copy()
                    districting=np.zeros(m)
                    for index in range(len(simple_path)-1):
                        edge=(simple_path[index],simple_path[index+1])
                        #print(edge)
                        edge2=(edge_map_0[edge[0],edge[1]],edge_map_1[edge[0],edge[1]])
                        #print(edge2)
                        G2.remove_edge(edge2[0],edge2[1])
                    G2_districts=list(nx.connected_components(G2))
                    #print('here c')
                    #print(G2_districts)
                    for index in range(2):
                        for node in G2_districts[index]:
                            districting[node]=index
                    districtings.append(districting)
                    print('districting:')
                    print(districting)
                    
    for districting in districtings:
        score=compute_population_score(m,k,population_ideal,population_data,districting)
        print score
        score=compute_compactness_score(m,k,area_data,perimeter_data,districting)
        print score
    
    G_metagraph=nx.Graph()
    for i in range(len(districtings)):
        for j in range(len(districtings)):
            districting1=districtings[i]
            districting2=districtings[j]
            if max(abs(districting1-districting2))==1:
                G_metagraph.add_edge(i,j)
    nx.draw(G_metagraph)
    plt.draw()

        

 

     

