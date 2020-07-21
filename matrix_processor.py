import numpy as np
from numpy.linalg import inv

class Matrix:
    values = []
    n = 0
    m = 0

    def __init__(self):
        self.n, self.m = map(int, input().split())
        self.values = [[float(x) for x in input().split()] for _ in range(self.n)]

    def add_matrix(self, mat):
        n1 = len(mat)
        m1 = len(mat[0])
        if not (n1 == self.n and m1 == self.m):
            print("ERROR")
            return False
        return [[mat[i][j] + self.values[i][j] for j in range(n1)] for i in range(m1)]

    def multiply_by_matrix(self, mat):
        n1 = len(mat)
        m1 = len(mat[0])
        if not (n1 == self.m):
            print("ERROR")
            return False
        return [[sum(a * b for a, b in zip(a_row, b_col)) for b_col in zip(*mat)] for a_row in self.values]

    def multiply_by_num(self, num):
        return [[self.values[i][j] * num for j in range(self.m)] for i in range(self.n)]

    def transpone_matrix(self, tr_type):
        if tr_type == 1:
            return [[self.values[j][i] for j in range(self.m)] for i in range(self.n)]
        elif tr_type == 2:
            res = [row[::-1] for row in self.values]
            res = [[res[j][i] for j in range(self.m)] for i in range(self.n)]
            return [row[::-1] for row in res]
        elif tr_type == 3:
            return [row[::-1] for row in self.values]
        elif tr_type == 4:
            return [self.values[self.n - i - 1] for i in range(self.n)]

    def determinant(self, mat):
        n1 = len(mat)
        m1 = len(mat[0])
        res = 0
        if n1 == m1 == 1:
            return mat[0][0]
        if n1 == m1 == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        else:
            for k in range(len(mat[0])):
                minor = [[mat[i][j] for j in range(m1) if j != k] for i in range(1, n1)]
                res += self.determinant(minor) * mat[0][k] * (-1) ** k
            return res

    def invert_matrix(self):
        det = self.determinant(self.values)
        if det == 0:
            print("ERROR")
            return False
        mat = self.transpone_matrix(1)
        res = self.transpone_matrix(1)
        n1 = len(mat)
        m1 = len(mat[0])
        for k in range(n1):
            for l in range(m1):
                minor = [[mat[i][j] for j in range(m1) if j != l] for i in range(n1) if i != k]
                res[k][l] = self.determinant(minor) * mat[k][l] * (-1) ** (k + l)
        return [[res[i][j] / det for j in range(m1)] for i in range(n1)]

    def print_matrix(self):
        print(*[print(*x) for x in self.values])


exit = False
while not exit:
    print('''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
''')
    choice = int(input())
    if choice == 0:
        exit = True
    elif choice == 1:
        mat1 = Matrix()
        mat2 = Matrix()
        mat1.values = mat1.add_matrix(mat2.values)
        mat1.print_matrix()
    elif choice == 2:
        mat1 = Matrix()
        num = int(input())
        mat1.values = mat1.multiply_by_num(num)
        mat1.print_matrix()
    elif choice == 3:
        mat1 = Matrix()
        mat2 = Matrix()
        mat1.values = mat1.multiply_by_matrix(mat2.values)
        mat1.print_matrix()
    elif choice == 4:
        print('''1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
''')
        choice = int(input())
        mat1 = Matrix()
        mat1.values = mat1.transpone_matrix(choice)
        mat1.print_matrix()
    elif choice == 5:
        mat1 = Matrix()
        print(mat1.determinant(mat1.values))
    elif choice == 6:
        mat1 = Matrix()
        np_mat = inv(np.array(mat1.values)).round(4)
        mat1.values = np_mat
        mat1.print_matrix()
