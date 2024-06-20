# Import packages
import numpy as np
from shapely.geometry import LineString

# def intersection_points_to_2d_array(intersection_points):
#     """ Convert the intersection points to a 2D array --> ONLY FOR NORMAL IN Y DIRECTION"""
#     # Reshape from m,2,3 to m*2,3 to convert from a 2D to 3D array
#     reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    
#     # Delete the third dimension (which is zero, due to 2D planes)
#     reshaped_intersection_points = np.delete(reshaped_intersection_points, 1, 1)
    
#     return reshaped_intersection_points

def get_coordinate_frame_from_normal_and_points(normal, origin, points):
    normal = normal / np.linalg.norm(normal)
    
    # Choose an arbitrary vector that is not parallel to the normal
    # because points on the plane we can choose the first point as the arbitrary vector
    arbitrary_vector = points[0,:] - origin
    arbitrary_vector /= np.linalg.norm(arbitrary_vector)
    
    B1 = arbitrary_vector
    
    B2 = np.cross(normal, B1)
    B2 /= np.linalg.norm(B2)
    
    return B1, B2


def create_transformation_matrix(B1, B2, normal, origin):
    """create the transformation matrix from the basis coordinate system to the new coordinate system"""
    normal = normal / np.linalg.norm(normal)
    B1 = B1 / np.linalg.norm(B1)
    B2 = B2 / np.linalg.norm(B2)
    
    U = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    
    V = np.array([B1, B2, normal])
    V_inv = np.linalg.inv(V)
    
    Rotation_matrix = V_inv @ U
    
    T_u_v = np.eye(4)
    T_u_v[:3, :3] = Rotation_matrix
    T_u_v[:3, 3] = origin
    
    T_v_u = np.linalg.inv(T_u_v)
    
    return T_u_v, T_v_u


def transform_points_to_new_coordinate_system(points, T):
    points_ones = np.hstack([points, np.ones((points.shape[0], 1))])
    new_points = np.dot(T, points_ones.T).T
    
    return new_points[:,:3]


def intersection_points_to_2d_array(intersection_points, normal, origin):
    """ Convert the intersection points in the 3D space to the corresponding 2D points on the plane"""
    # first check if the points array is not empty
    if intersection_points.shape[0] == 0:
        return np.array([])
    
    
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # place all points below each other
    reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    
    # get the coordinate system of the plane
    B1, B2 = get_coordinate_frame_from_normal_and_points(normal, origin, reshaped_intersection_points)
    
    # create the transformation matrix
    T_to_global, T_to_plane = create_transformation_matrix(B1, B2, normal, origin)
    
    # transform the points to the new coordinate system
    transformed_points = transform_points_to_new_coordinate_system(reshaped_intersection_points, T_to_plane)
    
    # remove the zero z axis
    transformed_points = transformed_points[:, :2]
    
    return transformed_points


def create_contour_from_intersection_points(intersections_with_planes, object_meshes, normals, origins):
    """ Create a 2D contour from the intersection points of the object_meshes for every plane"""
    #Initialize dictonary per plane
    all_contours = {}

    for plane in intersections_with_planes:
        
        #Initialize dictionary per object_mesh
        contours_per_object_mesh = {}
        
        plane_index = plane.split("plane")[1]
        normal = normals[int(plane_index)]
        origin = origins[int(plane_index)]
        
        for object_mesh in object_meshes:
                
            #Filter out the intersection points for the tumor and sma and reshape them to a 2D array
            contour_points = intersection_points_to_2d_array(intersections_with_planes[plane][object_mesh], normal, origin)
            
            #Create a LineString object for the object_mesh so you can calculate the intersection points
            contour = LineString(contour_points)
            
            #Add to dictionary
            contours_per_object_mesh[object_mesh] = contour
        
        #Add to main dictionary 
        all_contours[plane] = contours_per_object_mesh
        
    return all_contours
