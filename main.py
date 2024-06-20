"""Welcome"""
# ============================================================
# Imports
# ============================================================

#Import packages
import numpy as np
import trimesh
import matplotlib.pyplot as plt

#Import modules
from scripts.visualization import ObjectPlotter, create_plane_mesh, ContourPlotter
from scripts.centerline_points import centerline_straightcylinder, centerline_case_3
from scripts.plane_intersections import intersection_planes_with_objects
from scripts.contour_creation import create_contour_from_intersection_points
from scripts.line_intersections import filter_planes, line_intersections
from scripts.features import calculate_distance, filter_distances, feature_maximum_contact_length, feature_angles

# ============================================================
# Initialization of global parameters
# ============================================================

vessel_length = 30 #Provide the length of the segmented vessel in mm (to be measured in paraview)
number_of_slices =  21 #Defines the resolution
per_degree = 3 #Degree of line segments
minimum_degrees = 10 #Provide a treshold of the minimum value of degrees between the vessel and the tumor that you are interested in
example_plane = 12 #Provide as integer
vessel_wall = 1.5 #Provide the largest wall thickness in mm of the CA, SMA, CHA, SM or PV

# ============================================================
# Load data
# ============================================================

#Load data and add to the dictionary object_meshes
#Make sure you always name the tumor "tumor..."
#Make sure you give the vessels the name of the corresponding vessel
#DO NOT inmport any other structures then the vessels and the tumor

# #Case 1: Low resolution, straight cylinder
# tumor = trimesh.load('models/case1_tumor.STL')
# sma = trimesh.load('models/case1_SMA.STL')
# object_meshes = {"tumor":tumor, "SMA":sma}

#Case 2: high resolution, straight cylinder, rounded tumor, slightly less angle then 180 degrees
# tumor = trimesh.load('models/case2_tumor.STL')
# tumor = trimesh.load('models/case2_tumor.STL')
# sma = trimesh.load('models/case2_SMA.STL')
# object_meshes = {"tumor":tumor, "SMA":sma}

#Case 3: low resolution, curved cylinder
tumor = trimesh.load('models/case3_tumor.STL')
sma = trimesh.load('models/case3_SMA.STL')
object_meshes = {"tumor":tumor, "SMA":sma}

#Visualize object_meshes in a 3D visualization plot to get insight into the patient case
object_plotter = ObjectPlotter()
object_plotter.add_object(sma, label="SMA", color="r", alpha=0.7)
object_plotter.add_object(tumor, label="tumor", color="y", alpha=0.5)

# ============================================================
# Compute centerline points and corresponding normals
# ============================================================
# slice_thickness = vessel_length / number_of_slices

# #NOTE: ONLY CASE 1 & 2: Compute the centerline of the straight cylinder
# centerline_points, normal_points = centerline_straightcylinder(vessel_length, slice_thickness)
# object_plotter.add_points(centerline_points, color="black")

#Case 3
centerline_points, normal_points, arc_length = centerline_case_3(number_of_slices)
slice_thicknes = arc_length / number_of_slices

# ============================================================
# Create planes, compute intersections and create contours
# ============================================================

#Compute intersection points with planes perpendicular to the direction of the centerline of a specific vessel
intersections_with_planes = intersection_planes_with_objects(object_meshes, centerline_points, normal_points)

#Add the example plane as mesh to the visualization
mesh = create_plane_mesh(centerline_points[example_plane], normal_points[example_plane], plane_size=13)
object_plotter.add_object(mesh, label="plane", color="b", alpha=0.3)

#Create contour per object mesh per plane from intersection points
all_contours = create_contour_from_intersection_points(intersections_with_planes, object_meshes, centerline_points, normal_points)

#Filter contours to only achieve the planes in which the tumor is present
all_contours_filtered = filter_planes(all_contours)

# ================================================================
# Create lines, compute intersections, calculate distances, filter 
# ================================================================

#Compute lines and intersection points for every line for every object in every plane
all_intersections, lines = line_intersections(all_contours_filtered, per_degree)

