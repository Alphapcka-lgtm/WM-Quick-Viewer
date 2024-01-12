import tkinter as tk
from tkinter import Misc
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import datetime


class PlotFrame(tk.Frame):

    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(self, date_price: dict[datetime, float]):
        if not date_price:
            self.axes.set_visible(False)
            return
        
        stats = [(date, price) for date, price in date_price.items()]
        dates, prices = zip(*stats)
        self.axes.plot(dates, prices, marker='.')
        self.axes.set_xlim(dates[0])
        self.axes.set_ylim(0)
        self.axes.grid(True)
        self.axes.set_visible(True)
        self.axes.set_ylabel('Platin')
        self.canvas.draw()

    def hide_graph(self):
        self.update_graph(None, None)
