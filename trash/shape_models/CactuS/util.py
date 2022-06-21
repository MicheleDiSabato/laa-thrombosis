import meshio
import os
import pathlib
import csv 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.image as mpimg

def from_geo_to_csv(geo_filename, csv_filename):
    '''
    Reads the .geo file and writes the points writte in the format "Point(..) = {..,..,..}" inside a csv.
    '''
    coordinates_on_template = []
    with open(os.getcwd() + os.sep + csv_filename , 'w') as fw:
        with open(os.getcwd() + os.sep + geo_filename) as f:
            for line in f:
                if line[:5] == 'Point':
                    temp = line.split('{')
                    num_string = temp[1].split('}')[0]
                    num_string = num_string.split(',')[:2]
                    if num_string[1][0] == ' ':
                        num_string[1] = num_string[1][1:]
                    if num_string[0][0] == ' ':
                        num_string[0] = num_string[0][1:]
                    num_string[0] = float(num_string[0])
                    num_string[1] = float(num_string[1])
                    fw.write(str(num_string[0]) + ',' + str(num_string[1]) + '\n')
    with open(os.getcwd() + os.sep + csv_filename) as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            coordinates_on_template.append([float(row[0]),float(row[1])])
    return coordinates_on_template


def apply_rbf(radial_basis, epsilon, n_control_points, coordinates, displacements, x, y, correct_inlet = True):
    '''
    Applies the rbf transformation to the points collected in containers x and y. If "correct_inlet" is True, then is modifies the points 
    which compose the inlet so that they all share the same x component (which is supposed to be zero). This is done since on the inlet
    a boundary condition needs to be imposed.
    '''
    S = np.zeros((n_control_points, n_control_points))
    for i in range(n_control_points):
        for j in range(n_control_points):
            S[i,j] = radial_basis( coordinates[i][0]-coordinates[j][0], coordinates[i][1]-coordinates[j][1], epsilon)

    W = np.linalg.solve(S,displacements)

    phi_x = x
    phi_y = y
    for i in range(n_control_points):
        t = radial_basis( x - coordinates[i][0], y - coordinates[i][1], epsilon )
        phi_x = phi_x +  W[i,0]*radial_basis( x - coordinates[i][0], y - coordinates[i][1], epsilon )
        phi_y = phi_y +  W[i,1]*radial_basis( x - coordinates[i][0], y - coordinates[i][1], epsilon )
    if correct_inlet:
        phi_x[x==0] = 0
        phi_x[0] = 0
        phi_x[1] = 0
        phi_y[0] = 0
        phi_y[1] = 1
        count = 0
        index = []
        for i in range(len(phi_x)):
            cond_right = phi_x[i] != 0
            cond_left = phi_y[i] == 1 or phi_y[i] == 0
            if cond_right:
                count += 1
                index.append(i)
            if not(cond_right) and cond_left:
                count += 1
                index.append(i)
        points_x = np.zeros((count,))
        points_y = np.zeros((count,))
        for i in range(count):
            points_x[i] = phi_x[index[i]]
            points_y[i] = phi_y[index[i]]
    else:
        points_x = phi_x
        points_y = phi_y

    return (points_x, points_y)

def write_geo(points_x, points_y, geo_filename):
    '''
    Writes a .geo file starting from the points whose x and y coordinates are stored in the 
    lists points_x, points_y. The .geo file is ready to be used to produce a .msh file.
    '''
    with open(os.getcwd() + os.sep + geo_filename, 'w') as f:
            s='1'
            f.write('ref1 = 0.02;\n\n')
            for i in range(len(points_x)):
                f.write('Point('+str(i+1)+') = {'+str(points_x[i])+','+str(points_y[i])+',0,ref1};\n')
            for i in range(len(points_x) - 1, 0, -1):
                s+=','+str(i+1)
            f.write('\n\nSpline(1)={'+s+'};\n')     
            f.write('Line(2)={'+str(2)+','+str(1)+'};\n')
            f.write('\nPhysical Curve(1) = {1};\nPhysical Curve(2) = {2};\nCurve Loop(1) = {1,2};\n')
            f.write('Plane Surface(1) = {1};\nField[2] = BoundaryLayer;\nField[2].CurvesList = {1};\nField[2].SizeFar = 1.5;\nField[2].Size = 0.008;')
            f.write('\nField[2].Ratio = 1.2;\nField[2].Thickness = .03;\nBoundaryLayer Field = 2;\nPhysical Surface(2) = {1};')
    return
    