import trimesh
import matplotlib.pyplot as plt
import numpy as np

from visualization import create_plane_mesh, ObjectPlotter
from centerlinepoints import centerline
from intersections import intersection_plane_with_meshes


def test_load():
    tumor = trimesh.load('models/tumor.stl')
    sma = trimesh.load('models/SMA.stl')
    return tumor, sma


class Plane:
    def __init__(self, origin, normal):
        self.origin = origin
        self.normal = normal

    def get_mesh(self, plane_size=2.0):
        return create_plane_mesh(self.origin, self.normal, plane_size)



class Vessel:
    def __init__(self, mesh):
        self.mesh = mesh
        self.centerline_points = None
        self.slices = []
        
    def set_test_centerline(self):
        p1 = np.array([0, -15, 0])
        p2 = np.array([0, 15, 0])
        self.centerline_points = np.stack([np.linspace(i,j,21) for i,j in zip(p1,p2)],axis=1)
        


class Tumor:
    def __init__(self, mesh):
        self.mesh = mesh
        self.slices = []
    


def main():
    tumor_mesh, sma_mesh = test_load()
    # Add your code here to perform operations on tumor and sma objects

    tumor = Tumor(tumor_mesh)
    sma = Vessel(sma_mesh)
    
    sma.set_test_centerline()
    
    print(sma.centerline_points)
    
    plane_test = Plane(np.array([0,0,0]), np.array([0,1,0]))
    
    plane_mesh = plane_test.get_mesh()
    
    intersection_points = intersection_plane_with_meshes([tumor.mesh, sma.mesh], plane_test.normal, plane_test.origin)
    
    
    object_plotter = ObjectPlotter()
    
    object_plotter.add_mesh(sma.mesh)
    object_plotter.add_mesh(tumor.mesh)
    object_plotter.add_mesh(plane_mesh)
    object_plotter.add_points(intersection_points[0])
    object_plotter.add_points(intersection_points[1])
    object_plotter.add_points(sma.centerline_points)
    
    object_plotter.show()
    
    
    

    # Plot multiple meshes
    # plot_multiple_meshes([sma, tumor, plane_mesh])
    
    # centerline_points = centerline(sma, 0.001)
    
    # # Plot the centerline points in 3d
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(*centerline_points.T)
    # plt.show()
    
    
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