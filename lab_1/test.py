from lab_1.TMatrix import *
from lab_1.Vector4 import *

if __name__ == '__main__':
	m = TMatrix(((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0, 1)))
	m1 = TMatrix(((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0, 1)))
	ret =  m.mult(m1)
	print(ret.mat)

	print('\ntask 2')
	print('\ntranslation mat')
	T = make_trans_mat(10,20,30)
	print(T)

	print('\nscale mat ')
	S = make_scale_mat(1,2,3)
	print(S)

	print('\nrotation mat x')
	R= make_rot_mat(45,'x')
	print(R)

	print('\nrotation mat x')
	R= make_rot_mat(90,'y')
	print(R)

	print('\nrotation mat x')
	R= make_rot_mat(120,'z')
	print(R)

	#task 3
	p0 = Vector4(2,4,6,2)
	p1 = Vector4(0,0,0,1)
	d = euclidean_distance(p0, p1)
	print('\ntask 3\ndistance = {0}'.format(d))

	# task 4
	print('\ntask 4\nvector multiplication')
	v = Vector4(1,2,3,1)
	v_1 = T.mult_vec(v)
	print(v_1)

	#task 5
	print('\ntask 4 \nrot(90, x) · rot(-180, z) = rot(180, y) · rot(90, x)')
	R_x = make_rot_mat(90, 'x')
	R_y = make_rot_mat(180, 'y')
	R_z = make_rot_mat(-180, 'z')

	T_0 = R_y.mult(R_x)
	T_1 = R_x.mult(R_z)
	T_dif = T_0 - T_1
	print('difference between two matrices')
	print(T_dif)
