import argparse
import tkinter as tk
import requests
from waspy.drivers.aml_smd2 import AmlSmd2


def put_horizontal_grid(row, elements):
    for index, el in enumerate(elements):
        el.grid(row=row, column=index)


def build_and_run_ui(first_name: str, second_name: str, url: str):
    root = tk.Tk()
    root.title(f'AML {first_name} {second_name}')

    grid_frame = tk.Frame(root)
    oneline_frame = tk.Frame(root)

    first_label = tk.Label(grid_frame, text=first_name)
    first_entry = tk.Entry(grid_frame)
    first_value = tk.Label(grid_frame, text="-")

    second_label = tk.Label(grid_frame, text=second_name)
    second_entry = tk.Entry(grid_frame)
    second_value = tk.Label(grid_frame, text="-")


    def move_first():
        aml = AmlSmd2(url)
        aml.move_first(first_entry.va)

    first_go = tk.Button(oneline_frame, text=f"Move {first_name}", command=move_first)
    second_go = tk.Button(oneline_frame, text=f"Move {second_name}")
    load = tk.Button(oneline_frame, text="Load")

    put_horizontal_grid(0, [first_label, first_entry, first_value])
    put_horizontal_grid(1, [second_label, second_entry, second_value])
    put_horizontal_grid(2, [first_go, second_go, load])
    grid_frame.pack(side="top", fill="x")
    oneline_frame.pack(side="top", fill="x")


    def update():
        try:
            aml_status = requests.get(url+"/api/latest").json()
            print(aml_status)
            first_value.configure(text=aml_status.get("motor_1_position", "-"))
            second_value.configure(text=aml_status.get("motor_2_position", "-"))
        except:
            first_value.configure(text="-")
            second_value.configure(text="-")
        root.after(2000, update)

    update()

    tk.mainloop()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='minimal interface',
        description='minimal interface'
    )
    parser.add_argument('first_name', type=str)
    parser.add_argument('second_name', type=str)
    parser.add_argument('driver_url', type=str)
    args = parser.parse_args()

    build_and_run_ui(args.first_name, args.second_name, args.driver_url)

