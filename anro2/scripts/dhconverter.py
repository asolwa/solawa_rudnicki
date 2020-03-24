#!/usr/bin/env python
import json

def convertToFile():
	parameters={}
	with open('../yaml/dh.json','r') as file:
		parameters=json.loads(file.read())
	with open('../yaml/urdf.yaml','w') as file:
		for key in parameters.keys():
			a,d,alpha,th= parameters[key]
			a=float(a)
			d=float(d)
			alpha=float(alpha)
			th=float(th)

			file.write(key +":\n")
			file.write("	j_rpy: %s 0 0\n" %(alpha))
			file.write("	j_xyz: %s 0 %s\n" %(a,d))
			file.write("	l_rpy: 0 0 0\n")
			file.write("	l_xyz: %s 0 0\n" %(a/2))
			file.write("	l_len: %s\n" %(a))

if __name__ == '__main__':
    try:
        convertToFile()
    except RuntimeError:
        pass
