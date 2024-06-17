import numpy as np
from scipy.interpolate import splprep, splev


def centerline(vessel, resolution):
    # Sample points on the surface of the mesh
    sampled_points = vessel.sample(1000)
    
    # Fit a spline to the sampled points to get a smooth curve
    tck, u = splprep(sampled_points.T, s=0)
    
    # Define the resolution for the spline sampling
    u_fine = np.arange(0, 1, resolution / np.max(u))
    
    # Get the smoothed points along the spline
    smoothed_points = np.array(splev(u_fine, tck)).T
    
    # Approximate the centerline as the smoothed spline of the sampled points
    centerline_points = smoothed_points
    
    return centerline_points

