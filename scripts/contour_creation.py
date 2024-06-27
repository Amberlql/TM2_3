# Import packages
import numpy as np
from shapely.geometry import LineString, MultiLineString

def get_coordinate_frame_from_normal_and_points(origin, normal, points):
    """Create coordinate basis vectors (x,y,z)"""
    
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # Choose an arbitrary vector that is not parallel to the normal
    # because points on the plane we can choose the first point as the arbitrary vector
    arbitrary_vector = points[0,:] - origin
    
    # Ensure arbitrary_vector is a unit vector and rename to basis vector 1
    arbitrary_vector /= np.linalg.norm(arbitrary_vector)
    B1 = arbitrary_vector
    
    # Cross product to obtain vector perpendicular to B1 and normal vector and name this the basis vector 2 
    B2 = np.cross(normal, B1)
    
    # Ensure B2 is a unit vector
    B2 /= np.linalg.norm(B2)
    
    return B1, B2


def create_transformation_matrix(B1, B2, origin, normal):
    """Create the transformation matrix from the basis coordinate system to the new coordinate system"""
    
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # Ensure B1 and B2 are unit vectors
    B1 = B1 / np.linalg.norm(B1)
    B2 = B2 / np.linalg.norm(B2)
    
    # Define the basis vectors of the global coordinate system
    U = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    
    # Define the basis vectors of the plane coordinate system
    V = np.array([B1, B2, normal])
    
    # Create rotation matrix based on the regular convention
    V_inv = np.linalg.inv(V)
    Rotation_matrix = V_inv @ U
    
    # Create homogenous transformation matrix from plane to global
    # r11  .  .   x 
    # .  r22  .   y
    # .   .  r33  z
    #  0  0   0   1
    T_u_v = np.eye(4)
    T_u_v[:3, :3] = Rotation_matrix
    T_u_v[:3, 3] = origin
    
    # Create homogenous transformation matrix from gobal to plane
    T_v_u = np.linalg.inv(T_u_v)
    
    return T_u_v, T_v_u


def transform_points_to_new_coordinate_system(points, T):
    """Transform points from one coordinate system to another based on transformation matrix T"""
    
    # Add padding to create 4x1 vector x, y, z, 1 in order to multiply with transformation matrix
    points_ones = np.hstack([points, np.ones((points.shape[0], 1))])
    
    # Execute dot product between the points of in the coordination system with the transformation matrix
    new_points = np.dot(T, points_ones.T).T
    
    # Return and delete 4th column to recreate 3x1 vector x, y, z
    return new_points[:,:3]


def intersection_points_to_2d_array(intersection_points, origin, normal):
    """ Convert the intersection points in the 3D space to the corresponding 2D points on the plane"""
    # First check if the points array is not empty
    if intersection_points.shape[0] == 0:
        return np.array([])
    
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # Place all points below each other in order to loop through
    reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    
    # Get the coordinate system of the plane based on the origin and corresponding normal
    B1, B2 = get_coordinate_frame_from_normal_and_points(origin, normal, reshaped_intersection_points)
    
    # Create the transformation matrix, only to plane is used to provide 2D representation
    T_to_global, T_to_plane = create_transformation_matrix(B1, B2, origin, normal)
    
    # Transform the points to the new coordinate system
    transformed_points = transform_points_to_new_coordinate_system(reshaped_intersection_points, T_to_plane)
    
    # Remove the zero z axis, since this is now zero
    transformed_points = transformed_points[:, :2]
    
    return transformed_points


def create_contour_from_intersection_points(intersections_with_planes, object_meshes, centerline_points, normal_points):
    """ Create a 2D contour from the intersection points of the object_meshes for every plane"""
    #Initialize dictonary per plane
    all_contours = {}

    for plane in intersections_with_planes:
        
        #Initialize dictionary per object_mesh
        contours_per_object_mesh = {}
        
        plane_index = plane.split("plane")[1]
        normal = normal_points[int(plane_index)]
        origin = centerline_points[int(plane_index)]
        
        for object_mesh in object_meshes:
                
            #Move points to 2D plane coordinate system
            contour_points = intersection_points_to_2d_array(intersections_with_planes[plane][object_mesh], origin, normal)
            
            #Initialize empty contour
            contour = MultiLineString([])
            
            #Check if there are intersections with the object_mesh
            if contour_points.shape[0] == 0:
                contours_per_object_mesh[object_mesh] = contour
                continue
            
            #Loop through the line segments and add them to the multile string
            for i in range(0, contour_points.shape[0], 2):
                contour = contour.union(LineString([contour_points[i], contour_points[i+1]]))
                
            #Add to dictionary
            contours_per_object_mesh[object_mesh] = contour
        
        #Add to main dictionary 
        all_contours[plane] = contours_per_object_mesh
        
    return all_contours
