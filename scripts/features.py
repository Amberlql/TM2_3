#Import packages
import numpy as np

def euclidian_distance(p1, p2):
    """This function calculates the eucledian distance between two three dimensional points"""
    return np.sqrt((p2[0] - p1[0])**2 + 
                (p2[1] - p1[1])**2 + 
                (p2[2] - p1[2])**2)


def feature_maximum_contact_length(all_distances_filtered, centerline_points):
    """Calcute the maximum contact length between the tumor and the vessel and provide the planes which contribute to 
    this maximum contact length"""
    
    # Initialize lists
    plane_numbers = []
   
    for plane in all_distances_filtered:
        if all(value == np.inf for value in all_distances_filtered[plane].values()):
            print(f'no contact in {plane}')
        else:
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
        
    # Select only the centerline points (origins of the planes in the global coordinate system)
    points = []
    for index in plane_numbers_longest_streak:
        points.append(centerline_points[index])
      
    points = [tuple(arr) for arr in points] #Convert to a list of tupples to use
    
    # Approximate the longest distance of contact in mm using the global coordinates of the center by adding the euclidean distances betweeen the points
    maximum_contact_length = 0
    
    for i in range(len(points) - 1):
        maximum_contact_length += euclidian_distance(points[i], points[i+1])

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
                if angle_degree >= minimum_degrees:
                    if line_list:
                        angle_dict[f'Angle_{angle_degree}_degrees'] = [line_list[0], line_list[-1]]  #Note that due to the counting of python you do not have to substract the first line
                
                angle_degree = 0
                line_list = []
        
        if angle_degree >= minimum_degrees:
            if line_list:
                angle_dict[f'Angle_{angle_degree}_degrees'] = [line_list[0], line_list[-1]]
                
        if angle_dict:
            all_angles[plane] = angle_dict
            
    return all_angles