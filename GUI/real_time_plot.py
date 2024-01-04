'''
Created on Dec 26, 2023

@author: Kripali Jain
'''
import tkinter as tk
import serial
import numpy as np
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasAgg, FigureCanvasTkAgg
from matplotlib.backends.backend_template import FigureCanvas

data = np.array([])
cond = False

port = 'COM4'
baudrate = 9600

def plot_data():
    global cond, data
    
    # if(cond==True):
    # port = 'COM3'
    # baudrate = 250000
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.write(b'l000000000')    
    data = np.array([])
        # if (len(data)<100):
    for a in range (8000):
        
        line = ser.readline()
        a+=1
        if line :
            string = line.decode()
            data.append(string)
        # line.decode()
        # data = np.append(data, float(line[0:4]))
        # else:
        #     data[0:99] = data[1:100]
        #     data[99] = float(a[0:4])
        #     lines.set_xdata = (np.arrange(0, len(data)))
        #     lines.set_ydata = np.arrange(data)

    canvas.draw(data)
    gui.after(1, plot_data)    
            
def plot_start():
    # port = 'COM3'
    # baudrate = 250000
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.reset_input_buffer()
    global cond
    cond = True
    ser.write(b's000000000')
    ser.reset_input_buffer()
    
def plot_stop():
    # port = 'COM3'
    # baudrate = 250000
    ser = serial.Serial(port, baudrate, timeout=1)
    # ser.reset_input_buffer()
    global cond
    cond = False 
    ser.write(b'l000000000')    

                    
def close():
    global cond
    cond = False 
    ser.close()                    

# Create the main window
gui = tk.Tk()
gui.title("Graphical User Interface for Laser Locking")
gui.config(bg="white")

fig = Figure()
ax = fig.add_subplot(111)

ax.set_xlim(0, 10000)
ax.set_ylim(0, 6000)
lines = ax.plot([], []) [0]

canvas = FigureCanvasTkAgg(fig, master = gui)
canvas.get_tk_widget().place(x=10, y=10, width = 600, height = 400)
canvas.draw()

gui.update()
Scan = tk.Button(gui, text="Scan", fg = "white", bg = "#124ba6", bd=10, relief="raised", font = ("Arial", 18), command = lambda: plot_start()).place(relx = 0.53, rely = 0.7, anchor = tk.CENTER)

gui.update()
Lock = tk.Button(gui, text = "Lock", relief="raised", bg = "#575859", padx=20,  borderwidth=2, fg = "white", font = ("Arial bold", 12), command = lambda: plot_data()).place(relx = 0.02, rely = 0.02, anchor = tk.CENTER)

gui.update()
Stop = tk.Button(gui, text = "Comm_stop", relief="raised", bg = "#575859", padx=20,  borderwidth=2, fg = "white", font = ("Arial bold", 12), command = lambda: close()).place(relx = 0.06, rely = 0.08, anchor = tk.CENTER)



# ser = serial.Serial(port, baudrate, timeout=1)
# ser.reset_input_buffer()

gui.after(1, plot_data)
gui.mainloop()
