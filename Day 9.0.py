import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("Input the initial")
initial_x = input("position:  ")
initial_v = input("velocity:  ")
d = float(input("Damping constant: "))

def model(t,y):
    x = y[0]
    v = y[1]
    dxdt = v
    dvdt = -x -d*v
    return [dxdt,dvdt]

solution = solve_ivp(model, (0,50),[initial_x,initial_v], method= 'RK45',t_eval = np.linspace(0,50,500))

t = solution.t
x = solution.y[0]

plt.plot(t,x)
plt.xlabel("time")
plt.ylabel("position")
plt.show()