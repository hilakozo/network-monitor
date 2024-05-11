import time
import psutil
import config as config
from alert_system import AlertWindow
from graph import SimpleNetworkGraph

MAX_NUMBER_OF_NETWORK_DOWN = 5

NETWORK_DOWN_MSG = "Alert: The network interface is down. Packet rate per second: "
LOW_NETWORK_MSG = "Alert: Low bandwidth usage detected. Packet rate per second: "
HIGH_NETWORK_MESSAGE = "Alert: High bandwidth usage detected. Packet rate per second: "


class NetworkMonitor:
    _graph: SimpleNetworkGraph
    _alert_window: AlertWindow

    def __init__(self, graph: SimpleNetworkGraph, alert_window: AlertWindow):
        self._graph = graph
        self._alert_window = alert_window
        self._count_of_network_down = 0

    @staticmethod
    def _get_network_io_per_second(interface='en0') -> int:
        """
        Fetches the network I/O statistics for the specified interface over a given time interval.
        Returns the number of packets sent and received during that interval.
        """
        initial = psutil.net_io_counters(pernic=True)
        initial_stats = initial.get(interface)

        if initial_stats is None:
            raise ValueError(f"No such interface: {interface}")

        time.sleep(config.RATE_INTERVAL)

        final = psutil.net_io_counters(pernic=True)
        final_stats = final.get(interface)

        # Calculate the number of packets sent and received during the interval
        packet_sent_count = final_stats.packets_sent - initial_stats.packets_sent
        packets_recv_count = final_stats.packets_recv - initial_stats.packets_recv
        overall_traffic = packet_sent_count + packets_recv_count

        return overall_traffic

    def _send_alert(self, traffic_count: int):
        message = ""
        if self._count_of_network_down > MAX_NUMBER_OF_NETWORK_DOWN:
            message = NETWORK_DOWN_MSG
        if traffic_count < config.LOW_NETWORK_THRESHOLD:
            message = LOW_NETWORK_MSG
        if traffic_count > config.HIGH_NETWORK_THRESHOLD:
            message = HIGH_NETWORK_MESSAGE
        if message:
            self._alert_window.show_alert(message + f"{traffic_count}")

    def _draw_graph(self, traffic_count: int):
        self._graph.update_graph(traffic_count)

    def run(self, stop_event):
        print("Monitoring network...")  # Debug print
        while not stop_event.is_set():
            while True:
                traffic_count = NetworkMonitor._get_network_io_per_second()
                self._send_alert(traffic_count)
                self._draw_graph(traffic_count)
