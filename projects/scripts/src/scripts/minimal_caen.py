import argparse
import tkinter as tk
import requests
from waspy.drivers.caen import Caen
import os
import ctypes


def put_horizontal_grid(row, elements):
    for index, el in enumerate(elements):
        el.grid(row=row, column=index)


def build_and_run_ui(url: str):
    root = tk.Tk()
    root.title(f'Caen')

    grid_frame = tk.Frame(root)
    oneline_frame = tk.Frame(root)

    acquiring_label = tk.Label(grid_frame, text="Acquiring: ", width=20)
    acquiring_value = tk.Label(grid_frame, text="-")

    caen = Caen(url)

    clear = tk.Button(oneline_frame, text=f"Clear", command=caen.clear)
    start = tk.Button(oneline_frame, text=f"Start", command=caen.start)
    stop = tk.Button(oneline_frame, text=f"Stop", command=caen.stop)

    put_horizontal_grid(0, [acquiring_label, acquiring_value])
    put_horizontal_grid(0, [clear, start, stop])

    grid_frame.pack(side="top", fill="x")
    oneline_frame.pack(side="bottom", fill="x")

    def update():
        try:
            caen_status = requests.get(url + "/api/latest").json()
        except:
            caen_status = {}

        acquiring = caen_status.get("acquisition_active", "-")
        acquiring_value.config(text=f'{acquiring}')
        root.after(2000, update)

    update()

    tk.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='minimal interface',
        description='minimal interface'
    )
    parser.add_argument('driver_url', type=str)
    args = parser.parse_args()

    if os.name == 'nt':
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        user32.ShowWindow(hWnd, False)

    build_and_run_ui(args.driver_url)
