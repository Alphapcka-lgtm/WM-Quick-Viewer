import tkinter as tk
from tkinter import Misc
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class PlotFrame(tk.Frame):

    PLOT_TITLE = "Preise über die letzten 48h"

    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.figure = Figure(figsize=(3, 3), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
