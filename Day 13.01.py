#This new code is a simulation of two separate bodies (new and improved!!)
#I have programmed a collision behaviour (a slap-dash electric contact force)


import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

#These are the default initial conditions
y0p =[0,1,0,1,3,-1,3,1]
r1p = 0.5
r2p = 0.5
M1p = 1
M2p = 1
print("GRAVITATING OBJECTS SIMULATION")
print("     ")
time.sleep(1.0)
print("You may edit the initial conditions (answer 'position'/'velocity'/'angle') or the objects (answer 'radius'/'mass') or use the presets (answer 'none'/'no')")
time.sleep(1)
print("     ")
response = input("What would you like to edit? ")
time.sleep(0.5)

#This is the UI
while True:
    if response in ["angles", "angle", "initial angle", "initial angles"]:
        theta1 = float(input("Initial angle 1: ")) / 180 * np.pi
        theta2 = float(input("Initial angle 2: ")) / 180 * np.pi
        v_0_x1 = np.sqrt(y0p[1] ** 2 + y0p[3] ** 2) * np.cos(theta1)
        v_0_y1 = np.sqrt(y0p[1] ** 2 + y0p[3] ** 2) * np.sin(theta1)
        v_0_x2 = np.sqrt(y0p[5] ** 2 + y0p[7] ** 2) * np.cos(theta1)
        v_0_y2 = np.sqrt(y0p[5] ** 2 + y0p[7] ** 2) * np.sin(theta1)
        r1 = r1p
        r2 = r2p
        M1 = M1p
        M2 = M2p
        y0 = [y0p[0], v_0_x1, y0p[2], v_0_y1, y0p[4], v_0_x2, y0p[6], v_0_y2]
    elif response in ["velocity", "velocities"]:
        v1_0 = float(input("Initial velocity 1: "))
        v_0_x1 = v1_0 * np.cos(np.arctan(y0p[3] / y0p[1]))
        v_0_y1 = v1_0 * np.sin(np.arctan(y0p[3] / y0p[1]))
        v2_0 = float(input("Initial velocity 2: "))
        v_0_x2 = v2_0 * np.cos(np.arctan(y0p[7] / y0p[5]))
        v_0_y2 = v2_0 * np.sin(np.arctan(y0p[7] / y0p[5]))
        r1 = r1p
        r2 = r2p
        M1 = M1p
        M2 = M2p
        y0 = [y0p[0], v_0_x1, y0p[2], v_0_y1, y0p[4], v_0_x2, y0p[6], v_0_y2]
    elif response in ["positions", "position", "initial position"]:
        initial_position1 = input("Initial x1,y1: ").split(",")
        x1_0 = float(initial_position1[0])
        y1_0 = float(initial_position1[1])
        initial_position2 = input("Initial x2,y2: ").split(",")
        x2_0 = float(initial_position2[0])
        y2_0 = float(initial_position2[1])
        r1 = r1p
        r2 = r2p
        M1 = M1p
        M2 = M2p
        y0 = [x1_0, y0p[1], y1_0, y0p[3], x2_0, y0p[5], y2_0, y0p[7]]
    elif response in ["radius", "radii"]:
        r1 = float(input("Radius 1: "))
        r2 = float(input("Radius 2: "))
        M1 = M1p
        M2 = M2p
        y0 = y0p
    elif response in ["mass", "masses"]:
        M1 = float(input("Mass 1: "))
        M2 = float(input("Mass 2: "))
        r1 = r1p
        r2 = r2p
        y0 = y0p
    elif response in ["none", "no", "NO", "No", "nothing", "n", "N"]:
        print("Okay")
        y0 = y0p
        r1 = r1p
        r2 = r2p
        M1 = M1p
        M2 = M2p
    else:
        print("Please try again")


    # This funtion defines the coupled ODEs which describe each body
    def newt(t, y):
        x1, v_x1, y1, v_y1, x2, v_x2, y2, v_y2 = y
        dx1dt = v_x1
        dy1dt = v_y1
        dx2dt = v_x2
        dy2dt = v_y2
        if np.sqrt((x2 - x1) ** 2 + (y1 - y2) ** 2) >= r1 + r2:
            dv_x1dt = -10 * M2 * x1 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_y1dt = -10 * M2 * y1 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_x2dt = -10 * M1 * x2 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_y2dt = -10 * M1 * y2 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
        elif np.sqrt((x2 - x1) ** 2 + (y1 - y2) ** 2) < r1 + r2:
            dv_x1dt = 10 ** 18 * x1 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_y1dt = 10 ** 18 * y1 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_x2dt = 10 ** 18 * x2 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)
            dv_y2dt = 10 ** 18 * y2 / (np.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 3)

        return [dx1dt, dv_x1dt, dy1dt, dv_y1dt, dx2dt, dv_x2dt, dy2dt, dv_y2dt]


    # Other inputs into ivp solver
    t_span = (0, 50)
    t_eval = np.linspace(0, 50, 1000)

    sol = solve_ivp(newt, t_span, y0, t_eval=t_eval)

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(-max(max(np.abs(sol.y[0])), max(np.abs(sol.y[4]))), max(max(np.abs(sol.y[0])), max(np.abs(sol.y[4]))))
    ax.set_ylim(-max(max(np.abs(sol.y[2])), max(np.abs(sol.y[6]))), max(max(np.abs(sol.y[2])), max(np.abs(sol.y[6]))))

    point1, = ax.plot([], [], 'bo', markersize=8)
    point2, = ax.plot([], [], 'ro', markersize=8)


    def init():
        point1.set_data([], [])
        point2.set_data([], [])
        return point1, point2


    # Function to update the plot for each frame
    def update(frame):
        x1 = sol.y[0, frame]
        y1 = sol.y[2, frame]
        x2 = sol.y[4, frame]
        y2 = sol.y[6, frame]
        point1.set_data([x1], [y1])
        point2.set_data([x2], [y2])
        return point1, point2


    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(sol.t), init_func=init, blit=True, interval=2)

    plt.show()
    response2 = input("continue?")
    if response2 in["none", "no", "NO", "No", "nothing", "n", "N"]:
        print("Exiting the program.")
        break
    elif response2 in ["yes","y","Y"]:
        response = input("What would you like to edit? ")













