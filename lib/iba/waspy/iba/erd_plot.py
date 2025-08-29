import numpy as np
import math
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib.ticker as ticker
import numpy as np


def create_erd_evt_plot(name: str, extended_flt_data: list[list[float]]):
    np_histogram = np.asarray(extended_flt_data)
    if np_histogram.ndim != 2:
        raise ValueError("[erd_plot.py] Extended data should be two dimensional.")
    title = name + ".evt.png"
    pixels = _create_grid(np_histogram, x_index=1, y_index=2)
    plot = Plot()
    plot.set_data(pixels, np_histogram, title)
    return plot.create_plot()

def create_erd_mvt_plot(name: str, extended_flt_data: list[list[float]]):
    np_histogram = np.asarray(extended_flt_data)
    if np_histogram.ndim != 2:
        raise ValueError("[erd_plot.py] Extended data should be two dimensional.")
    title = name + ".mvt.png"
    pixels = _create_grid(np_histogram, x_index=1, y_index=4)
    plot = Plot()
    plot.set_data(pixels, np_histogram, title)
    return plot.create_plot()


def _create_grid(extended_data, x_index:int, y_index:int):
    """
    Returns a two dimensional grid containing, for each [y][x], the number of points
    that are contained in that square.

    Parameters x_index, y_index define which indices are selected from the extended data frame. (i.e. which columns).
    This way, one can use this function to plot both mass versus time, and energy versus time.
    """


    if len(extended_data) == 1 and len(extended_data[0]) == 0:
        # no flt data measured
        # return some data
        return np.zeros((1, 1))

    # TODO: zet x=(x: 50-...) en y=(y: 0-...)
    # min_x = np.min(extended_data[:,x_index]) - 1
    max_x = np.max(extended_data[:,x_index]) + 1
    # min_y = np.min(extended_data[:,y_index]) - 1
    max_y = np.max(extended_data[:,y_index]) + 1
    
    #

    GRID_SIZE = (
        math.ceil(max_x),
        math.ceil(max_y)
    )

    pixels = np.zeros((GRID_SIZE[1], GRID_SIZE[0]))

    for point in extended_data:
        x, y = point[x_index], point[y_index]
        x_i, y_i = int(x), int(y)
        pixels[y_i][x_i] += 1
    
    return pixels

@dataclass
class Plot:
    def __init__(self):
        self.ax: plt.Axes = field(init=False, default=None)

        self.fig, self.ax = plt.subplots()

        anchor_values = np.array([1, 2, 4, 8, 16, 32])
        anchor_colors = ["#000000", "#ff5500", "#ffff00", "#00ff00", "#00ffff", "#0000ff"]
        norm_anchor_vals = (np.log2(anchor_values) - np.log2(anchor_values[0])) / \
                            (np.log2(anchor_values[-1]) - np.log2(anchor_values[0]))
        self.cmap = LinearSegmentedColormap.from_list("custom_cmap", list(zip(norm_anchor_vals, anchor_colors)))
        self.norm = colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin=1, vmax=32, base=2)

        self.polygon_points: list[tuple[float, float]] = []
        self.scatter = None
        self.polygon_line = None
        self.closing_line = None
        self.background = None  # for blitting
        self.cbar = None
        self. im = None

    def create_plot(self):
        self.ax.set_xlabel('Time of flight (ns)')
        self.ax.set_ylabel('Energy channel')

        # Create artists **once** and attach to Axes. zorder ensures they draw on top.
        self.scatter = self.ax.scatter([], [], color='red', marker='o', zorder=5, s=10) # s: markersize
        self.polygon_line, = self.ax.plot([], [], color='red', zorder=5, linewidth=1)
        self.closing_line, = self.ax.plot([], [], color='red', linestyle='--', zorder=5, linewidth=1)

        self.fig.tight_layout()
        self.fig.canvas.draw()  # Force layout & renderer

        return self.fig

    def set_data(self, pixels, extended_data, title: str) -> None:
        """Sets the main data for the plot, preserving the polygon artists."""
        self.extended_data = extended_data

        # Mask invalid pixels
        masked_pixels = np.where(pixels >= 1, pixels, np.nan)

        # Create ScalarMappable to convert data -> RGBA
        sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        rgba_img = (sm.to_rgba(masked_pixels, bytes=True))  # uint8 RGBA array

        if self.im is None:
            # Feed pre-rendered RGBA directly to imshow
            self.im = self.ax.imshow(
                rgba_img,
                origin="lower",
                # interpolation="nearest",
                # extent=[0, 300, 0, 8000],
                aspect="auto"
            )
            if self.cbar is None:
                self.cbar = self.fig.colorbar(sm, ax=self.ax)
                self.cbar.set_label('Counts')
        else:
            # Just update bitmap — no re-colormapping
            self.im.set_data(rgba_img)

        self.ax.set_title(title)

        # Force colorbar to show integer ticks instead of powers-of-two
        self.cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

        ticks = [1, 2, 4, 8, 16, 32]
        self.cbar.set_ticks(ticks)
        self.cbar.ax.set_yticklabels([str(t) for t in ticks])

        
        self.fig.canvas.draw()