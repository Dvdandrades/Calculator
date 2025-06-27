import tkinter as tk

WINDOW_RESOLUTION = "375x667"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry(WINDOW_RESOLUTION)
        self.window.resizable(0, 0)
        self.window.title("Calculator")