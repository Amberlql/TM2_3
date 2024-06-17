import trimesh

def intersection_plane_with_mesh(mesh, plane_normal, plane_origin):
    isect = trimesh.intersections.mesh_plane(
        mesh,
        plane_normal=plane_normal,
        plane_origin=plane_origin,
        return_faces=False
    )
    return isect


def intersection_plane_with_meshes(meshes, plane_normal, plane_origin):
    intersections_points = []
    for mesh in meshes:
        isect = intersection_plane_with_mesh(mesh, plane_normal, plane_origin)
        intersections_points.append(isect)
    
    return intersections_points