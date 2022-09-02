"""
Created on Sun Feb 20 18:25:17 2022

@author: Amirmahdi_Amrollahi_Biukey
"""
from pyomo.environ import *
import numpy as np

# Set 1 :
# [0 132 217 164 58]
# [132 0 290 201 79]
# [217 290 0 113 303]
# [164 201 113 0 196]
# [58 79 303 196 0]

# 0 132 217 164 58 132 0 290 201 79 217 290 0 113 303 164 201 113 0 196 58 79 303 196 0

# Set2
#[0, 10, 15, 20] 
#[10, 0, 35, 25]
#[15, 35, 0, 30] 
#[20, 25, 30, 0]

# 0 10 15 20 10 0 35 25 15 35 0 30 20 25 30 0

print("Hello Nice to meet you")

ntown = int(input("Enter the number of towns: "))
# gathering number of towns

print("Enter the distances between towns in a single line separated by space: ")
# collecting the distance between towns

val = list(map(float, input().split()))

dis = np.array(val).reshape(ntown,ntown)
# forming the distances matrixs

M = ConcreteModel()

M.i = RangeSet(ntown)
M.j = RangeSet(ntown)
M.u = RangeSet(2,ntown)

M.x = Var(M.i, M.j, within = Binary)
# will we going from town i to town j ?

M.U = Var(M.u, within = NonNegativeReals)

M.z = Objective(expr = sum(dis[i-1][j-1]*M.x[i,j] for i in M.i for j in M.j) , sense = minimize)

M.ST = ConstraintList()

for i in M.i:
    M.ST.add(sum(M.x[i,j] for j in M.j) - M.x[i,i] == 1)
# just a single destination for each origin

for j in M.j:
    M.ST.add(sum(M.x[i,j] for i in M.i) - M.x[j,j] == 1)
# just a single origin for each destination

for i in M.i:
    for j in M.j:
        if (i>1 and j>1 and i!=j):
                M.ST.add(M.U[i] - M.U[j] + M.x[i,j]*ntown <= ntown-1)
# limitation to enforce that there is only a single tour covering all towns
 
#M.pprint()
opt = SolverFactory('cplex')
results = opt.solve(M)
display(M)

print('The optimum route is:')
for i in M.x:
    if(M.x[i].value == 1):
        print('x[', i, '] =', M.x[i].value)
    
print("The minimum distance is shown Bellow:")
print(value(M.z))

