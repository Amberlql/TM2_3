#Import packages
import numpy as np


def calculate_distance(all_intersections):
    """
    Calculate the distances between the tumor and vessel in mm per plane per line.
    
    This function takes a dictionary of intersections, where each intersection represents the coordinates of 
    where the tumor and vessel intersectin with 360 degree of lines in a specific plane. It computes the distance 
    between the tumor and the vessel or each line on each plane. If no intersection with the tumor is found, 
    the distance is set to infinity.

    Parameters:
    all_intersections (dict): A dictionary where the first level keys are plane numbers the second level keys 
                              are line numbers, the third level are the object mesh names ('tumor', 'vessel', 
                              etc.) and the values are the coordinates of their intersection with the line in 
                              the specific plane.

    Returns:
    dict: A dictionary where the keys are plane identifiers, the values are dictionaries with line identifiers
          as keys and the computed distances (in mm) as values. If a line has no intersection with the tumor,
          the distance is set to infinity.
    """
    
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
            
            if len(points) > 1:
                distance = points[0].distance(points[1])
                distance_per_line[line] = distance
                
            elif len(points) > 0:
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
    all_distances_filtered = {}
    
    for plane in all_distances:
        for line in all_distances[plane]:
            if all_distances[plane][line] <= vessel_wall: 
                all_distances_filtered[plane] = all_distances[plane]
                break
        
    return all_distances_filtered