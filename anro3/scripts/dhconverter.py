#! /usr/bin/python

import json
from tf.transformations import *

xaxis,zaxis = (1, 0, 0),(0, 0, 1)
def convertToFile():
    with open('../yaml/dh.json', 'r') as file:
        param = json.loads(file.read())

    with open('../yaml/urdf.yaml', 'w') as file:
        for key in param.keys():
            a, d, alpha, th = param[key]    #parametry w notacji DH
            a=float(a)
            d=float(d)
            alpha=float(alpha)
            th=float(th)

            tz = translation_matrix((0, 0, d))  #macierz translacji wzdluz osi z i-1
            rz = rotation_matrix(th, zaxis)     #macierz obrotu wokol osi z i-1
            tx = translation_matrix((a, 0, 0))  #macierz translacji wzdluz osi x i
            rx = rotation_matrix(alpha, xaxis)  #macierz obrotu wokol osi x i

            matrix = concatenate_matrices(tz, rz, tx, rx)  #macierz,bedaca wynikiem wymnozenia poszczegolnych macierzy

            rpy = euler_from_matrix(matrix)
            xyz = translation_from_matrix(matrix)

            file.write(key + ":\n")
            file.write("  j_xyz: {} {} {}\n".format(*xyz))
            file.write("  j_rpy: {} {} {}\n".format(*rpy))
            file.write("  l_xyz: {} 0 0\n".format(xyz[0] / 2))
            file.write("  l_rpy: 0 0 0\n")
            file.write("  l_len: {}\n".format(a))
if __name__ == '__main__':
    param = {}
    results = ''
    convertToFile()
