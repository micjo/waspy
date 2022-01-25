import io

import requests
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.widgets as widgets
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import pandas as pd
import json
import ctypes


# needed for older python versions
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

request = "minutes"
import sys
hide = True


def get_data():
    while True:
        response = requests.get("http://169.254.150.200/hive/api/trends/" + request, timeout=10)
        yield response.json()


def set_request(req):
    print("set request to: " + req)
    global request
    request = req


log_scale = False
def lin_log():
    global log_scale
    log_scale = not log_scale


class Graph:
    def __init__(self):
        self.fig = plt.figure(sys.argv[2])
        self.fig.set_figheight(3.2)
        self.fig.set_figwidth(6.5)

        self.title_text = plt.figtext(0.20, 0.94, f'{sys.argv[2]}', size='x-large', color='blue')
        self.tstamp_text = plt.figtext(0.45, 0.94, f'Time: ')
        self.value_text = plt.figtext(0.80, 0.94, f'Value: ')

        self.fig.patch.set_facecolor('gray')
        self.fig.patch.set_alpha(0.2)
        ax_size = [0.14, 0.21, 1 - 0.155,
                   1 - 0.29]  # [left, bottom, width, height] as fractions of figure width and height.
        self.axes = self.fig.add_axes(ax_size)

        self.reset_axes()

        self.day_button = widgets.Button(plt.axes([0.84, 0.01, 0.05, 0.060]), 'days')
        self.day_button.on_clicked(lambda e: set_request("days"))
        self.hour_button = widgets.Button(plt.axes([0.89, 0.01, 0.05, 0.060]), 'hr')
        self.hour_button.on_clicked(lambda e: set_request("hours"))
        self.min_button = widgets.Button(plt.axes([0.94, 0.01, 0.05, 0.060]), 'min')
        self.min_button.on_clicked(lambda e: set_request("minutes"))
        self.terminal_button = widgets.Button(plt.axes([0.01, 0.01, 0.075, 0.060]), 'Term.')
        self.terminal_button.on_clicked(lambda e: show_window())
        self.b_log = widgets.Button(plt.axes([0.01, 0.94, 0.075, 0.060]), 'lin/log')
        self.b_log.on_clicked(lambda e: lin_log())

    def __call__(self, data):
        self.reset_axes()
        df = pd.DataFrame.from_dict(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d %H:%M:%S")
        self.axes.plot(df['timestamp'],df[sys.argv[1]], color='blue')
        self.tstamp_text.set_text(f'Time: {df["timestamp"].iloc[-1]}')
        self.value_text.set_text(f'Value: {df[sys.argv[1]].iloc[-1]}')

    def reset_axes(self):
        self.axes.clear()
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel(sys.argv[2])
        self.axes.grid(which='both')
        self.axes.yaxis.set_ticks_position('left')
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.xaxis_date()
        self.axes.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        self.axes.xaxis.set_major_locator(ticker.AutoLocator())
        global log_scale
        if log_scale:
            self.axes.set_yscale('log')
        else:
            self.axes.set_yscale('linear')


def show_window():
    global hide
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    hide = not hide
    if hWnd:
        user32.ShowWindow(hWnd, hide)


if __name__ == "__main__":
    get_data()

    graph = Graph()
    ani = animation.FuncAnimation(graph.fig, graph,
                                  frames=get_data(),
                                  interval=1200,
                                  repeat=True,
                                  cache_frame_data=False,
                                  blit=False)

    show_window()
    plt.show()

