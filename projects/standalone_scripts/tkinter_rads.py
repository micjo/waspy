import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Label Widget Demo')


# label with a specific font
label_bad = ttk.Label(
    root,
    text='too much rads',
    background="red", foreground='white',anchor='center',
    font=("Helvetica", 14))

label_good = ttk.Label(
    root,
    text='too little rads', anchor='center',
    background="green", foreground='white',
    font=("Helvetica", 14))

label_bad.pack(fill='x', ipady=10)
label_good.pack(fill='x', ipady=10)

toggle_rads = True
def toggle():
    global toggle_rads
    toggle_rads = not toggle_rads
    if toggle_rads:
        label_good.pack_forget()
        label_bad.pack(fill='x', ipady=10)
    else:
        label_bad.pack_forget()
        label_good.pack(fill='x', ipady=10)
    root.after(2000, toggle)

toggle()
root.mainloop()