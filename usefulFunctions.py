import warnings
warnings.simplefilter(action='ignore') #IGNORE ALL THE WARNINGS. I KNOW IT'S BAD BUT THERE ARE TOO MANY OF THEM

import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.animation as animation
import random
import time
import math
from geographiclib.geodesic import Geodesic

#Simplifications, good functions

def lat_to_km(lat1, lon1, lat2, lon2): #giving distance given the curvature of the Earth, earth_radius=6371009 change the value to km to get km.
    distance = ox.distance.great_circle_vec(lat1, lon1, lat2, lon2)
    return distance #in meters by default

def get_position_of_node(graph, node):
    """
    Get latitude and longitude given node ID
    :param graph: object: OGraph object from osm_request
    :param node:      graphml node ID
    :return position: array:    [latitude, longitude]
    """
    # note that the x and y coordinates of the graph.nodes are flipped
    # this is possibly an issue with the omnx graph.load_graphml method
    # a correction is to make the position tuple be (y, x) as below
    position = np.array([graph.nodes[node]['x'], graph.nodes[node]['y']])
    return position

def getAllNodesIDs(graph):
    nodesList = []
    for i in graph.nodes:
        nodesList.append(i)
    return nodesList

def find_cars(init_node, end_node, cars):
    print("Nothing so far")
