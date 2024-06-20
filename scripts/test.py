import trimesh
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

from visualization import create_plane_mesh, ObjectPlotter, ContourPlotter
from plane_intersections import intersection_plane_with_objects
from contour_creation import intersection_points_to_2d_array


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


def distance_between_points(point1, point2):
    distance = point1.distance(point2)
    return distance



def transform_to_2d(points, origin, normal):
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # Choose an arbitrary vector that is not parallel to the normal
    # because points on the plane we can choose the first point as the arbitrary vector
    arbitrary_vector = points[0,:] - origin
    arbitrary_vector /= np.linalg.norm(arbitrary_vector)
    
    B1 = arbitrary_vector
    
    B2 = np.cross(normal, B1)
    B2 /= np.linalg.norm(B2)
    
    # Transform each point to 2D
    transformed_points = []
    for i in range(points.shape[0]):
        translated_point = points[i,:] - origin
        x = np.dot(translated_point, B1)
        y = np.dot(translated_point, B2)
        transformed_points.append([x, y])
    
    return np.array(transformed_points), B1, B2


def transform_to_3d(points_2d, origin, B1, B2):
    # Transform each 2D point back to 3D
    transformed_points_3d = []
    for point in points_2d:
        x, y = point
        point_3d = origin + x * B1 + y * B2
        transformed_points_3d.append(point_3d)
    
    return np.array(transformed_points_3d)


def test_transform_to_2d(normal, origin, points):
    transformed_points, B1, B2 = transform_to_2d(points, origin, normal)
    transformed_points_3d = transform_to_3d(transformed_points, origin, B1, B2)
    
    return transformed_points, transformed_points_3d


def get_coordinate_frame_from_normal_and_points(normal, origin, points):
    normal = normal / np.linalg.norm(normal)
    
    # Choose an arbitrary vector that is not parallel to the normal
    # because points on the plane we can choose the first point as the arbitrary vector
    arbitrary_vector = points[0,:] - origin
    arbitrary_vector /= np.linalg.norm(arbitrary_vector)
    
    B1 = arbitrary_vector
    
    B2 = np.cross(normal, B1)
    B2 /= np.linalg.norm(B2)
    
    return B1, B2


def create_transformation_matrix(B1, B2, normal, origin):
    """create the transformation matrix from the basis coordinate system to the new coordinate system"""
    normal = normal / np.linalg.norm(normal)
    B1 = B1 / np.linalg.norm(B1)
    B2 = B2 / np.linalg.norm(B2)
    
    U = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    
    V = np.array([B1, B2, normal])
    V_inv = np.linalg.inv(V)
    
    Rotation_matrix = V_inv @ U
    
    T_u_v = np.eye(4)
    T_u_v[:3, :3] = Rotation_matrix
    T_u_v[:3, 3] = origin
    
    T_v_u = np.linalg.inv(T_u_v)
    
    return T_u_v, T_v_u


def transform_points_to_new_coordinate_system(points, T):
    points_ones = np.hstack([points, np.ones((points.shape[0], 1))])
    new_points = np.dot(T, points_ones.T).T
    
    return new_points[:,:3]


def intersection_points_to_2d_array(intersection_points, normal, origin):
    """ Convert the intersection points in the 3D space to the corresponding 2D points on the plane"""
    # Ensure normal is a unit vector
    normal = normal / np.linalg.norm(normal)
    
    # place all points below each other
    reshaped_intersection_points = intersection_points.reshape(intersection_points.shape[0]*2, 3)
    
    # get the coordinate system of the plane
    B1, B2 = get_coordinate_frame_from_normal_and_points(normal, origin, reshaped_intersection_points)
    
    # transform the points to the new coordinate system
    transformed_points = transform_points_to_new_coordinate_system(reshaped_intersection_points, B1, B2, normal, origin)
    
    # remove the zero z axis
    transformed_points = transformed_points[:, :2]
    
    return transformed_points
    


