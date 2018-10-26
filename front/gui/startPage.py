import tkinter as tk
from tkinter import ttk


LARGE_FONT = ("Verdana", 12)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        from front.gui.pageOne import PageOne
        from front.gui.pageTwo import PageTwo
        from front.gui.pageThree import PageThree

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
