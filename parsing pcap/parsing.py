import pyshark
import os


def analyze_pcap(file_path):
    cap = pyshark.FileCapture(file_path, display_filter='http')
    total_packets = 0
    sessions = set()
    http_ok_count = 0
    http_methods = {}

    for packet in cap:
        total_packets += 1

        # Count sessions based on IP tuples
        if 'IP' in packet and 'TCP' in packet:
            sessions.add((packet.ip.src, packet.ip.dst, packet.tcp.srcport, packet.tcp.dstport))

        # HTTP data-analys
        if 'HTTP' in packet:
            # Count HTTP methods
            if hasattr(packet.http, 'request_method'):
                method = packet.http.request_method
                if method not in http_methods:
                    http_methods[method] = 0
                http_methods[method] += 1

            # Count HTTP "OK" responses
            if hasattr(packet.http, 'response_code') and packet.http.response_code == '200':
                http_ok_count += 1

    # Print  results
    print(f'Total number of packets: {total_packets}')
    print(f'Number of sessions: {len(sessions)}')
    print(f'Number of HTTP "OK" responses: {http_ok_count}')
    print('HTTP Methods Count:')
    for method, count in sorted(http_methods.items()):
        print(f'  {method}: {count}')


# file path
pcap_file = 'parsing the pcap httpforever.pcap'
full_pcap_path = os.path.join(os.path.dirname(__file__), pcap_file)
analyze_pcap(full_pcap_path)
