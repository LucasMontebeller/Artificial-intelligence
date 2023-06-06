from gurobipy import *

model = Model('exemplo')

x = model.addVar(obj=1, vtype='C', name='x')
y = model.addVar(obj=1, vtype='C', name='y')

model.update()

model.addConstr(-x+2*y<=8)
model.addConstr(2*x+y<=14)
model.addConstr(2*x-y<=10)

model.ModelSense=-1

model.optimize()

print('x=',x.X)
print('y=',y.X)