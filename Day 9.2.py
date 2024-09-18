import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("Input the initial")
initial_v = float(input("velocity:  "))
theta= float(input("angle:  "))
d = float(input("drag:  "))

initial_v_1 = float(initial_v)*np.sin(np.pi*theta/180)
initial_v_2 = float(initial_v)*np.cos(np.pi*theta/180)

def coupled_odes(t, y):
    x_1, v_1, x_2, v_2 = y
    dx_1dt = v_1
    dx_2dt = v_2
    dv_1dt = -d*np.sqrt((dx_1dt)**2+(dx_2dt)**2)*dx_1dt-9.81
    dv_2dt = -d*np.sqrt((dx_1dt)**2+(dx_2dt)**2)*dx_2dt
    return [dx_1dt, dv_1dt, dx_2dt, dv_2dt]

y0 = [0,initial_v_1,0,initial_v_2]
t_span = (0, 5)
t_eval = np.linspace(0, 5, 100)
sol = solve_ivp(coupled_odes, t_span, y0, t_eval=t_eval)


#plt.plot(sol.t,sol.y[0])
plt.plot(sol.y[2],sol.y[0])
plt.show()