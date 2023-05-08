import ortools.linear_solver.pywraplp as olsp

solver = olsp.Solver('Problema', olsp.Solver.GLOP_LINEAR_PROGRAMMING)

# cria variável continua (limite inferior, limite superior, string)
x = solver.NumVar(0, 10, 'x') 
y = solver.NumVar(0, 10, 'y')

# restrições
solver.Add(-x + 2 * y <= 8)
solver.Add(2 * x + y <= 14)
solver.Add(2 * x - y <= 10)

# funcao objetivo
solver.Maximize(x + y)

resultado = solver.Solve()
if resultado == olsp.Solver.OPTIMAL:
    print(f'''Resultado: 
        x = {x.solution_value()}
        y = {y.solution_value()}
        ''')
    