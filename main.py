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
from scripts.features import calculate_distance, filter_distances, feature_maximum_contact_length, feature_angles

#Initialize global parameters
number_of_slices = 21 #Provide the number of slices, i.e. the resolution, in which you want to calculate the measumernts 
vessel_length = 30 #Provide the length of the segmented vessel in mm (to be measured in paraview)

per_degree = 2 #Degree of line segments
minimum_degrees = 10 #Provide a treshold of the minimum value of degrees between the vessel and the tumor that you are interested in
example_plane = 12 #Provide as integer
vessel_wall = 1.5 #Provide the largest wall thickness in mm of the CA, SMA, CHA, SM or PV

#Load data and add to the dictionary object_meshes
#Make sure you always name the tumor "tumor..."
#Make sure you give the vessels the name of the corresponding vessel
#DO NOT inmport any other structures then the vessels and the tumor
tumor = trimesh.load('models/tumor.STL')
sma = trimesh.load('models/SMA.STL')
object_meshes = {"tumor":tumor, "SMA":sma}

#Visualize object_meshes in a 3D visualization plot to get insight into the patient case
object_plotter = ObjectPlotter()
object_plotter.add_object(sma, color="r", alpha=0.7)
object_plotter.add_object(tumor, color="y", alpha=0.5)

#NOTE: ONLY FOR EXAPLE DATA: Compute the centerline of the straight cylinder
centerline_points, normal_points = centerline_straightcylinder(vessel_length, number_of_slices)
object_plotter.add_points(centerline_points, color="black")

#Compute intersection points with planes perpendicular to the direction of the centerline of a specific vessel
intersections_with_planes = intersection_planes_with_objects(object_meshes, centerline_points, normal_points)

#Visualize the example plane as mesh
mesh = create_plane_mesh(centerline_points[example_plane], normal_points[example_plane], plane_size=13)
object_plotter.add_object(mesh, color="b", alpha=0.3)
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
    if "tumor" in object_mesh:
        contourplotter.add_contour(plane_contour[object_mesh], color="y", linewidth=4)
    else:
        contourplotter.add_contour(plane_contour[object_mesh], color="r", linewidth=4)
for line in plane_intersection:
    for mesh in plane_intersection[line]:
        contourplotter.add_point(plane_intersection[line][mesh], color="b", marker="o", markersize=2)
        
#Vizualize the lines of 90, 180, 270 degrees
contourplotter.add_contour(lines[(int(90 / per_degree))], color="black", linestyle="--")
contourplotter.add_contour(lines[(int(180 / per_degree))], color='black', linestyle="--")
contourplotter.add_contour(lines[(int(270 / per_degree))], color='black', linestyle="--")
contourplotter.show()

#Compute distances per plane per line between the tumor and the vessel 
all_distances = calculate_distance(all_intersections)

#Filter distances to get the planes where there is at least one contact point
all_distances_filtered = filter_distances(all_distances, vessel_wall)

#Calculate the maximum contact length and provide in which planes this contact is made
maximum_contact_length, plane_numbers_maximum_contact_length = feature_maximum_contact_length(vessel_length, number_of_slices, all_distances_filtered)
print(f'The maximum contact length is {maximum_contact_length} and present in the following planes {plane_numbers_maximum_contact_length}')

#Calculate the angle of encasement of the tumor around the vessel
all_angles = feature_angles(all_distances_filtered, per_degree, minimum_degrees)
print(all_angles)
