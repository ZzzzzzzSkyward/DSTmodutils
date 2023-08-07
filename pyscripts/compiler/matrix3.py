import math

class Matrix3:
    def __init__(self):
        self.matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]

    def set_translation(self, x, y):
        self.matrix[0][2] = x
        self.matrix[1][2] = y

    def set_scale(self, x, y):
        self.matrix[0][0] = x
        self.matrix[1][1] = y

    def set_rotation(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        self.matrix[0][0] = c
        self.matrix[0][1] = s
        self.matrix[1][0] = -s
        self.matrix[1][1] = c

    def get_translation(self):
        return [self.matrix[0][2], self.matrix[1][2]]

    def __neg__(self):
        new_matrix = Matrix3()
        new_matrix.matrix = [-x for x in self.matrix]
        return new_matrix

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            result = Matrix3()
            for i in range(3):
                for j in range(3):
                    result.matrix[i][j] = sum(
                        self.matrix[i][k] * other.matrix[k][j]
                        for k in range(3)
                    )
            return result
        else:
            raise TypeError("Unsupported operand type for multiplication.")

    def __add__(self, other):
        if isinstance(other, Matrix3):
            result = Matrix3()
            for i in range(3):
                for j in range(3):
                    result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
            return result
        else:
            raise TypeError("Unsupported operand type for addition.")

    def __str__(self):
        return str(self.matrix)

def create_trans_rot_scale_pivot_matrix(pos: tuple|list, angle: float, scale: tuple|list, pivot: tuple|list) -> Matrix3:
    pivot_trans = Matrix3()
    pivot_trans.set_translation(pivot[0], pivot[1])

    scale_m = Matrix3()
    scale_m.set_scale(scale[0], scale[1])

    trans = Matrix3()
    trans.set_translation(pos[0], pos[1])

    rot = Matrix3()
    rot.set_rotation(angle)

    return trans * rot * scale_m * pivot_trans

def reverse_trans_rot_scale_pivot_matrix(matrix: Matrix3, last, first) -> tuple:
    m = matrix.matrix
    scale_x = math.sqrt(m[0][0] ** 2 + m[1][0] ** 2)
    scale_y = math.sqrt(m[0][1] ** 2 + m[1][1] ** 2)

    eps = 1e-3

    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if det < 0:
        if first or (last["scale_x"] <= last["scale_y"]):
            scale_x = -scale_x
        else:
            scale_y = -scale_y

    if math.fabs(scale_x) < eps or math.fabs(scale_y) < eps:
        angle = last["angle"]
    else:
        sin_approx = 0.5 * (m[0][1] / scale_y - m[1][0] / scale_x)
        cos_approx = 0.5 * (m[0][0] / scale_x + m[1][1] / scale_y)
        angle = math.atan2(sin_approx, cos_approx)

    spin = (1 if math.fabs(angle - last["angle"]) <= math.pi else -1) * (-1 if angle < last["angle"] else 1)

    last["scale_x"] = scale_x
    last["scale_y"] = scale_y
    last["angle"] = angle

    return {"scale_x": scale_x, "scale_y": scale_y, "angle": angle, "spin": spin}