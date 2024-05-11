import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimpleNetworkGraph:
    def __init__(self, parent):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.draw()
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.packet_rates = []

    def update_graph(self, packet_rate):
        self.packet_rates.append(packet_rate)
        if len(self.packet_rates) > 60:
            self.packet_rates.pop(0)
        self.ax.clear()
        self.ax.plot(self.packet_rates, label='Packet Rate')
        self.ax.set_title("Network Packet Rate Over Time")
        self.ax.set_xlabel("Time (updates)")
        self.ax.set_ylabel("Packets")
        self.ax.legend()
        self.canvas.draw()
