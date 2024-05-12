import argparse
import tkinter as tk
from threading import Thread, Event

from alert_system import AlertWindow
from graph import SimpleNetworkGraph
from network_monitor import NetworkMonitor


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor network packet rates")
    parser.add_argument("--low", type=int, default=2, help="Set the low threshold for packet rate alerts")
    parser.add_argument("--high", type=int, default=50, help="Set the high threshold for packet rate alerts")
    parser.add_argument("--graph", action="store_true", help="Display the graph for packet rates")
    args = parser.parse_args()
    return args


def on_closing(root, alert_root, graph_root, stop_event):
    stop_event.set()
    root.destroy()
    alert_root.destroy()
    graph_root.destroy()


def main():
    args = parse_args()
    root = tk.Tk()
    root.title("Network Monitor Main")

    alert_root = tk.Toplevel(root)
    alert_root.title("Alerts")
    alert_window = AlertWindow(alert_root)

    if args.graph:
        graph_root = tk.Toplevel(root)
        graph_root.title("Network Graph")
        graph = SimpleNetworkGraph(graph_root)
    else:
        graph = None

    network_monitor = NetworkMonitor(graph=graph, alert_window=alert_window,
                                     low_threshold=args.low, high_threshold=args.high)

    stop_event = Event()

    monitor_thread = Thread(target=network_monitor.run, args=[stop_event], daemon=True)
    monitor_thread.start()

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, alert_root, graph_root, stop_event))
    root.mainloop()
    monitor_thread.join()


if __name__ == "__main__":
    main()
