# Import packages
import numpy as np
from shapely.geometry import LineString

def intersection_points_to_2d_array(intersection_points):
    """ Convert the intersection points to a 2D array --> ONLY FOR NORMAL IN Y DIRECTION"""
    # Reshape from m,2,3 to m*2,3 to convert from a 2D to 3D array
    reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    
    # Delete the third dimension (which is zero, due to 2D planes)
    reshaped_intersection_points = np.delete(reshaped_intersection_points, 1, 1)
    
    return reshaped_intersection_points
   
def create_contour_from_intersection_points(intersections_with_planes, object_meshes):
    """ Create a 2D contour from the intersection points of the object_meshes for every plane"""
    #Initialize dictonary per plane
    all_contours = {}

    for plane in intersections_with_planes:
        
        #Initialize dictionary per object_mesh
        contours_per_object_mesh = {}
        
        for object_mesh in object_meshes:
                
            #Filter out the intersection points for the tumor and sma and reshape them to a 2D array
            contour_points = intersection_points_to_2d_array(intersections_with_planes[plane][object_mesh])
            
            #Create a LineString object for the object_mesh so you can calculate the intersection points
            contour = LineString(contour_points)
            
            #Add to dictionary
            contours_per_object_mesh[object_mesh] = contour
        
        #Add to main dictionary 
        all_contours[plane] = contours_per_object_mesh
        
    return all_contours
