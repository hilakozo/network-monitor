import tkinter as tk


class AlertWindow:
    def __init__(self, root):
        self.root = root
        self.top = None

    def show_alert(self, msg):
        if self.top:
            self.top.destroy()
        self.top = tk.Toplevel(self.root)
        self.top.title("Alert")
        label = tk.Label(self.top, text=msg, height=10, width=50)
        label.pack()
        button = tk.Button(self.top, text="Dismiss", command=self.top.destroy)
        button.pack()
