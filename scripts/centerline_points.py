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

def centerline_straightcylinder(vessel_length, slice_thickness):
    """Compute the centerline of a straight cylinder"""
    
    p1 = np.array([0, (-(vessel_length/2)), 0]) 
    p2 = np.array([0, (vessel_length/2), 0])
    number_of_steps = vessel_length / slice_thickness
    
    #interpolate between p1 and p2 to create points on the centerline
    centerline_points = np.stack([np.linspace(i, j, int(number_of_steps)) for i,j in zip(p1, p2)], axis=1) 
    cylinder_normal = normal_straightcylinder(p1, p2)
    normal_points = np.full(centerline_points.shape, cylinder_normal)
    return centerline_points, normal_points


def centerline_case_3(number_of_slices):
    radius = 14
    arc_degrees = 110
    arc_radians = np.deg2rad(arc_degrees)
    
    # length of the arc
    arc_length = radius * arc_radians
    
    
    # Calculate angle increments
    theta_start = -arc_radians / 2
    theta_end = arc_radians / 2
    theta = np.linspace(theta_start, theta_end, n)

    # Calculate points on the circle
    points = np.array([(radius * np.cos(t), radius * np.sin(t)) for t in theta])


    # Calculate tangent vectors
    tangents = np.array([(-np.sin(t), np.cos(t)) for t in theta])

    # Normalize tangent vectors (though they're already unit vectors)
    tangents = tangents / np.linalg.norm(tangents, axis=1)[:, np.newaxis]
    
    # add row for z coordinate
    points = np.hstack([points, np.zeros((number_of_slices, 1))])
    tangents = np.hstack([tangents, np.zeros((number_of_slices, 1))])

    return points, tangents, arc_length