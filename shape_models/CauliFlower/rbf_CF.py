'''
Function that applies a radial basis function approach to create the Cauliflower mesh.

Algorithm:

1) Define the position of a suitable number of control points, i.e. we write a .geo file and compile
it, to get a .msh file, called original_template_*.geo and original_template_*.msh1

2) Write another .geo file (called modified_template_*.geo), positioning the control points to
match the final shape

3) Run a python file, which reads the two .geo and the .msh file, extracts the relevant information,
such as the location of the control points, and computes the shifts

4) The same python file then computes the weights of the shape model and applies the radial basis
function to all the points contained in original_template_*.msh

5) The same python file writes an entire .geo file (called [GEOMETRY_NAME].geo), containing the
coordinates of the points in the original_template_*.msh file, shifted according to the radial
basis function

6) Finally, we use GMSH to compile the [GEOMETRY_NAME].geo file just created and obtain the
corresponding [GEOMETRY_NAME].msh file, which will be uploaded into the FreeFemm++ code
'''

# Import libraries
import meshio
import os
import pathlib
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.image as mpimg
from util import from_geo_to_csv, apply_rbf, write_geo

# LOAD THE 1D .MSH FILE
this_dir = pathlib.Path(__file__).resolve().parent
filename = this_dir / 'original_template_CF.msh'
mesh = meshio.read(filename)
num_points = len(mesh.points[:,0]) # number of control points
x = mesh.points[:,0]
y = mesh.points[:,1]

# WRITE AND READ THE CONTROL POINTS ON THE TEMPLATE DOMAIN
coordinates_CF = from_geo_to_csv('original_template_CF.geo', 'template_control_points_CF.csv')
n_control_point_CF = len(coordinates_CF)

# transform into a matrix
coordinates_CF_matrix = np.zeros((n_control_point_CF,2))
for i in range(n_control_point_CF):
    coordinates_CF_matrix[i,0] = coordinates_CF[i][0]
    coordinates_CF_matrix[i,1] = coordinates_CF[i][1]

# WRITE AND READ THE NEW CONTROL POINTS (on the final mesh):
coordinates_modified_CF = from_geo_to_csv('modified_template_CF.geo', 'modified_control_points_CF.csv')
assert len(coordinates_modified_CF) == len(coordinates_CF)

displacements = np.zeros((n_control_point_CF, 2)) # contains the displacement of the control points from the template to the final mesh
with open('modified_control_points_CF.csv') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        displacements[index,0] = float(row[0]) - coordinates_CF[index][0]
        displacements[index,1] = float(row[1]) - coordinates_CF[index][1]

# coordinates_modified_CF = np.zeros((n_control_point_CF,2)) # contains the coordinates of the control points on the final mesh
# for index in range(n_control_point_CF):
#     coordinates_modified_CF[index,0] = coordinates_CF[index][0] + displacements[index,0]
#     coordinates_modified_CF[index,1] = coordinates_CF[index][1] + displacements[index,1]

# DEFINE THE RADIAL BASIS FUNCTIONS AND FIND THE BEST WEIGHTS:
def radial_basis_gaussian(x,y,epsilon):
     return np.exp( - (x**2 + y**2)*epsilon**2 )
def radial_basis_multiquadratic(x,y,epsilon):
    r = np.sqrt(x**2 + y**2)
    return np.sqrt(1+(epsilon*r)**2)
def radial_basis_inverse_quadratic(x,y,epsilon):
    r = np.sqrt(x**2 + y**2)
    return 1/(1+(epsilon*r)**2)
def radial_basis_polymorphic_line(x,y,k=2):
    r = np.sqrt(x**2 + y**2)
    return r**k
def radial_basis_log_polymorphic_line(x,y,k=2):
    r = np.sqrt(x**2 + y**2)
    return r**k * np.log(r)
epsilon = 6
radial_basis = radial_basis_inverse_quadratic

# apply radial basis functions and compute the weights
# apply_rbf()

points_x, points_y = apply_rbf(radial_basis, epsilon, n_control_point_CF, coordinates_CF, displacements, x, y, correct_inlet = True)

# WRITE THE ENTIRE FILE .GEO THAT NEEDS TO BE COMPILED INTO .MSH
write_geo(points_x, points_y, 'cauliflower.geo')
