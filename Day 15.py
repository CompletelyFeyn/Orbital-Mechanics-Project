import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import font
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation


# UI is better and it has three bodies
# I removed the collision functionality as  I couldn't crack scaling the radius with the displayed radius
# Plus it wasn't very realistic for planets anyway - the next time I will try I'll simulate extended bodies/ fluids

# Takes the inputs from the UI and makes them useful
def gather():
    global M1, M2, M3

    initial_position1 = s1_0.get()
    initial_positions1 = initial_position1.split(",")
    x1_0 = float(initial_positions1[0])
    y1_0 = float(initial_positions1[1])

    initial_position2 = s2_0.get()
    initial_positions2 = initial_position2.split(",")
    x2_0 = float(initial_positions2[0])
    y2_0 = float(initial_positions2[1])

    initial_position3 = s3_0.get()
    initial_positions3 = initial_position3.split(",")
    x3_0 = float(initial_positions3[0])
    y3_0 = float(initial_positions3[1])

    v_0_x1 = float(v1_0.get()) * np.cos(float(theta1.get()) * np.pi / 180)
    v_0_y1 = float(v1_0.get()) * np.sin(float(theta1.get()) * np.pi / 180)

    v_0_x2 = float(v2_0.get()) * np.cos(float(theta2.get()) * np.pi / 180)
    v_0_y2 = float(v2_0.get()) * np.sin(float(theta2.get()) * np.pi / 180)

    v_0_x3 = float(v3_0.get()) * np.cos(float(theta3.get()) * np.pi / 180)
    v_0_y3 = float(v3_0.get()) * np.sin(float(theta3.get()) * np.pi / 180)

    M1 = float(M1_0.get())
    M2 = float(M2_0.get())
    M3 = float(M3_0.get())

    return [x1_0, v_0_x1, y1_0, v_0_y1, x2_0, v_0_x2, y2_0, v_0_y2, x3_0, v_0_x3, y3_0, v_0_y3]


# Defines the three-body ODE
def newt(t, y):
    x1, v_x1, y1, v_y1, x2, v_x2, y2, v_y2, x3, v_x3, y3, v_y3 = y
    dx1dt = v_x1
    dy1dt = v_y1
    dx2dt = v_x2
    dy2dt = v_y2
    dx3dt = v_x3
    dy3dt = v_y3
    r_12 = np.sqrt((x2 - x1) ** 2 + (y1 - y2) ** 2)
    r_13 = np.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
    r_23 = np.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
    dv_x1dt =- 10 * M2 * (x1-x2) / (r_12 ** 3) - 10 * M3 * (x1-x3) / (r_13 ** 3)
    dv_y1dt = -10 * M2 * (y1-y2) / (r_12 ** 3) - 10 * M3 * (y1-y3) / (r_13 ** 3)
    dv_x2dt = -10 * M1 * (x2-x1) / (r_12 ** 3) - 10 * M3 * (x2-x3) / (r_23 ** 3)
    dv_y2dt =- 10 * M1 * (y2-y1) / (r_12 ** 3)  -10 * M3 * (y2-y3) / (r_23 ** 3)
    dv_x3dt = -10 * M1 * (x3 - x1) / (r_13 ** 3) - 10 * M2 * (x3-x2) / (r_23 ** 3)
    dv_y3dt =- 10 * M1 * (y3 - y1) / (r_13 ** 3) - 10 * M2 * (y3 - y2) / (r_23 ** 3)

    return [dx1dt, dv_x1dt, dy1dt, dv_y1dt, dx2dt, dv_x2dt, dy2dt, dv_y2dt, dx3dt, dv_x3dt, dy3dt, dv_y3dt]


# Solves ODE and animates
def simulate():
    t_span = (0, 200)
    t_eval = np.linspace(0, 200, 10000)

    # ODE solver
    initial_conditions = gather()
    sol = solve_ivp(newt, t_span, initial_conditions, t_eval=t_eval)

    # Create a figure and axes
    fig, ax = plt.subplots()
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)

    # Scale the markers according to the mass
    size1 = np.ceil(np.sqrt(M1))
    size2 = np.ceil(np.sqrt(M2))
    size3 = np.ceil(np.sqrt(M3))
    point1, = ax.plot([], [], 'bo', markersize=size1)
    point2, = ax.plot([], [], 'ro', markersize=size2)
    point3, = ax.plot([], [], 'go', markersize=size3)

    # sets the initial frame
    def init():
        point1.set_data([], [])
        point2.set_data([], [])
        point3.set_data([], [])
        return point1, point2, point3

    # Function to update the plot for each frame
    def update(frame):
        x1 = sol.y[0, frame]
        y1 = sol.y[2, frame]
        x2 = sol.y[4, frame]
        y2 = sol.y[6, frame]
        x3 = sol.y[8, frame]
        y3 = sol.y[10, frame]
        point1.set_data([x1], [y1])
        point2.set_data([x2], [y2])
        point3.set_data([x3], [y3])
        return point1, point2, point3

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(sol.t), init_func=init, blit=True, interval=0.2)

    plt.show()


