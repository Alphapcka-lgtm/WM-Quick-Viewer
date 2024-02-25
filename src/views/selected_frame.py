import tkinter as tk
from tkinter import ttk
from tkinter import Misc
from views.vertical_scrolled_frame import VerticalScrolledFrame

class SelectedView(tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        # tk.Label(self, text='').grid(column=0, row=0)
        # tk.Label(self, text='').grid(column=0, row=1)

        self.items_frame = VerticalScrolledFrame(self)
        self.items_frame.grid(column=0, row=0, sticky='NESW', padx=10, rowspan=3)

class SelectedFrameTV(ttk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.style = ttk.Style(self)
        self.style.configure('Treeview', rowheight=35)

        self.tv_selected_items = ttk.Treeview(self, columns=('quantity', 'single_price', 'quantity_price'))
        
        self.tv_selected_items.heading('#0', text='Item Name')
        self.tv_selected_items.heading('quantity', text='quantity')
        self.tv_selected_items.heading('single_price', text='Single price')
        self.tv_selected_items.heading('quantity_price', text='Quantity price')
        
        self.tv_selected_items.column('quantity', width=15)
        self.tv_selected_items.column('single_price', width=85)
        self.tv_selected_items.column('quantity_price', width=85)

        self.btn_remove = ttk.Button(self, text='remove item', state='disabled')

        self.lbl_complete_price = ttk.Label(self, font='Helvetica 18 bold')
        
        self.lbl_complete_price.pack(side='bottom', fill='both')
        self.btn_remove.pack(side='bottom', fill='x')
        self.tv_selected_items.pack(side='top', fill='both')
