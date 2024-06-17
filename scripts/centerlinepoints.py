import numpy as np
from scipy.interpolate import splprep, splev

def normal_straightcylinder(p1, p2):
    # Calculate the vector from p1 to p2
    vec = p2 - p1
    
    # Calculate the magnitude of the vector
    mag = np.linalg.norm(vec)
    
    # Check for zero magnitude (to avoid division by zero)
    if mag == 0:
        return np.zeros_like(vec)  # Return zero vector if points are identical
    
    # Normalize the vector
    cylinder_normal = vec / mag
    
    return cylinder_normal

def centerline_straightcylinder():
    n = 21 #number of points selected on centerline
    p1 = np.array([0, -15, 0]) #numbers known from mock data creation
    p2 = np.array([0, 15, 0]) #numbers known from mock data creation
    
    #interpolate 21 points between p1 and p2 to create points on the centerline
    centerline_points = np.stack([np.linspace(i, j, n) for i,j in zip(p1, p2)], axis=1) 
    cylinder_normal = normal_straightcylinder(p1, p2)
    normal_points = np.full(centerline_points.shape, cylinder_normal)
    return centerline_points, normal_points