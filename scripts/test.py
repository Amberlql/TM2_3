import trimesh
import matplotlib.pyplot as plt
import numpy as np

from visualization import plot_mesh, plot_multiple_meshes, create_plane_mesh


def test_load():
    tumor = trimesh.load('models/tumor.stl')
    sma = trimesh.load('models/ader.stl')
    return tumor, sma


def main():
    tumor, sma = test_load()
    # Add your code here to perform operations on tumor and sma objects
    
    transformation_matrix = np.array([[1, 0, 0, 0],  # Translate along x by 1 unit
                                   [0, 1, 0, 0],  # Translate along y by 2 units
                                   [0, 0, 1, 0],  # Translate along z by 3 units
                                   [0, 0, 0, 1]])
    
    sma.apply_transform(transformation_matrix)
    
    plane_mesh = create_plane_mesh(np.array([10,10,0]), np.array([1,1,0]), plane_size=20)
    
    
    # Plot a single mesh
    # plot_mesh(tumor)
    
    # Plot multiple meshes
    plot_multiple_meshes([sma, tumor, plane_mesh])
    
    # isect, face_inds = trimesh.intersections.mesh_plane(
    # tumor,
    # plane_normal=(0,1,0),
    # plane_origin=(0,0,0),
    # return_faces=True
    # )
    
    # plt.scatter(*isect[:,0,0::2].T)
    # plt.show()

if __name__ == "__main__":
    main()