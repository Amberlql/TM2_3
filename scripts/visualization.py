import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh

class ObjectPlotter:
    """
    A class to plot 3D mesh objects using matplotlib.
    """
    
    def __init__(self):
        """ Initialization of plotter """
        self.fig = plt.figure() #Create figure
        self.ax = self.fig.add_subplot(111, projection='3d') #Add 3D subplot
        
    def add_object(self, mesh, **kwargs):
        """ Add mesh object """
        #Add mesh-object to the plot
        vertices = mesh.vertices
        faces = mesh.faces
        mesh_collection = Poly3DCollection(vertices[faces], **kwargs)
        self.ax.add_collection3d(mesh_collection)
        
    def add_points(self, points, **kwargs):
        """
        Adds array of 3D points to plot
        """
        self.ax.scatter(*points.T, **kwargs)
        
    def set_settings(self, title):
        """Set settings of the plot"""
        # Set title
        self.ax.set_title(title)
        
        # Set labels
        self.ax.set_xlabel('X [mm]')
        self.ax.set_ylabel('Y [mm]')
        self.ax.set_zlabel('Z [mm]')
        
         # Scale axis equal
        self.ax.axis("equal")
        
        # Add legend
        self.ax.legend()
    
class ContourPlotter:
    """Add contours to a 2D plot to visualize them"""
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.contours = []
        
    def add_contour(self, contour, **kwargs):
        """Add contour to plot"""
        self.contours.append(contour)
        self.ax.plot(contour.xy[0], contour.xy[1], **kwargs)
    
    def add_point(self, point, **kwargs):
        """Add point to plot"""
        self.ax.plot(point.x, point.y, **kwargs)
        
    def set_settings(self, title):
        """Set settings of the plot"""
        # Set title
        self.ax.set_title(title)

        # Set labels
        self.ax.set_xlabel('X [mm]')
        self.ax.set_ylabel('Y [mm]')

        # Scale axis equal
        self.ax.axis("equal")

        # Add legend
        self.ax.legend()
    
        
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


