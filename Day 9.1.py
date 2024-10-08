import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
#I a looking at a particle in the potential V(x)=exp(-|x|)
print("Input the initial")
initial_x = input("position:  ")
initial_v = input("velocity:  ")

def model(t,y):
    x = y[0]
    v = y[1]
    dxdt = v
    if x>0:
        dvdt = np.exp(-x)
        return [dxdt,dvdt]
    else:
        dvdt = -np.exp(x)
        return [dxdt,dvdt]

solution = solve_ivp(model, (0,10),[initial_x,initial_v], method= 'RK45',t_eval = np.linspace(0,10,500))

t = solution.t
x = solution.y[0]

plt.plot(t,x)
plt.xlabel("time")
plt.ylabel("position")
plt.show()
