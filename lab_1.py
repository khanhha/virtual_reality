import math
from copy import copy
import numpy as np

class TMatrix: 
	def __init__(self):
		self.mat = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]	
		pass
	
	def __init__(self, m_values):
		assert len(m_values) == 4
		for row in m_values:
			assert len(row) == 4
		self.mat = [list(row) for row in m_values]
	
	def elm(self, i, j):
		return self.mat[i][j]
	
	def row(self, i):
		return self.mat[i]
	
	def col(self, j):
		ret = list(self.mat[i][j] for i in range(4))
		return ret

	def dot(self, a, b):
		s = 0.0
		for i in range(len(a)):
			s += a[i]*b[i]
		return s

	def mult(self, other_matrix):
		out = copy(other_matrix)
		for i in range(4):
			for j in range(4):
				out.mat[i][j] = self.dot(self.row(i), other_matrix.col(j))
		return out

def make_trans_mat(x, y, z):
	T = TMatrix([[1,0,0, x],[0,1,0, y],[0,0,1,z], [0,0,0,1]])
	return T

def make_scale_mat(sx, sy, sz):
	S = TMatrix([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])
	return S

def make_rot_mat(angle_deg, axis):
	cs = math.cos(math.radians(angle_deg))
	sn = math.sin(math.radians(angle_deg))
	if axis == 'x':
		R = TMatrix([[1, 0, 0, 0], [0, cs, sn, 0], [0, -sn, cs, 0], [0, 0, 0, 1]])
	elif axis == 'y':
		R = TMatrix([[cs, 0, -sn, 0], [0, 1, 0, 0], [0, 0, 1 , 0], [0, 0, 0, 1]])
	elif axis == 'z':
		R = TMatrix([[1, 0, 0, 0], [0, cs, sn, 0], [0, -sn, cs, 0], [0, 0, 0, 1]])
	else:
		assert False

if __name__ == '__main__':
	m = TMatrix(((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0, 1)))
	m1 = TMatrix(((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0, 1)))
	ret =  m.mult(m1)
	print(ret.mat)

	T = make_trans_mat(10,20,30)