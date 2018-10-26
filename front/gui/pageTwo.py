import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        from front.gui.pageOne import PageOne
        from front.gui.startPage import StartPage

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()