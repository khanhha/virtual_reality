import math
from copy import copy

class TMatrix:
    def __init__(self, m_values = None):
        if m_values is None:
            self.mat = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        else:
            assert len(m_values) == 4
            for row in m_values:
                assert len(row) == 4
            self.mat = [list(row) for row in m_values]

    def __sub__(self, other):
        out = TMatrix()
        for i in range(4):
            for j in range(4):
                out.mat[i][j] = self.mat[i][j] - other.mat[i][j]
        return out

    def row(self, i):
        return self.mat[i]

    def col(self, j):
        ret = list(self.mat[i][j] for i in range(4))
        return ret

    def dot(self, a, b):
        s = 0.0
        for ai,bi in zip(a,b):
            s += ai*bi
        return s

    def mult(self, other_matrix):
        out = TMatrix()
        for i in range(4):
            for j in range(4):
                out.mat[i][j] = self.dot(self.row(i), other_matrix.col(j))
        return out

    def mult_vec(self, v):
        return [self.dot(row,v) for row in self.mat]

    def __str__(self):
        out = ''
        for row in self.mat:
            out = out + '{0:10}{1:10}{2:10}{3:10}\n'.format("%.4f" % row[0], "%.4f" % row[1], "%.4f" % row[2], "%.4f" % row[3])
        return out

def make_trans_mat(x, y, z):
    T = TMatrix([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])
    return T


def make_scale_mat(sx, sy, sz):
    S = TMatrix([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])
    return S


def make_rot_mat(angle_deg, axis):
    cs = math.cos(math.radians(angle_deg))
    sn = math.sin(math.radians(angle_deg))
    if axis == 'x':
        R = TMatrix([[1, 0, 0, 0], [0, cs, sn, 0], [0, -sn, cs, 0], [0, 0, 0, 1]])
        #R = TMatrix([[1, 0, 0, 0], [0, cs, -sn, 0], [0, sn, cs, 0], [0, 0, 0, 1]])
    elif axis == 'y':
        R = TMatrix([[cs, 0, -sn, 0], [0, 1, 0, 0], [sn, 0, cs, 0], [0, 0, 0, 1]])
        #R = TMatrix([[cs, 0, sn, 0], [0, 1, 0, 0], [-sn, 0, cs, 0], [0, 0, 0, 1]])
    elif axis == 'z':
        R = TMatrix([[cs, sn, 0, 0], [-sn, cs, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        #R = TMatrix([[cs, -sn, 0, 0], [sn, cs, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    else:
        assert False
    return R