import numpy as np

def normal_straightcylinder(p1, p2):
    """Compute the normal of a straight cylinder"""
    
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

def centerline_straightcylinder(vessel_length, number_of_slices):
    """Compute the centerline of a straight cylinder"""
    
    p1 = np.array([0, (-(vessel_length/2)), 0]) 
    p2 = np.array([0, (vessel_length/2), 0])
    
    #interpolate 21 points between p1 and p2 to create points on the centerline
    centerline_points = np.stack([np.linspace(i, j, number_of_slices) for i,j in zip(p1, p2)], axis=1) 
    cylinder_normal = normal_straightcylinder(p1, p2)
    normal_points = np.full(centerline_points.shape, cylinder_normal)
    return centerline_points, normal_points