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

request = "minutes"


def get_data():
    while True:
        try:
            response = requests.get("http://localhost:8000/api/trends/" + request)
        except Exception as e:
            yield {}

        yield response.json()


def set_request(req):
    print("set request to: " + req)
    global request
    request = req


class Graph:
    def __init__(self):
        self.fig = plt.figure("my first plot")
        ax_size = [0.11, 0.20, 1 - 0.140,
                   1 - 0.27]  # [left, bottom, width, height] as fractions of figure width and height.
        self.axes = self.fig.add_axes(ax_size)
        self.reset_axes()

        self.day_button = widgets.Button(plt.axes([0.84, 0.01, 0.05, 0.060]), 'days')
        self.day_button.on_clicked(lambda e: set_request("days"))
        self.hour_button = widgets.Button(plt.axes([0.89, 0.01, 0.05, 0.060]), 'hr')
        self.hour_button.on_clicked(lambda e: set_request("hours"))
        self.min_button = widgets.Button(plt.axes([0.94, 0.01, 0.05, 0.060]), 'min')
        self.min_button.on_clicked(lambda e: set_request("minutes"))

    def __call__(self, data):
        self.reset_axes()
        df = pd.DataFrame.from_dict(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d %H:%M:%S")
        self.axes.plot(df['timestamp'], df['value'])

    def reset_axes(self):
        self.axes.clear()
        self.axes.set_xlabel("energy levels")
        self.axes.set_ylabel("occurrence")
        self.axes.grid(which='both')
        self.axes.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        self.axes.xaxis.set_major_locator(ticker.AutoLocator())


if __name__ == "__main__":
    get_data()

    graph = Graph()
    ani = animation.FuncAnimation(graph.fig, graph,
                                  frames=get_data(),
                                  interval=1200,
                                  repeat=True,
                                  cache_frame_data=False,
                                  blit=False)

    plt.show()
