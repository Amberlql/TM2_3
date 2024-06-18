"""Welcome"""
#Import packages
import numpy as np
import trimesh
import matplotlib.pyplot as plt

#Import modules
from scripts.visualization import ObjectPlotter, create_plane_mesh, ContourPlotter
from scripts.centerlinepoints import centerline_straightcylinder
from scripts.plane_intersections import intersection_planes_with_objects
from scripts.contour_creation import create_contour_from_intersection_points
from scripts.line_intersections import filter_planes, line_intersections

#Initialize global parameters
per_degree = 3 #Degree of line segments
example_plane = 12 #Provide as integer

#Load data and add to the dictionary object_meshes
#Make sure you always name the tumor "tumor..."
#Make sure you give the vessels the name of the corresponding vessel
#DO NOT inmport any other structures then the vessels and the tumor
tumor = trimesh.load('models/tumor.STL')
sma = trimesh.load('models/SMA.STL')
object_meshes = {"tumor":tumor, "SMA":sma}

#Visualize object_meshes in a 3D visualization plot to get insight into the patient case
object_plotter = ObjectPlotter()
object_plotter.add_object(sma, "r")
object_plotter.add_object(tumor, "y")

#NOTE: ONLY FOR EXAPLE DATA: Compute the centerline of the straight cylinder
centerline_points, normal_points = centerline_straightcylinder()
object_plotter.add_points(centerline_points, "m")

#Compute intersection points with planes perpendicular to the direction of the centerline of a specific vessel
intersections_with_planes = intersection_planes_with_objects(object_meshes, centerline_points, normal_points)

#Visualize the example plane as mesh
mesh = create_plane_mesh(centerline_points[example_plane], normal_points[example_plane], plane_size=8.5)
object_plotter.add_object(mesh, "b")
object_plotter.show()

#Create contour per object mesh per plane from intersection points
all_contours = create_contour_from_intersection_points(intersections_with_planes, object_meshes)

#Filter contours to only achieve the planes in which the tumor is present
all_contours_filtered = filter_planes(all_contours)

#Compute lines and intersection points for every line for every object in every plane
all_intersections, lines = line_intersections(all_contours_filtered, per_degree)

#Visualize intersection points for every line for every object a plane as example
contourplotter = ContourPlotter()
plane_intersection = all_intersections[f'plane{example_plane}']
plane_contour = all_contours_filtered[f'plane{example_plane}']
for object_mesh in plane_contour:
    contourplotter.add_contour(plane_contour[object_mesh], "r")
for line in plane_intersection:
    for mesh in plane_intersection[line]:
        contourplotter.add_point(plane_intersection[line][mesh], "b")
        
#Vizualize the lines of 90, 180, 270 degrees
contourplotter.add_contour(lines[30], 'black')
contourplotter.add_contour(lines[60], 'black')
contourplotter.add_contour(lines[90], 'black')
contourplotter.show()