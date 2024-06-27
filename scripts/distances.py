#Import packages
import numpy as np


def calculate_distance(all_intersections):
    """Calculate the distances between the tumor and vessel in mm per plane per line."""
    
    #Initialize dictonary per plane
    all_distances = {}
    
    for plane in all_intersections:
        
        #Initialize dictionary per line
        distance_per_line = {}
        
        for line in all_intersections[plane]:
            
            #Initialize list
            points = []
            
            #Filter only the lines that have an intersection with the tumor
            if 'tumor' in all_intersections[plane][line]:
                for object_mesh in all_intersections[plane][line]:
                    points.append(all_intersections[plane][line][object_mesh])
            
            if len(points) >= 2:
                distance = points[0].distance(points[1])
                distance_per_line[line] = distance
   
            else:
                distance_per_line[line] = np.inf #infinite value to show no intersection with the tumor
                
        #Add to dictionary
        all_distances[plane] = distance_per_line
    
    return all_distances


def filter_distances(all_distances, vessel_wall):
    """Filter the planes where at least on one of the lines the distance between the tumor and the vessel is smaller or equal to
    the vessel wall thickness set in the parameters in the main file"""
    
    #Initialize dictionary
    all_planes_filtered = {}
    
    #Add plane to dictionary if there is contact between the tumor and vessel at a certain point
    for plane in all_distances:
        for line in all_distances[plane]:
            if all_distances[plane][line] <= vessel_wall: 
                all_planes_filtered[plane] = all_distances[plane]
                break
            
    #Initialize dictionary
    all_distances_filtered = {}
            
    #Change line value in dictionary if for that line, the tumor is not close enough to the vessel to make contact
    for plane in all_planes_filtered:
        #Initialize dictionary
        all_lines_filtered = {}
        for line in all_planes_filtered[plane]:
            if all_planes_filtered[plane][line] <= vessel_wall: 
                all_lines_filtered[line] = all_planes_filtered[plane][line]
            else:
                all_lines_filtered[line] = np.inf
                
        all_distances_filtered[plane] = all_lines_filtered

    return all_distances_filtered