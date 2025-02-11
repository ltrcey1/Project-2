#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:37:32 2021

@author: kendrick shepherd
"""

import sys

import Geometry_Operations as geom

# Determine the unknown bars next to this node
def UnknownBars(node):
    bars_to_node = node.bar
    my_unknown_bars = []
    for the_current_bar in bars_to_node:
        if the_current_bar.is_computed == False:
            my_unknown_bars.append(the_current_bar)
    return my_unknown_bars

# Determine if a node if "viable" or not
def NodeIsViable(node):
    my_unknown_bar=UnknownBars(node)
    if len(my_unknown_bar)>0 & len(my_unknown_bar)<=2:
        return True
    else: 
        return False
    
# Compute unknown force in bar due to sum of the
# forces in the x direction
def SumOfForcesInLocalX(node, local_x_bar):
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)
    x_sum=0
    #sum of external forces
    x_sum += node.GetNetXForce()*geom.CosineVectors(local_x_vector, [1,0])
    x_sum += node.GetNetYForce()*geom.CosineVectors(local_x_vector, [0,1])
    for Bar in node.bars:
        if Bar.is_computed == True:
            x_sum +=Bar.axial_load*geom.SineBars(local_x_bar, Bar)
    #calculate unknown force
    other_bar=-1*x_sum
    local_x_bar.axial_load = other_bar
    local_x_bar.is_computed == True
    return

# Compute unknown force in bar due to sum of the 
# forces in the y direction
def SumOfForcesInLocalY(node, unknown_bars):
    local_x_bar=unknown_bars[0]
    other_bar=unknown_bars[2]
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)
    y_sum=0
    #sum of external forces
    y_sum += node.GetNetXForce()*geom.SineVectors(local_x_vector, [1,0])
    y_sum += node.GetNetYForce()*geom.SineVectors(local_x_vector, [0,1])
    for Bar in node.bars:
        if Bar.is_computed == True:
            y_sum +=Bar.axial_load*geom.SineBars(local_x_bar, Bar)
    #calculate unknown force
    other_bar=-1*y_sum/geom.SineBars(local_x_bar, other_bar)
    unknown_bars.axial_load = other_bar
    unknown_bars.is_computed == True
    return
    return
    
# Perform the method of joints on the structure
def IterateUsingMethodOfJoints(nodes,bars):
    count=1
    contwhile = False
    for Bar in bars:
        if Bar.is_computed == False:
            contwhile = True
            break 
    while contwhile == True: 
        for node in nodes:
            if NodeIsViable()== True:
                unknown_bar = UnknownBars(node)
                if len(unknown_bar)==2:
                    SumOfForcesInLocalY(unknown_bar)
                local_x_bar = unknown_bar
                SumOfForcesInLocalX(local_x_bar)
        contwhile = False
        for Bar in bars:
            if Bar.is_computed == False:
                contwhile=True 
                break 
        if count <= len(nodes):
            count += 1
        else: 
            sys.exit("Infinite Loop")
    return