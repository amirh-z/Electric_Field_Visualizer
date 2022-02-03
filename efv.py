# amirh_z

import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def add_item():
    cv = charge_value.get()
    x_pos_v = x_pos_value.get()
    y_pos_v = y_pos_value.get()
    if cv.lstrip("-").isdigit() and x_pos_v.isdigit() and y_pos_v.isdigit() and int(x_pos_v) < 31 and int(x_pos_v) > -1 and int(y_pos_v) < 31 and int(y_pos_v) > -1:
        items.append([int(cv), int(x_pos_v), int(y_pos_v)])
        charge_lst.insert("", "end", values=(charge_value.get(), x_pos_value.get(),y_pos_value.get()),)

def del_item():
    selected_items = charge_lst.selection()
    if len(selected_items) != 0:
        s_items = [] # items with their values
        for item in selected_items:
            s_items.append([charge_lst.item(item)['values'][0], charge_lst.item(item)['values'][1], charge_lst.item(item)['values'][2]])
    for item in s_items:
        if item in items:
            items.remove(item)
    charge_lst.delete(*selected_items)

def plot():
    np.seterr(divide='ignore', invalid='ignore')

    # grid size
    N = 30
    M = 30

    # coordinates
    X = np.arange(0, M, 1)
    Y = np.arange(0, N, 1)
    X, Y = np.meshgrid(X, Y)

    Ex = np.zeros((N, M))
    Ey = np.zeros((N, M))

    k = 9e9

    pos_pos = [[], []]
    pos_neg = [[], []]
    for record in items:
        q, qx, qy = record[0], record[1], record[2]
        if q > 0:
            pos_pos[0].append(qx)
            pos_pos[1].append(qy)
        else:
            pos_neg[0].append(qx)
            pos_neg[1].append(qy)
        for i in range(M):
            for j in range(N):
                r = ((i - qx) ** 2 + (j - qy) ** 2) ** 0.5 # distance from (i, j) to (qx, qy) to the power of 3
                if r != 0: 
                    Ex[i, j] += ((k * q * 1e-9 * ((i-qx)/r)) / (r**2))
                    Ey[i, j] += ((k * q * 1e-9 * ((j-qy)/r)) / (r**2))

    colormap = np.hypot(Ex, Ey) # Numeric data that defines the arrow colors by colormapping via norm

    E = np.hypot(Ex, Ey)
    Ex1 = Ex / E
    Ey1 = Ey / E

    plt.figure(figsize=(12, 8))
    plt.plot(*pos_pos, 'bo')
    plt.plot(*pos_neg, 'ro')
    plt.quiver(Y, X, Ex1, Ey1, np.log10(colormap), cmap="hsv", pivot='mid')
    quiver_colorbar = plt.colorbar()
    quiver_colorbar.ax.set_xlabel('$\log_{10}(E)$')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title('Electric Field Lines')
    plt.axis('equal')
    plt.show()

window = tk.Tk()
window.title("Electric Field Visualizer")
window.geometry("600x230")

items = []

charge_lst = ttk.Treeview(window)
charge_lst.place(x=235, y=10)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=charge_lst.yview)
scrollbar.place(x=565, y=10, height=201)
charge_lst.configure(yscrollcommand=scrollbar.set)
charge_lst["columns"] = ("q", "x", "y")
charge_lst.column("q", width = 110, anchor=CENTER)
charge_lst.column("x", width = 110, anchor=CENTER)
charge_lst.column("y", width = 110, anchor=CENTER)
charge_lst['show'] = 'headings'
charge_lst.heading("q", text ="q(nC)")
charge_lst.heading("x", text ="x(m)")
charge_lst.heading("y", text ="y(m)")

charge_label = tk.Label(text="q (nC):").place(x=10, y=10)
charge_value = tk.StringVar()
charge_entry = tk.Entry(width=5, textvariable=charge_value).place(x=150, y=10)

x_pos_label = tk.Label(text="x-axis position (m):").place(x=10, y=40)
x_pos_value = tk.StringVar()
x_pos_entry = tk.Entry(width=5, textvariable=x_pos_value).place(x=150, y=40)

y_pos_label = tk.Label(text="y-axis position (m):").place(x=10, y=70)
y_pos_value = tk.StringVar()
y_pos_entry = tk.Entry(width=5, textvariable=y_pos_value).place(x=150, y=70)

add_btn = tk.Button(window, text="Add", height=2, width=6, command=add_item).place(x=10, y=125)
del_btn = tk.Button(window, text="Delete", height=2, width=6, command=del_item).place(x=80, y=125)
plot_btn = tk.Button(window, text="Plot", height=2, width=6, command=plot).place(x=150, y=125)


window.mainloop()
