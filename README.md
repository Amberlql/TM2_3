# TM2_3 Pancreatic Tumor Vascularization Quantification
This script quantifies the vascularization of pancreatic tumors using multiple hand-written modules. It involves loading object meshes of the tumor and vessels, creating contours based on the mesh cross-sectioned with a plane perpendicular to the direction of the vessel's centerline, and calculating maximum contact areas and angles of encasement based on line intersections with contours in 2D planes. The code is based on three mock cases, each representing different scenarios of tumor and vessel geometries.

## Author
Amber Liqui Lung

## Date
2024-06-24

## Getting Started

### Installation
To run the script, ensure you have the necessary packages installed:
- numpy (version 1.24.4)
- trimesh (version 4.1.1)
- shapely (version 2.0.4)
- matplotlib (version 3.8.4)

### Usage

1. Load Data and Setup Parameters:
Adjust parameters such as number_of_slices, per_degree, minimum_degrees, example_plane, and vessel_wall according to your requirements and the specific mock case chosen.

2. Initialize Data and Compute Centerline:
Load tumor and vessel meshes (*.STL) for the chosen mock case.
Compute the centerline of the vessel using functions like centerline_straightcylinder or centerline_case_3, depending on the mock case.

3. Create Planes, Compute Intersections, and Create Contours:
Compute intersection points of planes with object meshes.
Create contours from these intersection points to visualize the cross-sections.

4. Compute Lines, Intersections, Distances, and Filter:
Compute lines and intersection points for each line.
Calculate distances between tumor and vessel.
Filter distances based on vessel_wall thickness.

5. Calculate Maximum Contact Length and Angles of Encasement:
Determine the maximum contact length and angles of encasement between tumor and vessel based on filtered distances.

6. Visualize Results:
Visualize the 3D tumor and vessel meshes, intersection points, contours, and angles using matplotlib.

## Mock Cases
The script includes mock cases to simulate different scenarios of tumor and vessel geometries. Ensure you choose the appropriate case and adjust the data loading and computation accordingly.

### Case 1: Low Resolution, Straight Cylinder
Example files: case1_tumor.STL, case1_SMA.STL

### Case 2: High Resolution, Straight Cylinder, Rounded Tumor and smaller angle
Example files: case2_tumor.STL, case2_SMA.STL

### Case 3: Low Resolution, Curved Cylinder
Example files: case3_tumor.STL, case3_SMA.STL

## Notes
Certain parts of the code are hard-coded for the mock cases mentioned above. Adjustments may be necessary for different datasets or scenarios.
Ensure that the meshes (*.STL files) are correctly named and located in the models directory relative to the script.
