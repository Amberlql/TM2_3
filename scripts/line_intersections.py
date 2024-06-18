#Import packages
import numpy as np
from shapely.geometry import LineString 

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
                    
def one_degree_lines():
    "Compute lines within 360 degrees per degree starting in the centroid of the vessel"
    # Parameters
    line_length_mm = 10  # Length of each line segment in mm, this should be enough to reach the first intersection with the vessel and tumor
    num_lines = 360  # Number of lines (one for each degree in a 360 degree angle)

    # Define the centroid of the cylinder (assuming it's at the origin)
    centroid = np.array([0, 0, 0])

# Arrays to store the x and y coordinates of the line endpoints
x_coords = []
y_coords = []

# Generate lines every 1 degree around the centroid
for angle in range(0, 360):
    # Convert angle to radians
    theta = np.deg2rad(angle)
    
    # Calculate endpoint of the line segment
    x_end = line_length_mm * np.cos(theta)
    y_end = line_length_mm * np.sin(theta)
    
    # Store the coordinates
    x_coords.append(x_end)
    y_coords.append(y_end)

# Return the x and y coordinates of the line endpoints
coordinates = np.column_stack((x_coords, y_coords))
print(coordinates)

# Optionally, plot the lines for visualization
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x_coords, y_coords, 'ro')  # Plot points at the line endpoints
for x, y in zip(x_coords, y_coords):
    ax.plot([centroid[0], x], [centroid[1], y], 'b')  # Plot line segments
    
    
    
    

def line_intersections(all_contours_filtered, object_meshes):
    "Compute all intersection points per plane per line with all objects"
    
    #Initialize dictonary per plane
    all_intersections = {}

    for plane in all_contours_filtered:
        
        #Initialize dictionary per object_mesh
        intersection_per_object_mesh = {}
        
        for object_mesh in object_meshes:
                
            #Compute the intersections for every object mesh for every plane with a line
            intersection_points = all_contours_filtered[plane][object_mesh](line)
            
            #Add to dictionary
            intersection_per_object_mesh[object_mesh] = intersection_points
        
        #Add to main dictionary 
        all_intersections[plane] = intersection_per_object_mesh
        
    return all_intersections
    