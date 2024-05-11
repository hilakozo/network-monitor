import argparse
import time
import tkinter as tk
from threading import Thread, Event

import psutil
from config import *
from alert_system import AlertWindow
from graph import SimpleNetworkGraph

global zero_packet_down, low_threshold, high_threshold


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor network packet rates")
    parser.add_argument("--low", type=int, default=2, help="Set the low threshold for packet rate alerts")
    parser.add_argument("--high", type=int, default=50, help="Set the high threshold for packet rate alerts")
    parser.add_argument("--graph", action="store_true", help="Display the graph for packet rates")
    args = parser.parse_args()
    print(f"Parsed arguments: {args}")  # Debug print
    return parser.parse_args()


def get_network_io(interface='en0', callback=None):
    """
    Fetches the network I/O statistics for the specified interface over a given time interval.
    Returns the number of packets sent and received during that interval.
    """
    try:
        # Get initial network I/O counters for all interfaces
        initial = psutil.net_io_counters(pernic=True)
        initial_stats = initial.get(interface)

        if initial_stats is None:
            raise ValueError(f"No such interface: {interface}")

        # Sleep for the defined interval
        time.sleep(RATE_INTERVAL)

        # Get final network I/O counters for all interfaces
        final = psutil.net_io_counters(pernic=True)
        final_stats = final.get(interface)

        # Calculate the number of packets sent and received during the interval
        packet_sent = final_stats.packets_sent - initial_stats.packets_sent
        packets_recv = final_stats.packets_recv - initial_stats.packets_recv

        if callback:
            callback(packet_sent + packets_recv)

    except Exception:
        return 0


def check_thresholds(packet_rate, alert_window, graph):
    """
    Checks if the network usage is outside of the defined thresholds and logs alerts.
    """
    global zero_packet_down
    print(f"Checking thresholds for packet rate: {packet_rate}")  # Debug print
    if not packet_rate:
        zero_packet_down += 1
        if zero_packet_down == 5:
            zero_packet_down = 0
            alert_window.show_alert(f"Alert: The network interface is down. Packet rate: {packet_rate} per sec")
        else:
            pass
            # time.sleep(1)

    else:
        zero_packet_down = 0
        if packet_rate < LOW_NETWORK_THRESHOLD:
            alert_window.show_alert(f"Alert: Low bandwidth usage detected. Packet rate: {packet_rate} per sec")
        elif packet_rate > HIGH_NETWORK_THRESHOLD:
            alert_window.show_alert(f"Alert: High bandwidth usage detected. Packet rate: {packet_rate} per sec")
    graph.update_graph(packet_rate)


def monitor_network(alert_window, graph, stop_event):
    print("Monitoring network...")  # Debug print
    while not stop_event.is_set():
        while True:
            get_network_io(callback=lambda network_rate: check_thresholds(network_rate, alert_window, graph))


def setup_main_windows():
    root = tk.Tk()
    root.title("Network Monitor Main")

    alert_root = tk.Toplevel(root)
    alert_root.title("Alerts")

    graph_root = tk.Toplevel(root)
    graph_root.title("Network Graph")

    return root, alert_root, graph_root


def on_closing(root, alert_root, graph_root, stop_event):
    stop_event.set()
    root.destroy()
    alert_root.destroy()
    graph_root.destroy()


def main():
    args = parse_args()
    global zero_packet_down, low_threshold, high_threshold
    zero_packet_down = 0
    stop_event = Event()

    root, alert_root, graph_root = setup_main_windows()

    graph = SimpleNetworkGraph(graph_root) if args.graph else None
    alert_window = AlertWindow(alert_root)

    # with open("config.py", "w") as f:
    #     for line in f.readlines():
    #         if "HIGH_NETWORK_THRESHOLD" in line:
    #
    #         elif "LOW_NETWORK_THRESHOLD" in line:
    #             ΩΩzΩ

    monitor_thread = Thread(target=monitor_network, args=(alert_window, graph, stop_event), daemon=True)
    monitor_thread.start()

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, alert_root, graph_root, stop_event))
    root.mainloop()
    monitor_thread.join()


if __name__ == "__main__":
    main()
