import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh


def create_plane_mesh(origin, normal, plane_size=2.0):
    """
    Create a plane mesh with the given origin and normal.

    Parameters:
    - origin: A 3-element array-like representing the origin of the plane.
    - normal: A 3-element array-like representing the normal vector of the plane.
    - plane_size: The size of the plane (side length), default is 2.0.

    Returns:
    - plane_mesh: A trimesh.Trimesh object representing the plane mesh.
    """
    # Define the vertices of the plane in the local coordinate system (XY plane)
    half_size = plane_size / 2
    plane_vertices = np.array([
        [-half_size, -half_size, 0],  # Bottom-left
        [ half_size, -half_size, 0],  # Bottom-right
        [ half_size,  half_size, 0],  # Top-right
        [-half_size,  half_size, 0]   # Top-left
    ])

    # Define the faces of the plane (two triangles)
    plane_faces = np.array([
        [0, 1, 2],  # First triangle
        [0, 2, 3]   # Second triangle
    ])

    # Create the Trimesh object
    plane_mesh = trimesh.Trimesh(vertices=plane_vertices, faces=plane_faces)

    # Ensure the normal is a unit vector
    normal = normal / np.linalg.norm(normal)

    # Calculate the rotation matrix to align the Z-axis with the plane normal
    z_axis = np.array([0, 0, 1])
    if np.allclose(normal, z_axis):
        rotation_matrix = np.eye(4)
    else:
        rotation_axis = np.cross(z_axis, normal)
        rotation_angle = np.arccos(np.dot(z_axis, normal))
        rotation_matrix = trimesh.transformations.rotation_matrix(rotation_angle, rotation_axis)

    # Create the translation matrix to move the plane to the origin
    translation_matrix = trimesh.transformations.translation_matrix(origin)

    # Combine the rotation and translation into a single transformation matrix
    transformation_matrix = np.dot(translation_matrix, rotation_matrix)

    # Apply the combined transformation to the plane mesh
    plane_mesh.apply_transform(transformation_matrix)

    return plane_mesh

def plot_mesh(mesh):
    vertices = mesh.vertices
    faces = mesh.faces
    
    bounding_box = mesh.bounds
    x_min, y_min, z_min = bounding_box[0]
    x_max, y_max, z_max = bounding_box[1]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mesh_collection = Poly3DCollection(vertices[faces], alpha=0.1, edgecolor='k')

    # Add the collection to the axis
    ax.add_collection3d(mesh_collection)
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set the plot limits based on the original bounding box
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_zlim([z_min, z_max])

    # Show the plot
    plt.show()
    

def plot_multiple_meshes(meshes):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    bounding_box = meshes[0].bounds
    x_min, y_min, z_min = bounding_box[0]
    x_max, y_max, z_max = bounding_box[1]
    
    for mesh in meshes:
        vertices = mesh.vertices
        faces = mesh.faces
        mesh_collection = Poly3DCollection(vertices[faces], alpha=0.1, edgecolor='k')
        ax.add_collection3d(mesh_collection)
        
        bounding_box = mesh.bounds
        x_min = min(x_min, bounding_box[0][0])
        y_min = min(y_min, bounding_box[0][1])
        z_min = min(z_min, bounding_box[0][2])
        x_max = max(x_max, bounding_box[1][0])
        y_max = max(y_max, bounding_box[1][1])
        z_max = max(z_max, bounding_box[1][2])
        
        
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_zlim([z_min, z_max])
    # Show the plot
    plt.show()