def main():
    test = "plane10"
    
    print(int(test.split("plane")[1]))
    
    tumor_mesh, sma_mesh = test_load()
    # Add your code here to perform operations on tumor and sma objects
    
    normal = np.array([1,1,0])
    origin = np.array([1,1,1])

    plane_test = Plane(origin, normal)
    plane_mesh = plane_test.get_mesh(plane_size=20.0)
    
    object_meshes = {
        "tumor": tumor_mesh,
        "sma": sma_mesh
    }
    
    # object_plotter = ObjectPlotter()
    # object_plotter.add_object(sma_mesh, color='r', alpha=0.7)
    # object_plotter.add_object(tumor_mesh, color='y', alpha=0.5)
    # object_plotter.add_object(plane_mesh, color='b', alpha=0.3)
    # object_plotter.show()
    
    
    # get intersection points for one plane with all objects
    intersection_points = intersection_plane_with_objects(object_meshes, origin, normal)
    
    intersection_points_tumor = intersection_points["tumor"]    
    # Reshape from m,2,3 to m*2,3 to convert from a 2D to 3D array
    reshaped_intersection_points = intersection_points_tumor.reshape(intersection_points_tumor.shape[0]*2, 3)
    
    print(reshaped_intersection_points.shape)
    
    print(reshaped_intersection_points[:5, :])
    
    B1, B2 = get_coordinate_frame_from_normal_and_points(normal, origin, reshaped_intersection_points)
    
    T_u_v, T_v_u = create_transformation_matrix(B1, B2, normal, origin)
    
    transformed_points = transform_points_to_new_coordinate_system(reshaped_intersection_points, T_v_u)
    
    print(transformed_points.shape)
    
    print(transformed_points[:5, :])
    
    # transform back to 3d
    transformed_points_back = transform_points_to_new_coordinate_system(transformed_points, T_u_v)
    
    print(transformed_points_back[:5, :])
    
    print(transformed_points_back.shape)
    
    # plot the points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*reshaped_intersection_points.T, marker='o', color='r')
    ax.scatter(*transformed_points.T)
    ax.scatter(*transformed_points_back.T)
    plt.show()
    
    # print(reshaped_intersection_points[:5, :])
    # transformed_points, B1, B2 = transform_to_2d(reshaped_intersection_points, origin, normal)
    
    # # plot the 2d points
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(*transformed_points.T[:5, :])
    # plt.show()
    
    # print(transformed_points[:5, :])
    # transformed_points_3d = transform_to_3d(transformed_points, origin, B1, B2)
    
    # print(transformed_points_3d[:5, :])
    
    # # basis coordinate system
    # U = np.array([[1,0,0],
    #               [0,1,0],
    #               [0,0,1]])
    
    # V = np.array([B1, B2, normal])
    # V_inv = np.linalg.inv(V)
    
    # Rotation_matrix = V_inv @ U
    
    # T_u_v = np.eye(4)
    # T_u_v[:3, :3] = Rotation_matrix
    # T_u_v[:3, 3] = origin
    
    # T_v_u = np.linalg.inv(T_u_v)

    
    # transformed_points_3d_ones = np.hstack([transformed_points_3d, np.ones((transformed_points_3d.shape[0], 1))])
    
    # final_points = np.dot(T_v_u, transformed_points_3d_ones.T).T
    
    # print(final_points[:5, :])
    
    
    
    
    # # plot the basis vectors in 3d
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.quiver(*origin, *B1, color='r')
    # ax.quiver(*origin, *B2, color='g')
    # ax.quiver(*origin, *normal, color='b')
    
    # # add original coordinate system
    # ax.quiver(0,0,0,1,0,0, color='r')
    # ax.quiver(0,0,0,0,1,0, color='g')
    # ax.quiver(0,0,0,0,0,1, color='b')
    
    # # plot the transformed points
    
    # ax.scatter(*transformed_points.T, color='b')
    # ax.scatter(*transformed_points_3d.T, color='r')
    
    # final_points_plot = final_points[:5, :3]
    # ax.scatter(*final_points_plot.T, color='g')
    
    
    # plt.show()
    
    
    
    
    # # filter out the intersection points for the tumor and sma and reshape them to a 2D array
    # contour_points_tumor = intersection_points_to_2d_array(intersection_points["tumor"])
    # contour_points_sma = intersection_points_to_2d_array(intersection_points["sma"])
    
    
    # # print(contour_points_tumor)
    
    # # create a LineString object for the tumor and sma so we can calculate the intersection points
    # contour_tumor = LineString(contour_points_tumor)
    # contour_vessel = LineString(contour_points_sma)
    
    # contour_centroid = contour_vessel.centroid
    
    # # test line intersection
    # line = LineString([[0,0], [-10,0]])
    # intersection_tumor = contour_tumor.intersection(line)
    # intersection_vessel = contour_vessel.intersection(line)
    
    # contour_plotter = ContourPlotter()
    # contour_plotter.add_contour(contour_tumor, color='b')
    # contour_plotter.add_contour(contour_vessel, color='r')
    # contour_plotter.add_point(contour_centroid, color='g', marker='o')
    # contour_plotter.show()
    
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