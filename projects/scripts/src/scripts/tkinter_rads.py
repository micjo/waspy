import random
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from pydantic import BaseSettings
import requests

root = tk.Tk()
root.title('Label Widget Demo')

pastel_green = "#82e67e"
pastel_yellow = "#f7e283"
pastel_red = "#ff7c70"


class GlobalConfig(BaseSettings):
    G64_url = "http://169.254.150.100/hive/api/any/g64"

env_config = GlobalConfig()


label_bad = ttk.Label(
    root,
    text='Danger of ionizing radiation',
    background=pastel_red, foreground='black', anchor='center',
    font=("Helvetica", 70))

label_ok = ttk.Label(
    root,
    text='Safe to enter', anchor='center',
    background=pastel_green, foreground='black',
    font=("Helvetica", 70))

label_warning = ttk.Label(
    root,
    text='Qualified personnel only', anchor='center',
    background=pastel_yellow, foreground='black',
    font=("Helvetica", 70))

label_timestamp = ttk.Label(
    root,
    text='1/1/1970 00:00:00', anchor='ne',
    font=("Helvetica", 20))

label_rads = ttk.Label(
    root,
    text='0', anchor='center',
    font=("Helvetica", 30))

label_bad.pack(fill='both')
label_ok.pack(fill='both')
label_warning.pack(fill='both')
label_timestamp.pack(fill='x')
label_rads.pack(fill='x')


def clear():
    label_ok.pack_forget()
    label_bad.pack_forget()
    label_warning.pack_forget()


def set_widget_colors(color):
    label_timestamp.configure(background=color)
    label_rads.configure(background=color)


def update():
    clear()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rads = float(requests.get(env_config.G64_url).json()['dosage_rate(uSv/h)'])

    if rads > 3.2 :
        active_label = label_bad
        set_widget_colors(pastel_red)
    elif rads > 1.2:
        active_label = label_warning
        set_widget_colors(pastel_yellow)
    else:
        active_label = label_ok
        set_widget_colors(pastel_green)

    root.after(2000, update)
    label_timestamp.configure(text=now)
    label_rads.configure(text="Radiation level: {0:.5f} uSv/h".format(rads))
    active_label.pack(fill='both', expand=True)


update()
root.mainloop()
