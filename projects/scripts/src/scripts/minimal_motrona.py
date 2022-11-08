import argparse
import tkinter as tk
import requests
from waspy.drivers.motrona_dx350 import MotronaDx350
import os
import ctypes


def put_horizontal_grid(row, elements):
    for index, el in enumerate(elements):
        el.grid(row=row, column=index)


def build_and_run_ui(url: str):
    root = tk.Tk()
    root.title(f'Motrona')

    grid_frame = tk.Frame(root)
    oneline_frame = tk.Frame(root)

    target_charge_label = tk.Label(grid_frame, text="Target Charge")
    target_charge_entry = tk.Entry(grid_frame)
    target_charge_value = tk.Label(grid_frame, text="-")

    accumulated_charge_label = tk.Label(grid_frame, text="Charge")
    accumulated_charge_value = tk.Label(grid_frame, text="-")

    motrona = MotronaDx350(url)

    def set_target_charge():
        motrona.set_target_charge(target_charge_entry.get())

    set_target_charge = tk.Button(oneline_frame, text=f"Set Target Charge", command=set_target_charge)
    clear_start = tk.Button(oneline_frame, text=f"Clear & Start", command=motrona.start_count_from_zero)
    pause = tk.Button(oneline_frame, text=f"Pause", command=motrona.pause)

    put_horizontal_grid(0, [target_charge_label, target_charge_entry, target_charge_value])
    put_horizontal_grid(1, [accumulated_charge_label, accumulated_charge_value])
    put_horizontal_grid(2, [set_target_charge, clear_start, pause])
    grid_frame.pack(side="top", fill="x")
    oneline_frame.pack(side="top", fill="x")

    def update():
        try:
            motrona_status = requests.get(url+"/api/latest").json()
        except:
            motrona_status = {}

        target_charge = motrona_status.get("target_charge(nC)", "")
        charge = motrona_status.get("charge(nC)", "")
        target_charge_value.config(text=f'{target_charge}')
        accumulated_charge_value.config(text=f'{charge} -> {target_charge}')
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

