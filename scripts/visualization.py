import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh


class ObjectPlotter:
    """
    A class to plot 3D mesh objects using matplotlib.
    """
    
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.bounding_box = None
        self.x_min = None
        self.y_min = None
        self.z_min = None
        self.x_max = None
        self.y_max = None
        self.z_max = None
        
    def add_mesh(self, mesh):
        vertices = mesh.vertices
        faces = mesh.faces
        mesh_collection = Poly3DCollection(vertices[faces], alpha=0.1, edgecolor='k')
        self.ax.add_collection3d(mesh_collection)
        
        bounding_box = mesh.bounds
        if self.bounding_box is None:
            self.bounding_box = bounding_box
            self.x_min, self.y_min, self.z_min = bounding_box[0]
            self.x_max, self.y_max, self.z_max = bounding_box[1]
        else:
            self.x_min = min(self.x_min, bounding_box[0][0])
            self.y_min = min(self.y_min, bounding_box[0][1])
            self.z_min = min(self.z_min, bounding_box[0][2])
            self.x_max = max(self.x_max, bounding_box[1][0])
            self.y_max = max(self.y_max, bounding_box[1][1])
            self.z_max = max(self.z_max, bounding_box[1][2])
    
    def show(self):
        # Set labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.set_xlim([self.x_min, self.x_max])
        self.ax.set_ylim([self.y_min, self.y_max])
        self.ax.set_zlim([self.z_min, self.z_max])
        # Show the plot
        plt.show()
        
    def add_points(self, points):
        self.ax.scatter(*points.T)
        
    
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