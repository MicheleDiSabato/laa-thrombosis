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
filename = this_dir / 'original_template_CS.msh'
mesh = meshio.read(filename)
num_points = len(mesh.points[:,0]) # number of control points
x = mesh.points[:,0]
y = mesh.points[:,1]

# READ AND WRITE THE CONTROL POINTS ON THE TEMPLATE DOMAIN
coordinates_CS = from_geo_to_csv('original_template_CS.geo', 'template_control_points_CS.csv')
n_control_point_CS = len(coordinates_CS)

# transform into a matrix
coordinates_CS_matrix = np.zeros((n_control_point_CS,2))
for i in range(n_control_point_CS):
    coordinates_CS_matrix[i,0] = coordinates_CS[i][0]
    coordinates_CS_matrix[i,1] = coordinates_CS[i][1]

# READ AND WRITE THE NEW CONTROL POINTS (on the final mesh):
coordinates_modified_CS = from_geo_to_csv('modified_template_CS.geo', 'modified_control_points_CS.csv')
assert len(coordinates_modified_CS) == len(coordinates_CS)

displacements = np.zeros((n_control_point_CS, 2)) # contains the displacement of the control points from the template to the final mesh
with open('modified_control_points_CS.csv') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        displacements[index,0] = float(row[0]) - coordinates_CS[index][0]
        displacements[index,1] = float(row[1]) - coordinates_CS[index][1]

# coordinates_modified_CS = np.zeros((n_control_point_CS,2)) # contains the coordinates of the control points on the final mesh
# for index in range(n_control_point_CS):
#     coordinates_modified_CS[index,0] = coordinates_CS[index][0] + displacements[index,0]
#     coordinates_modified_CS[index,1] = coordinates_CS[index][1] + displacements[index,1]

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
epsilon = 5
radial_basis = radial_basis_multiquadratic

# apply radial basis functions and compute the weights
points_x, points_y = apply_rbf(radial_basis, epsilon, n_control_point_CS, coordinates_CS, displacements, x, y, correct_inlet = True)

# WRITE THE ENTIRE FILE .GEO THAT NEEDS TO BE COMPILED INTO .MSH
write_geo(points_x, points_y, 'cactus.geo')