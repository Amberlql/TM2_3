#Import packages
import numpy as np
from shapely.geometry import LineString, Point

def filter_planes(all_contours):
    """Filter out all planes that have no tumor contact"""
    all_contours_filtered = {}
    
    #Collect the planes for which the tumor has no contact i.e. the key 'tumor' is empty
    for plane in all_contours:
        for object_mesh in all_contours[plane]:
            if "tumor" in object_mesh:
                if not all_contours[plane][object_mesh].is_empty:
                    all_contours_filtered[plane] = all_contours[plane]
                    
    return all_contours_filtered
                    
def create_lines(per_degree):
    "Compute lines within 360 degrees per degree starting in the centroid of the vessel"
    # Parameters
    line_length = 10  # Length of each line segment in mm, this should be enough to reach the first intersection with the vessel and tumor

    # Arrays to store the x and y coordinates of the line endpoints
    x_start = []
    y_start = []
    x_end = []
    y_end = []

    # Generate lines every 1 degree around the centroid
    for angle in range(0, 360, per_degree):
        
        # Convert angle to radians
        theta = np.deg2rad(angle)
        
        # Calculate endpoint of the line segment
        x_endpoint = line_length * np.cos(theta)
        y_endpoint = line_length * np.sin(theta)
        
        # Store the coordinates
        x_start.append(0) #Since the centroid is always in at 0,0 due to the defenition of the planes coordinate system
        y_start.append(0) #Since the centroid is always in at 0,0 due to the defenition of the planes coordinate system
        x_end.append(x_endpoint)
        y_end.append(y_endpoint)
    
    #Initialize empty list for LineString objects
    lines=[]
    
    #Create linestring objects
    for i in range(len(x_start)):
        lines.append(LineString([[x_start[i], y_start[i]], [x_end[i], y_end[i]]]))
    
    return lines
    

def line_intersections(all_contours_filtered, per_degree):
    "Compute all intersection points per plane per line with all objects"
    
    #Initialize dictonary per plane
    all_intersections = {}

    for plane in all_contours_filtered:
        
        #Compute lines for the vessel
        lines = []
        centroid_vessel = Point(0, 0) #Since the centroid is always in at 0,0 due to the defenition of the planes coordinate system
        for object_mesh in all_contours_filtered[plane]:
            if not 'tumor' in object_mesh:
                lines = create_lines(per_degree)
        
        #Initialize dictionary per line
        intersection_per_line = {}
        
        #Compute the intersection points for every line for every object mesh in every plane 
        for i, line in enumerate(lines):
            
            #Initialize dictionary per object
            intersection_per_object_mesh = {}
            
            for object_mesh in all_contours_filtered[plane]:
                
                #Compute the intersections for every object mesh for every plane with a line
                line_intersection = line.intersection(all_contours_filtered[plane][object_mesh])
                
                if line_intersection.geom_type == 'Point':
                    
                    #Add to dictionary
                    intersection_per_object_mesh[object_mesh] = line_intersection
                    
                elif line_intersection.geom_type == 'MultiPoint':
                    point_1 = line_intersection.geoms[0]
                    point_2 = line_intersection.geoms[1]
                    distance_point_1 = centroid_vessel.distance(point_1)
                    distance_point_2 = centroid_vessel.distance(point_2)
                    
                    if distance_point_1 > distance_point_2: #only the closest point with the vessel matters
                        #Add to dictionary
                        intersection_per_object_mesh[object_mesh] = point_2 
                    else:
                        intersection_per_object_mesh[object_mesh] = point_1
                        
            #Add to dictionary
            intersection_per_line[f'line{i}'] = intersection_per_object_mesh
            
        #Add to main dictionary 
        all_intersections[plane] = intersection_per_line
        
    return all_intersections, lines
    