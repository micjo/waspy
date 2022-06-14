import io
from datetime import datetime, timedelta

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
from pydantic import BaseSettings

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

request = "minutes"
import sys


class GlobalConfig(BaseSettings):
    LOGBOOK_URL = "http://169.254.150.200:8001"


env_config = GlobalConfig()


class Graph:
    def __init__(self):
        self._request_interval = 'minutes'
        self._log_scale = False
        self._hide_term = True

        self.fig = plt.figure(sys.argv[2])
        self.fig.set_figheight(3.2)
        self.fig.set_figwidth(6.5)

        self.title_text = plt.figtext(0.20, 0.94, f'{sys.argv[2]}', size='x-large', color='blue')
        self.tstamp_text = plt.figtext(0.45, 0.94, f'Time: ')
        self.value_text = plt.figtext(0.80, 0.94, f'Value: ')

        self.fig.patch.set_facecolor('gray')
        self.fig.patch.set_alpha(0.2)
        # [left, bottom, width, height] as fractions of fig width and height.
        ax_size = [0.14, 0.21, 1 - 0.155, 1 - 0.29]
        self.axes = self.fig.add_axes(ax_size)

        self.reset_axes()

        self.day_button = widgets.Button(plt.axes([0.84, 0.01, 0.05, 0.060]), 'days')
        self.day_button.on_clicked(lambda _: self._set_request_interval("days"))
        self.hour_button = widgets.Button(plt.axes([0.89, 0.01, 0.05, 0.060]), 'hr')
        self.hour_button.on_clicked(lambda _: self._set_request_interval("hours"))
        self.min_button = widgets.Button(plt.axes([0.94, 0.01, 0.05, 0.060]), 'min')
        self.min_button.on_clicked(lambda _: self._set_request_interval("minutes"))
        self.terminal_button = widgets.Button(plt.axes([0.01, 0.01, 0.075, 0.060]), 'Term.')
        self.terminal_button.on_clicked(lambda _: self.toggle_show())
        self.b_log = widgets.Button(plt.axes([0.01, 0.94, 0.075, 0.060]), 'lin/log')
        self.b_log.on_clicked(lambda _: self._toggle_lin_log())

    def generate_data(self):
        trend_url = env_config.LOGBOOK_URL
        while True:
            end = datetime.now()

            if self._request_interval == "days":
                start = datetime.now() - timedelta(days=1)
                step = "30"
            elif self._request_interval == "hours":
                start = datetime.now() - timedelta(hours=2)
                step = "5"
            elif self._request_interval == "minutes":
                start = datetime.now() - timedelta(minutes=10)
                step = "1"
            else:
                start = end
                step = "1"

            full_url = "{trend_url}/get_trend?start={start}&end={end}&id={id}&step={step}".format(
                trend_url=trend_url, start=start, end=end, id=sys.argv[1], step=step)
            try:
                response = requests.get(full_url).json()
            except Exception as e:
                response = None
            yield response

    def consume_data(self, data):
        if data == None:
            print("No data Available !!")
            self.axes.set_facecolor('lightgrey')
            self.axes.get_lines()[0].set_color("black")
            return
        else:
            self.axes.set_facecolor('white')

        self.reset_axes()
        df = pd.DataFrame.from_dict(data)
        df['epoch'] = pd.DatetimeIndex(pd.to_datetime(df['epoch'], unit='s', utc=True)).tz_convert(
            'Europe/Brussels').tz_localize(None)
        self.axes.plot(df['epoch'], df[sys.argv[1]], color='blue')
        self.tstamp_text.set_text(f'Time: {df["epoch"].iloc[-1]}')
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
        if self._log_scale:
            self.axes.set_yscale('log')
        else:
            self.axes.set_yscale('linear')

    def _set_request_interval(self, interval: str):
        self._request_interval = interval

    def _toggle_lin_log(self):
        self._log_scale = not self._log_scale

    def toggle_show(self):
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        self._hide_term = not self._hide_term
        if hWnd:
            user32.ShowWindow(hWnd, self._hide_term)


if __name__ == "__main__":
    # url = sys.argv[3]

    graph = Graph()

    ani = animation.FuncAnimation(graph.fig, graph.consume_data,
                                  frames=graph.generate_data,
                                  interval=1000,
                                  repeat=True,
                                  cache_frame_data=False,
                                  blit=False)
    graph.toggle_show()
    plt.show()
