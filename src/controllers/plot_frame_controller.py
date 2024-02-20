from models.warframe_market_model import WarframeMarketData
from models.market_item import MarketItem
from views.plot_frame import PlotFrame

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from matplotlib.dates import DateFormatter

import statistics
import numpy as np
from datetime import datetime

from tkinter.messagebox import showinfo

class PlotFrameController:
    def __init__(self, model: WarframeMarketData, view: PlotFrame) -> None:
        self.model = model
        self.view = view
        
        self.axes = self.view.figure.add_subplot(111)
        self.axes.set_visible(False)
        self.axes.set_title(PlotFrame.PLOT_TITLE)

        self.annot = self.axes.annotate('', xy=(0,0), xytext=(20,20), textcoords='offset points', bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(True)

        self.view.canvas.mpl_connect('motion_notify_event', self._on_hover)

        self.plt_line: Line2D = None
    
    def update_graph(self, date_price: dict[datetime, ]):
        if not date_price:
            self.axes.set_visible(False)
            self.canvas.draw()
            return
        
        stats = [(date, price) for date, price in date_price.items()]
        dates, prices = zip(*stats)

        self.axes.clear()
        self.axes.set_title(PlotFrame.PLOT_TITLE)
        self.annot = self.axes.annotate('', xy=(0,0), xytext=(10, 10), textcoords='offset points', bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(True)

        # there is only one 2dline
        self.plt_line = self.axes.plot(dates, prices, marker='.', picker=5)[0]
        self.axes.set_xlim(dates[0])
        self.axes.set_ylim(0)
        self.axes.grid(True)
        self.axes.set_visible(True)
        self.axes.set_ylabel('Platin')
        self.axes.xaxis.set_major_formatter(DateFormatter('%d.%m.%Y'))
        self.view.figure.autofmt_xdate()
        self.view.canvas.draw()

    def hide_graph(self):
        self.update_graph(None)
    
    def plot_item(self, item: MarketItem):
        stats = item.statistics
        if stats == None or stats.closed_48h == None or len(stats.closed_48h) == 0:
            showinfo('Statistics', 'Currently there are no statistics available.')
            return
        
        date_prices: dict[datetime, list[float]] = {}
        for stat in stats.closed_48h:
            if stat.datetime in date_prices.keys():
                date_prices[stat.datetime].append(stat.closed_price / stat.volume)
            else:
                date_prices[stat.datetime] = [stat.closed_price / stat.volume]
        
        date_median_price = {date: round(statistics.median(prices)) for date, prices in date_prices.items()}
        self.update_graph(date_median_price)

    def _on_hover(self, event: MouseEvent):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            cont, ind = self.plt_line.contains(event)
            if cont:
                self._update_annot(ind)
                self.annot.set_visible(True)
                self.view.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.view.canvas.draw_idle()
    
    def _update_annot(self, ind: np.ndarray):
        pos = self.plt_line.get_xydata()[ind['ind'][0]]
        self.annot.xy = pos

        price_data = self.plt_line.get_ydata(True)[ind['ind'][0]]
        self.annot.set_text(f'{price_data} Platin')
        self.annot.get_bbox_patch().set_alpha(0.4)
