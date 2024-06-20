#Import packages
import numpy as np

def calculate_distance(all_intersections):
    """Calculate the distances between the tumor and vessel in mm per plane per line"""
    
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
            
            if len(points) > 0:
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
    all_distances_filtered = {}
    
    for plane in all_distances:
        for line in all_distances[plane]:
            if all_distances[plane][line] <= vessel_wall: 
                all_distances_filtered[plane] = all_distances[plane]
                break
        
    return all_distances_filtered

def feature_maximum_contact_length(all_distances_filtered, slice_thickness):
    """Calcute the maximum contact length between the tumor and the vessel and provide the planes which contribute to 
    this maximum contact length"""
    
    # Initialize lists
    plane_numbers = []
    
    for plane in all_distances_filtered:
        plane_index = int((plane.split("plane")[1]))
        plane_numbers.append(plane_index)

    # Count the longest consecutive range
    longest_streak = 1
    current_streak = 1
    plane_numbers_current_streak = [plane_numbers[0]] #Since a range always starts at the first number
    plane_numbers_longest_streak = [] #Since a range always starts at the first number

    for i in range(1, len(plane_numbers)):
        
        #Check if the current number is one more then the previous
        if plane_numbers[i] == plane_numbers[i-1] + 1: 
            current_streak += 1
            plane_numbers_current_streak.append(plane_numbers[i])
        else:
            #Check if the current streak is longer than the longest streak, then replace the longest streak including plane numbers
            if current_streak > longest_streak:
                longest_streak = current_streak
                plane_numbers_longest_streak = plane_numbers_current_streak.copy()
            current_streak = 1
            plane_numbers_longest_streak = [plane_numbers[i]]
           
    # Update longest streak for last consecutive range
    if current_streak > longest_streak:
        longest_streak = current_streak
        plane_numbers_longest_streak = plane_numbers_current_streak.copy()
    
    # Calculate the longest distance of contact in mm
    maximum_contact_length = longest_streak * slice_thickness

    return maximum_contact_length, plane_numbers_longest_streak

def feature_angles(all_distances_filtered, per_degree, minimum_degrees):
    """Calculate the maximum angle for a given plane and safe the lines between which this angle is created"""
    
    #Initialize dictionary
    all_angles = {}
     
    for plane in all_distances_filtered:
        
        #Initialize dictionary and list to registrate per angle
        angle_dict = {}
        line_list = []
        
        #Initialize angle
        angle_degree = 0
        
        for line in all_distances_filtered[plane]:
            
            #Check if the distance between the tumor and the vessel is close enough to contribute to the angle
            if all_distances_filtered[plane][line] < np.inf:
                
                #If close enough, add that line to the total angle
                angle_degree += per_degree
                line_list.append(line)
                
            #If not close enough, close angle and check if it is larger than the set minimum degrees of interest
            else:
                if angle_degree < minimum_degrees:
                    angle_degree = 0
                    line_list = []
                
                #If larger than the st of minimum degrees of interest, safe in dictionary
                else:
                    angle_dict[f'Angle_{angle_degree - per_degree}_degrees'] = [line_list[0], line_list[-1]]
                    angle_degree = 0
                    line_list = []
                    
        all_angles[plane] = angle_dict
                
    return all_angles