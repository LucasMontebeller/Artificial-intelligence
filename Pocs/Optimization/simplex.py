import sympy as sp


# transforma as restrições no formato padrão para a forma de folgas
def initialize_simplex(A: sp.Matrix, x: sp.Matrix, b: sp.Matrix):
    print(f"{A} . {x} <= {b}")
    MAX_DIM = 3 
    if (len(A.shape) > MAX_DIM):
        raise Exception(f"Máximo de dimensões suportado é {MAX_DIM}")
    
    A_m, A_n = A.shape[0], A.shape[-1]
    x_m, x_n = x.shape[0], x.shape[-1]
    if (A_n != x_m or (A_m, x_n) != b.shape):
        raise Exception("Formato das restrições inválidos")
    
    x_basico = x
    return sp.Eq(b - A*x, x_basico)
        

# restrições (formato padrão)
A = sp.Matrix([[4, -1], [2, 1], [5, -2]])
b = sp.Matrix([[8], [10], [-2]])
x1, x2 = sp.symbols('x1 x2')
x = sp.Matrix([[x1], [x2]])


folga = initialize_simplex(A, x, b)
print(folga)
