#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 02:55:29 2018

@author: sherlock
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import psycopg2 
import numpy as np
from geopy.distance import distance
import os

def load():
    if os.path.isfile('file.npy'):
        ways = np.load('file.npy')
        return ways
    else:
     save()


def save():
        conn = psycopg2.connect("host=localhost dbname=AI_ass user=postgres password=123")
        current = conn.cursor()
        current.execute("select ST_AsText(ST_Transform(ST_GeomFromText(ST_AsText(way),900913),4326)) As wgs_geom from planet_osm_line")
        all_paths = current.fetchall()
        #print(all_paths)
        path_list = []
        for path in all_paths:
            nodes = path[0][11:-1].split(',')
            nodes_list = []
            for node in nodes:
                coordinates = tuple(map(float,node.split()))
    
                #nodes_list += [coordinates]
                nodes_list.append(coordinates)
            #nodes_list = np.array(nodes_list)
            path_list.append(nodes_list)
        np.save('file.npy',path_list)
        #print(path_list)
        return np.array(path_list)


class Node():

    def __init__(self,xcoor,ycoor):
        self.coordinates = (xcoor,ycoor) ## latitude, longitude
        self.parent = None
        self.g_score = 0
        self.h_score = 0

    def __repr__(self):
        return str(self.coordinates)

def successors(current_position,all_paths):
    curr_present_in = []

    #print(all_paths[0])

    '''for idx,row in enumerate(all_paths):
        print(idx, row)
        if present(current_position, row):
            curr_present_in.append((idx,row.index(current_position)))
       '''      
    
    current_position.coordinates=(current_position.coordinates[0], current_position.coordinates[1])
    
    current_position.coordinates=(78.2937005720353, 17.1993392800056)
    
    #print(current_position.coordinates)
    
    #current_position.coordinates=(78.1909770514864, 16.9529632260631)
    
    curr_present_in = [(idx, row.index(current_position.coordinates)) for idx,row in enumerate(all_paths) if current_position.coordinates in row ] #saving (idx_row, idx_col)
   
    child_nodes = []
   
    #print(curr_present_in)

    for item in curr_present_in:
        if item[1]+1 < len(all_paths[item[0]]):
            child_nodes.append(all_paths[item[0]][item[1]+1])
        if item[1]-1 >= 0:
            child_nodes.append(all_paths[item[0]][item[1]-1])    
    return child_nodes



def heuristic(current, destination):
    current_coord = [current.coordinates[1], current.coordinates[0]]    # longitudes and latitudes
    destination_coord = [destination.coordinates[1], destination.coordinates[0]]
    return distance(current_coord, destination_coord).km

def isInList(node,lis):
    i=0
    for n in lis:
        if node.coordinates==n.coordinates:
            return i
        i+=1
    return -1


def A_Star(sourc, destination,all_paths):
    source = Node(sourc[0],sourc[1])
    destination = Node(destination[0], destination[1])
    open_list = []
    closed_list = []
    current = source
    current.g_score=0
    current.h_score=distance(source.coordinates,destination.coordinates).km
    open_list.append(source)
    
    i=0
    
    while open_list:
        i += 1
        current = min(open_list, key=lambda x: x.g_score + x.h_score)
        #open_list.remove(current)
        open_list.remove(current)
        closed_list.append(current)
        
        # finding the immediate neighbours

        successor = successors(current,all_paths)
   
        nodes=[]
        
        for node in successor:
            newNode=Node(node[0],node[1])
            newNode.parent=current
            nodes.append(newNode)        
        
        for node in nodes:
            # Condition 1: checking if it is the goal
            #print(node.coordinates, destination)
            if node.coordinates==destination.coordinates:
                print("reached destination")
                path = []
                while node.coordinates!=source.coordinates:
                    path.append(node.coordinates)
                    node = node.parent
                path.append(node)
                return path[::-1]
          
            current_coord = [current.coordinates[1], current.coordinates[0]]    # longitudes and latitudes
            node_coord = [node.coordinates[1], node.coordinates[0]]
            
            open_ind=isInList(node,open_list)
            close_ind=isInList(node,closed_list)
           
            #print(open_ind)
            #print(close_ind)
            
            if open_ind==-1 and close_ind==-1:
                node.g_score = current.g_score + distance(current_coord, node_coord).km
                node.h_score = heuristic(node, destination)
                node.parent = current
                open_list.append(node)
            elif close_ind==-1:
                check_g = current.g_score + distance(current_coord, node_coord).km
                if check_g < open_list[open_ind].g_score:
                    open_list[open_ind].g_score = check_g
                    open_list[open_ind].parent = current
             
                              
                
       ## END of while loop


if __name__ == '__main__':
    # Initialize the endpoints
    #source=Node(2,3)
    #source=(78.1902810368042, 16.9513236295984)
    source=(78.2291316457064, 17.2108921149703)
    #source=(78.4983,17.4399)
    #source = (78.33274719,  17.29257221)
    destination= (78.2937298571135, 17.2081390822869)
    #destination=(78.1882855192321, 16.9443068269725)
    #destination=(78.4294,17.2403)
    all_paths = save()
    path = A_Star(source,destination,all_paths)
    print(path)
    