import tkinter
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

from waspy.hardware_control.hw_action import get_packed_histogram
from waspy.hardware_control.rbs_entities import CaenDetector

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")
ax.set_xlim(0,1024)
ax.set_ylim(0,5000)
ax.set_xlabel("Energy Level")
ax.set_ylabel("Occurrence")
ax.grid(which='both')

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.quit)


def update_values():
    detector = CaenDetector(board="33", channel=0, identifier="", bins_min=0, bins_max=8192,
                            bins_width=1024)

    resp_code, data = get_packed_histogram("http://localhost:20200/api/latest", detector)
    line.set_data(range(len(data)), data)

    # required to update canvas and attached toolbar!
    canvas.draw()
    root.after(1000,update_values)


def update_frequency(new_val):
    # retrieve frequency
    f = float(new_val)

    # update data
    # y = 2 * np.sin(2 * np.pi * f * t)
    # line.set_data(t, y)





update_values()

# outer_frame = tkinter.Frame(root, borderwidth=2, relief="groove")
# outer_frame.pack(side="bottom", fill="both", expand=True, padx=20, pady=20)
#
# tkinter.Label(outer_frame, text="Child Frame 1").pack(side='left')
# tkinter.Label(outer_frame, text="Child Frame 2").pack(side='left')
# tkinter.Label(outer_frame, text="Child Frame 3").pack(fill="both", expand=True)
#
# s1 = ttk.Separator(outer_frame, orient="horizontal")
# s2 = ttk.Separator(outer_frame, orient="horizontal")
#
# f1.pack(side="top", fill="both", expand=True)
# s1.pack(side="top", fill="x", expand=False)
# f2.pack(side="top", fill="both", expand=True)
# s2.pack(side="top", fill="x", expand=False)
# f3.pack(side="top", fill="both", expand=True)


slider_update = tkinter.Scale(root, from_=1, to=5, orient=tkinter.HORIZONTAL,
                              command=update_frequency, label="Frequency [Hz]")

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.grid(sticky=(tkinter.N, tkinter.E, tkinter.W, tkinter.S))
slider_update.grid()
toolbar.grid()
canvas.get_tk_widget().grid(sticky="NEWS")

root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

tkinter.mainloop()