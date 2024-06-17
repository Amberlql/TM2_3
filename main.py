"""Welcome"""
#Import packages
import numpy as np
import trimesh
import matplotlib.pyplot as plt

#Import modules
from scripts.visualization import ObjectPlotter
from scripts.centerlinepoints import centerline_straightcylinder

#Load data
"Here you can load all your mesh objects and provide them with a fitting name"
tumor = trimesh.load('models/tumor.STL')
sma = trimesh.load('models/SMA.STL')

#Visualize case
object_plotter = ObjectPlotter()
object_plotter.add_object(sma, "r")
object_plotter.add_object(tumor, "y")

#Compute the centerline of the straight cylinder
centerline_points, normal_points = centerline_straightcylinder()
object_plotter.add_points(centerline_points, "m")

#Show plot
object_plotter.show()