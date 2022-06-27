import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from hive.hardware_control.hw_action import get_packed_histogram
from hive.hardware_control.rbs_entities import CaenDetector
from matplotlib import widgets, dates, ticker


class Graph:
    def __init__(self):
        self.detector= CaenDetector(board="33", channel=0, identifier="", bins_min=0, bins_max=8192, bins_width=1024)
        title_string = "Histogram board=" + self.detector.board + ", channel=" + str(self.detector.channel)
        self.fig = plt.figure(title_string)
        self.title_text = plt.figtext(0.20, 0.94, title_string, size='x-large', color='blue')
        ax_size = [0.11, 0.20, 1-0.140, 1-0.27] # [left, bottom, width, height] as fractions of figure width and height.
        self.axes = self.fig.add_axes(ax_size)
        self.reset_axes()
        self.pause = False

    def set_play_pause(self, animation):
        self.pause = not self.pause
        if self.pause:
            animation.pause()
        else:
            animation.resume()

    def reset_axes(self):
        self.axes.clear()
        self.axes.set_xlabel("Energy Level")
        self.axes.set_ylabel("Occurrence")
        self.axes.grid(which='both')
        self.axes.yaxis.set_ticks_position('left')
        self.axes.xaxis.set_ticks_position('bottom')
        # self.axes.xaxis_date()
        # self.axes.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        # self.axes.xaxis.set_major_locator(ticker.AutoLocator())

    def consume_data(self, data):
        self.reset_axes()
        self.axes.plot(data)

    def get_data(self):
        while True:
            resp_code, data = get_packed_histogram("http://localhost:20200/api/latest", self.detector)
            yield data


if __name__ == "__main__":
    graph = Graph()
    ani = animation.FuncAnimation(graph.fig, graph.consume_data,
                                  frames=graph.get_data(),
                                  interval=1200,
                                  repeat=True,
                                  cache_frame_data=False,
                                  blit=False)

    graph.day_button = widgets.Button(plt.axes([0.84, 0.01, 0.15, 0.060]), 'play/pause')
    graph.day_button.on_clicked(lambda _: graph.set_play_pause(ani))
    plt.show()