# The preset initial conditions
y0p = [0, 1, 0, 1, -2, 1, 2, -1, 4, -2, 4, 2]

M1p = 5
M2p = 1
M3p = 2

# Creates the UI and formats
root = tk.Tk()
root.title("Initial conditions:")
root.geometry("1035x400")
custom_font = ("Courier New", 12)
custom_font1 = ("Courier New", 10)
root.configure(bg="#292929")
text1_colourfg = "#337d37"
text1_colourbg = "#292929"
text2_colourfg = "white"
text2_colourbg = "#3b3b3b"

label1 = tk.Label(root, text="Initial position 1 (x,y):", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label1.grid(row=0, column=0, padx=10, pady=10)
s1_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
s1_0.grid(row=1, column=0, padx=10, pady=10)
s1_0.insert(0, str(y0p[0]) + "," + str(y0p[2]))

label2 = tk.Label(root, text="Initial position 2 (x,y):", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label2.grid(row=0, column=1, padx=10, pady=10)
s2_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
s2_0.grid(row=1, column=1, padx=10, pady=10)
s2_0.insert(0, str(y0p[4]) + "," + str(y0p[6]))

label03 = tk.Label(root, text="Initial position 3 (x,y):", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label03.grid(row=0, column=2, padx=10, pady=10)
s3_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
s3_0.grid(row=1, column=2, padx=10, pady=10)
s3_0.insert(0, str(y0p[8]) + "," + str(y0p[10]))

label3 = tk.Label(root, text="Initial angle 1:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label3.grid(row=2, column=0, padx=10, pady=10)
theta1 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
theta1.grid(row=3, column=0, padx=10, pady=10)
theta1.insert(0, str(np.arctan(y0p[3] / y0p[1]) * 180 / np.pi))

label4 = tk.Label(root, text="Initial angle 2:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label4.grid(row=2, column=1, padx=10, pady=10)
theta2 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
theta2.grid(row=3, column=1, padx=10, pady=10)
theta2.insert(0, str(np.arctan(y0p[7] / y0p[5]) * 180 / np.pi))

label05 = tk.Label(root, text="Initial angle 3:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label05.grid(row=2, column=2, padx=10, pady=10)
theta3 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
theta3.grid(row=3, column=2, padx=10, pady=10)
theta3.insert(0, str(np.arctan(y0p[9] / y0p[11]) * 180 / np.pi))

label5 = tk.Label(root, text="Initial velocity 1:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label5.grid(row=4, column=0, padx=10, pady=10)
v1_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
v1_0.grid(row=5, column=0, padx=10, pady=10)
v1_0.insert(0, np.sqrt(y0p[1] ** 2 + y0p[3] ** 2))

label6 = tk.Label(root, text="Initial velocity 2:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label6.grid(row=4, column=1, padx=10, pady=10)
v2_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
v2_0.grid(row=5, column=1, padx=10, pady=10)
v2_0.insert(0, np.sqrt(y0p[5] ** 2 + y0p[7] ** 2))

label07 = tk.Label(root, text="Initial velocity 3:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label07.grid(row=4, column=2, padx=10, pady=10)
v3_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
v3_0.grid(row=5, column=2, padx=10, pady=10)
v3_0.insert(0, np.sqrt(y0p[9] ** 2 + y0p[11] ** 2))

label7 = tk.Label(root, text="Mass 1:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label7.grid(row=6, column=0, padx=10, pady=10)
M1_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
M1_0.grid(row=7, column=0, padx=10, pady=10)
M1_0.insert(0, M1p)

label8 = tk.Label(root, text="Mass 2:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label8.grid(row=6, column=1, padx=10, pady=10)
M2_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
M2_0.grid(row=7, column=1, padx=10, pady=10)
M2_0.insert(0, M2p)

label09 = tk.Label(root, text="Mass 3:", font=custom_font, fg=text1_colourfg, bg=text1_colourbg)
label09.grid(row=6, column=2, padx=10, pady=10)
M3_0 = tk.Entry(root, width=40, font=custom_font1, fg=text2_colourfg, bg=text2_colourbg)
M3_0.grid(row=7, column=2, padx=10, pady=10)
M3_0.insert(0, M3p)

submit_button = tk.Button(root, text="Simulate", command=lambda: simulate(), font=custom_font, fg="white", bg="#292929")
submit_button.grid(row=8, column=1, padx=10, pady=10)
root.mainloop()
