#I have finally managed to get an orbit simulation working this one is 1 orbit centred around a mass


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

GM = float(input("Mass * big G: "))

#Intoduce a function (I could not get this to work in polar coords)
def newt(t, y):
    x, v_x, y, v_y = y
    dxdt = v_x
    dydt = v_y
    dv_xdt = -GM*x/np.sqrt(x**2+y**2)
    dv_ydt = -GM*y / np.sqrt(x ** 2 + y ** 2)
    return [dxdt, dv_xdt, dydt, dv_ydt]

#Inputs into ivp solver
y0 = [20.0,3, 10, 4]
t_span = (0, 20)
t_eval = np.linspace(0, 20, 10000)


sol = solve_ivp(newt, t_span, y0, t_eval=t_eval)


plt.plot(sol.t,sol.y[1])
plt.xlabel("x")
plt.ylabel("y")
plt.title("Finally an orbit!!")
plt.show()