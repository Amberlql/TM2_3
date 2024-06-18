#Import packages
import trimesh

def intersection_plane_with_object(object_mesh, plane_origin, plane_normal):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return intersection points of this plane with the mesh-object"""
    intersection = trimesh.intersections.mesh_plane(
        object_mesh,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        return_faces=False
    )
    return intersection


def intersection_plane_with_objects(object_meshes, plane_origin, plane_normal):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return intersection points of this plane with multiple mesh-objects"""
    intersections_points = {}
    for object_mesh in object_meshes:
        intersection = intersection_plane_with_object(object_meshes[object_mesh], plane_origin, plane_normal)
        intersections_points[f"{object_mesh}"] = intersection
    
    return intersections_points

def intersection_planes_with_objects(object_meshes, plane_origins, plane_normals):
    """ Create an intersection plane perpendicular on the plane_normal with plane_origin. 
    Return a dictionary with for every plane the intersection points of this plane with multiple mesh-objects
    """
    intersection_points_per_object_per_plane = {}
    i=0
    for origin, normal in zip(plane_origins, plane_normals):
        intersection = intersection_plane_with_objects(object_meshes, origin, normal)
        intersection_points_per_object_per_plane[f"plane{i}"] = intersection
        i+=1
            
    return intersection_points_per_object_per_plane