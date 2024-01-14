import tkinter as tk
from tkinter import Misc
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from datetime import datetime
import numpy as np


class PlotFrame(tk.Frame):

    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_visible(False)

        self.annot = self.axes.annotate('', xy=(0,0), xytext=(20,20), textcoords='offset points', bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(True)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('motion_notify_event', self._on_hover)

        self.plt_line: Line2D = None

    def update_graph(self, date_price: dict[datetime, float]):
        if not date_price:
            self.axes.set_visible(False)
            return
        
        stats = [(date, price) for date, price in date_price.items()]
        dates, prices = zip(*stats)
        # there is only one 2dline
        self.plt_line = self.axes.plot(dates, prices, marker='.', picker=5)[0]
        self.axes.set_xlim(dates[0])
        self.axes.set_ylim(0)
        self.axes.grid(True)
        self.axes.set_visible(True)
        self.axes.set_ylabel('Platin')
        self.canvas.draw()

    def hide_graph(self):
        self.update_graph(None)

    def _update_annot(self, ind: np.ndarray):
        pos = self.plt_line.get_xydata()[ind['ind'][0]]
        self.annot.xy = pos

        price_data = self.plt_line.get_ydata(True)[ind['ind'][0]]
        self.annot.set_text(f'{price_data} Platinum')
        self.annot.get_bbox_patch().set_alpha(0.4)

    def _on_hover(self, event: MouseEvent):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            cont, ind = self.plt_line.contains(event)
            if cont:
                self._update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()
