import trimesh
import numpy as np

def intersection_plane_with_object(mesh, plane_origin, plane_normal):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return intersection points of this plane with the mesh-object"""
    intersection = trimesh.intersections.mesh_plane(
        mesh,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        return_faces=False
    )
    return intersection


def intersection_plane_with_objects(meshes, plane_origin, plane_normal):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return intersection points of this plane with multiple mesh-objects"""
    intersections_points = {}
    for mesh in meshes:
        intersection = intersection_plane_with_object(meshes[mesh], plane_origin, plane_normal)
        intersections_points[f"{mesh}"] = intersection
    
    return intersections_points

def intersection_points(meshes, plane_origins, plane_normals):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return a dictionary with for every plane the intersection points of this plane with multiple mesh-objects
    """
    intersection_points_per_object_per_plane = {}
    i=0
    for origin, normal in zip(plane_origins, plane_normals):
        intersection = intersection_plane_with_objects(meshes, origin, normal)
        intersection_points_per_object_per_plane[f"plane {i}"] = intersection
        i+=1
            
    return intersection_points_per_object_per_plane


def intersection_points_to_2d_array(intersection_points):
    """ Convert the intersection points to a 2D array"""
    reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    reshaped_intersection_points = np.delete(reshaped_intersection_points, 1, 1)
    return reshaped_intersection_points