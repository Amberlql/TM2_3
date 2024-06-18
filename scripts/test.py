import trimesh
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

from visualization import create_plane_mesh, ObjectPlotter, ContourPlotter
from plane_intersections import intersection_plane_with_object, intersection_points_to_2d_array, intersection_plane_with_objects


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
    

class IntersectionLine:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.line = LineString([point1, point2])
        
    def intersection(self, line):
        intersection = self.line.intersection(line)
        
        if intersection.geom_type == 'Point':
            return intersection
        elif intersection.geom_type == 'MultiPoint':
            return intersection[0]
        
        return self.line.intersection(line)
    
    
def intersection_line_with_contour(line, contour):
    """ Calculate the intersection point between a line and a contour and return a list of the points in the intersection"""
    line_intersection = line.intersection(contour)
    
    line_intersection_points_list = []
    
    if line_intersection.geom_type == 'Point':
        line_intersection_points_list.append(line_intersection)
    elif line_intersection.geom_type == 'MultiPoint':
        for point in line_intersection.geoms:
            line_intersection_points_list.append(point)
    
    return line_intersection_points_list




def main():
    tumor_mesh, sma_mesh = test_load()
    # Add your code here to perform operations on tumor and sma objects

    plane_test = Plane(np.array([0,0,0]), np.array([0,1,0]))
    plane_mesh = plane_test.get_mesh()
    
    object_meshes = {
        "tumor": tumor_mesh,
        "sma": sma_mesh
    }
    
    
    # get intersection points for one plane with all objects
    intersection_points = intersection_plane_with_objects(object_meshes, np.array([0,0,0]), np.array([0,1,0]))

    
    # filter out the intersection points for the tumor and sma and reshape them to a 2D array
    contour_points_tumor = intersection_points_to_2d_array(intersection_points["tumor"])
    contour_points_sma = intersection_points_to_2d_array(intersection_points["sma"])
    
    # print(contour_points_tumor)
    
    # create a LineString object for the tumor and sma so we can calculate the intersection points
    contour_tumor = LineString(contour_points_tumor)
    contour_vessel = LineString(contour_points_sma)
    
    # test line intersection
    line = LineString([[0,0], [-10,0]])
    intersection_tumor = contour_tumor.intersection(line)
    intersection_vessel = contour_vessel.intersection(line)
    
    contour_plotter = ContourPlotter()
    contour_plotter.add_contour(contour_tumor, 'b')
    contour_plotter.add_contour(contour_vessel, 'r')
    contour_plotter.show()
    
    # plt.plot(contour_points_tumor[:,0], contour_points_tumor[:,1], 'b')
    # plt.plot(contour_points_sma[:,0], contour_points_sma[:,1], 'r')
    # plt.plot(line.xy[0], line.xy[1], 'b')
    # for point in intersection_tumor.geoms:
    #     plt.plot(point.xy[0], point.xy[1], 'go')
    # # plt.plot(intersection_tumor.xy[0], intersection_tumor.xy[1], 'go')
    # plt.plot(intersection_vessel.xy[0], intersection_vessel.xy[1], 'ro')
    # plt.show()
    
    
    
    # lines = []
    
    # i = 5
    
    # points = intersection_points[0][i,:,:]
    # print(points)
    
    # point1 = points[0,:]
    # point2 = points[1,:]
    
    # print(point1, point2)
    
    # line = LineString([point1, point2])
    # line2 = LineString([[0,0], [-5,0]])
    
    # result = line2.intersection(line)
    # print(result)
    
    # #plot the lines and the intersection point
    # print(line.coords.xy)
    # x,y = line.xy
    # print(x, y)
    # x2, y2 = line2.xy
    # plt.plot(x, y, color='blue')
    # plt.plot(x2, y2, color='red')
    # plt.show()
    
    
    
    # for obj in range(len(intersection_points)):
    #     for i in range(intersection_points[obj].shape[0]):
    #         plt.plot(intersection_points[obj][i,:,0], intersection_points[obj][i,:,2], 'ro')
        
    
    # plt.show()
    
    
    

    # plt.plot(intersection_points[0][:,1,0], intersection_points[0][:,1,2], 'ro')
    # plt.plot(intersection_points[0][:,0,0], intersection_points[0][:,0,2], 'ro')
    # plt.plot(intersection_points[1][:,1,0], intersection_points[1][:,1,2], 'bo')
    # plt.plot(intersection_points[1][:,0,0], intersection_points[1][:,0,2], 'bo')
    # plt.show()
    
    
    # object_plotter = ObjectPlotter()
    
    # object_plotter.add_mesh(sma.mesh)
    # object_plotter.add_mesh(tumor.mesh)
    # object_plotter.add_mesh(plane_mesh)
    # object_plotter.add_points(intersection_points[0])
    # object_plotter.add_points(intersection_points[1])
    # object_plotter.add_points(sma.centerline_points)
    
    # object_plotter.show()
    
    
    

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