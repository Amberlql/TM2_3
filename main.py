"""Welcome"""
#Import packages
import numpy as np
import trimesh
import matplotlib.pyplot as plt

#Import modules
from scripts.visualization import ObjectPlotter, create_plane_mesh
from scripts.centerlinepoints import centerline_straightcylinder
from scripts.plane_intersections import intersection_planes_with_objects

## Load data and add to the dictionary object_meshes
tumor = trimesh.load('models/tumor.STL')
sma = trimesh.load('models/SMA.STL')
object_meshes = {"tumor":tumor, "SMA":sma}

## Visualize object_meshes in a 3D visualization plot to get insight into the patient case
object_plotter = ObjectPlotter()
object_plotter.add_object(sma, "r")
object_plotter.add_object(tumor, "y")

## Compute the centerline of the straight cylinder
centerline_points, normal_points = centerline_straightcylinder()
object_plotter.add_points(centerline_points, "m")

## Compute intersection points with planes perpendicular to the direction of the centerline of a specific vessel
intersections = intersection_planes_with_objects(object_meshes, centerline_points, normal_points)

#visualize planes
for center, normal in zip(centerline_points, normal_points):
    mesh = create_plane_mesh(center, normal, plane_size=8.5)
    object_plotter.add_object(mesh, "b")
    
# #Show plot
# object_plotter.show()