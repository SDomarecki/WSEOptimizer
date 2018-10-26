import collections
import tkinter as tk

import matplotlib

from shared.model.company import Company
from shared.model.config import read_config, Config
from shared.model.technical import StockDay

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pandas as pd

LARGE_FONT = ("Verdana", 12)


class WSEOapp(tk.Tk):

    company = None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(Config.geometry)

        # Menu
        self.populate_menu()

        # Kontenery
        self.get_fundamental(Config.last_used_ticker)
        self.get_technical(Config.last_used_ticker)

        lbl = tk.Label(self, text=self.company.name)
        lbl.grid(row=0, column=0, sticky='W')

        df = pd.read_csv('../../database/technical/' + Config.last_used_ticker + '_d.csv', delimiter=';')
        print(df)
        df['Data'] = pd.to_datetime(df['Data'])

        f = Figure(figsize=(5, 2), dpi=100)
        plt = f.add_subplot(111)
        plt.plot(df['Data'], df['Zamkniecie'])

        plt.set_xlabel('Data')
        plt.set_title('Cena')

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)

    def populate_menu(self):
        menu = tk.Menu(self)

        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label='New')

        menu_view = tk.Menu(menu, tearoff=0)
        menu_view.add_command(label='New')

        menu_simulation = tk.Menu(menu, tearoff=0)
        menu_simulation.add_command(label='New')

        menu_about = tk.Menu(menu, tearoff=0)
        menu_about.add_command(label='New')

        menu.add_cascade(label='File', menu=menu_file)
        menu.add_cascade(label='View', menu=menu_view)
        menu.add_cascade(label='Simulation', menu=menu_simulation)
        menu.add_cascade(label='About', menu=menu_about)

        self.config(menu=menu)

    def get_fundamental(self, ticker):
        import json

        with open('../../database/fundamental/' + ticker + '.json', encoding='utf8') as json_data:
            d = json.load(json_data)
            self.company = Company(d['BASIC']['NAME'], d['BASIC']['TICKER'], d['BASIC']['LINK'])
            json_data.close()

    def get_technical(self, ticker):
        # import pandas as pd
        # reader = pd.read_csv('database/technical/' + ticker + '_d.csv', header=None)
        # print(reader)

        import csv
        stockDays = collections.OrderedDict()

        with open('../../database/technical/' + ticker + '_d.csv') as csv_data:
            csv_reader = csv.reader(csv_data, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                date = row[0]
                _open = float(row[1])
                high = float(row[2])
                low = float(row[3])
                close = float(row[4])
                volume = float(row[5])
                circulation = close * volume
                stockDays[date] = StockDay(date, _open, high, low, close, volume, circulation)

        self.company.stockDays = stockDays

        csv_data.close()


if __name__ == "__main__":
    read_config()

    app = WSEOapp()
    app.title(Config.appName + ' ' + Config.version)
    app.mainloop()