import math
class Vector4:
    def __init__(self, v0, v1, v2, v3):
        self.v = [v0,v1,v2,v3]

    def __getitem__(self, idx):
        return self.v[idx]

def euclidean_distance(p0, p1):
    a = (p0.v[i]/p0.v[3] for i in range(3))
    b = (p1.v[i]/p1.v[3] for i in range(3))
    return math.sqrt(sum((ai-bi)*(ai-bi) for ai, bi in zip(a,b)))