#Visualize intersection points for every line for every object a plane as example
contour_plotter = ContourPlotter()
plane_intersection = all_intersections[f'plane{example_plane}']
plane_contour = all_contours_filtered[f'plane{example_plane}']
for object_mesh in plane_contour:
    if "tumor" in object_mesh:
        count = 0 #in order to only add the label once to the legend
        for line in plane_contour[object_mesh].geoms:
            if count == 0:
                contour_plotter.add_contour(line, label="tumor", color="y", linewidth=4)
                count += 1
            else:
                contour_plotter.add_contour(line, color="y", linewidth=4)
    else:
        count == 0 #in order to only add the label once to the legend
        for line in plane_contour[object_mesh].geoms:
            if count == 0:
                contour_plotter.add_contour(line, label=(f'{object_mesh}'), color="r", linewidth=4)
                count += 1
            else:
                contour_plotter.add_contour(line, color="r", linewidth=4)
for line in plane_intersection:
    count = 0 #in order to only add one point to the legend
    for mesh in plane_intersection[line]:
        if count == 0:
            contour_plotter.add_point(plane_intersection[line][mesh], color="b", marker="o", markersize=2)
            count +=1
        else: 
            contour_plotter.add_point(plane_intersection[line][mesh], color="b", marker="o", markersize=2)
    
#Compute distances per plane per line between the tumor and the vessel 
all_distances = calculate_distance(all_intersections)

#Filter distances to get the planes where there is at least one contact point
all_distances_filtered = filter_distances(all_distances, vessel_wall)

# ================================================================
# Compute maximum contact length and angles of encasement 
# ================================================================

#Calculate the maximum contact length and provide in which planes this contact is made
maximum_contact_length, plane_numbers_maximum_contact_length = feature_maximum_contact_length(all_distances_filtered, slice_thickness)
print(f'The maximum contact length is {maximum_contact_length} and present in the following planes {plane_numbers_maximum_contact_length}')

#Calculate the angle of encasement of the tumor around the vessel
all_angles = feature_angles(all_distances_filtered, per_degree, minimum_degrees)

#Print angles per plane
for plane in all_angles:
    for angle in all_angles[plane]:
        print(f'An angle of encasement for {plane} is {angle.replace("_", " ")}')

#Visualize planes with given angle
for plane in all_angles:
    contour_plotter2 = ContourPlotter()
    contour = all_contours_filtered[plane]
    for object_mesh in plane_contour:
        if "tumor" in object_mesh:
            count = 0 #in order to only add the label once to the legend
            for line in plane_contour[object_mesh].geoms:
                if count == 0:
                    contour_plotter2.add_contour(line, label="tumor", color="y", linewidth=4)
                    count += 1
                else:
                    contour_plotter2.add_contour(line, color="y", linewidth=4)
        else:
            count = 0 #in order to only add the label once to the legend
            for line in plane_contour[object_mesh].geoms:
                if count == 0:
                    contour_plotter2.add_contour(line, label=(f'{object_mesh}'), color="r", linewidth=4)
                    count += 1
                else:
                    contour_plotter2.add_contour(line, color="r", linewidth=4)
    for angle in all_angles[plane]:
        first_line_number = all_angles[plane][angle][0]
        first_line_number = int(first_line_number[4:])
        second_line_number = all_angles[plane][angle][1]
        second_line_number = int(second_line_number[4:])
        contour_plotter2.add_contour(lines[first_line_number], color="black", linestyle="--")
        contour_plotter2.add_contour(lines[second_line_number], color="black", linestyle="--")
        title = f'{angle.replace("_", " ")} for {plane}' #Set title for the figure
        contour_plotter2.set_settings(title)

#Show all figures
title = "Visualizations of the mock-case with the 3D tumor and vessel mesh including an example 2D slice plane" #Set title for the figure
object_plotter.set_settings(title)
title = "Visualization of a 2D cross-sectional plane with and intersection points with all lines" #Set title of figure
contour_plotter.set_settings(title)
plt.show()
