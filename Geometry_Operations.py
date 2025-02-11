#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:25:01 2021

@author: kendrick shepherd
"""

import math
import numpy as np
import sys

# length of the beam
def Length(bar):
    bar_node = bar.init_node
    bar_vec= BarNodeToVector(bar_node,bar)
    bar_length= VectorTwoNorm(bar_vec)
    return bar_length

# Find two norm (magnitude) of a vector
def VectorTwoNorm(vector):
    norm = 0
    for i in range(0,len(vector)):
        norm+= vector[i]**2
    return np.sqrt(norm)

# Find a shared node between two bars
def FindSharedNode(bar_1,bar_2):
    if (bar_1.init_node==bar_2.init_node):
        return bar_1.init_node
    elif (bar_1.end_node==bar_2.end_node):
        return bar_1.end_node
    elif (bar_1.end_node==bar_2.init_node):
        return bar_1.end_node
    elif (bar_1.init_node==bar_2.end_node):
        return bar_1.init_node
    else:
        sys.exit("The two input bars do not share a node")
    

# Given a bar and a node on that bar, find the other node
def FindOtherNode(node,bar):
    if(bar.init_node == node):
        return bar.end_node
    elif(bar.end_node == node):
        return bar.init_node
    else:
        sys.exit("the input node is not on the bar")


# Find a vector from input node (of the input bar) in the direction of the bar
def BarNodeToVector(origin_node,bar):
    other_node=FindOtherNode(origin_node,bar)
    origin_loc=origin_node.location
    other_loc=other_node.location
    vec=[other_loc[0]-origin_loc[0], other_loc[1]-origin_loc[1]]
    return vec

# Convert to bars that meet at a node into vectors pointing away from that node
def BarsToVectors(bar_1,bar_2):
    shared_node=FindSharedNode(bar_1, bar_2)
    vec_1=BarNodeToVector(shared_node, bar_1)
    vec_2=BarNodeToVector(shared_node, bar_2)
    return [vec_1, vec_2]

# Cross product of two vectors
def TwoDCrossProduct(vec1,vec2):
    cross_product=vec1[0]*vec2[1]-vec2[0]*vec1[1]
    return cross_product

# Dot product of two vectors
def DotProduct(vec1,vec2):
    dot_product=0
    for i in range(0,len(vec1)):
        dot_product = vec1[i]*vec2[i]+dot_product
    return dot_product

# Cosine of angle from local x vector direction to other vector
def CosineVectors(local_x_vec,other_vec):
    cos_vec = DotProduct(local_x_vec, other_vec)/(VectorTwoNorm(local_x_vec)*VectorTwoNorm(other_vec))
    return cos_vec

# Sine of angle from local x vector direction to other vector
def SineVectors(local_x_vec,other_vec):
    sin_vec = TwoDCrossProduct(local_x_vec, other_vec)/(VectorTwoNorm(local_x_vec)*VectorTwoNorm(other_vec))
    return sin_vec

# Cosine of angle from local x bar to the other bar
def CosineBars(local_x_bar,other_bar):
    vector1, vector2 = BarsToVectors(local_x_bar,other_bar)
    cosine=CosineVectors(vector1,vector2)
    return cosine

# Sine of angle from local x bar to the other bar
def SineBars(local_x_bar,other_bar):
    vector1, vector2 = BarsToVectors(local_x_bar, other_bar)
    sine=SineVectors(vector1, vector2)
    return sine