"""Welcome"""
#Import packages
import numpy as np
import trimesh
import matplotlib.pyplot as plt

#Import modules
from scripts.centerlinepoints import centerline

#Load data
"Here you can load all your mesh objects and provide them with a fitting name"
tumor = trimesh.load('models/tumor.STL')
sma = trimesh.load('models/SMA.STL')

#Define constant
resolution = 0.1 

# Compute the centerline 
centerline_points = centerline(sma, resolution)