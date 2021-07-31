import ipaddress
import socket
import sys

import requests
from requests.structures import CaseInsensitiveDict

from jarvis.utils import config_utils

server_ip = None


def send_record_to_server(frame_data):
    # TODO: use config or even ping to find the server on local network ?
    url_service = "http://" + str(get_server_ip()) + ":" + str(get_server_port()) + "/process_audio_request"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/xml; charset=utf8"
    # headers["Authorization"] = config_utils.get_in_config("API_KEY")

    response = requests.post(url_service,
                             headers=headers,
                             data=frame_data)

    print(response.content)


def get_server_port():
    return config_utils.get_in_config('SERVER_PORT') if not None else 5000


def get_server_ip():
    global server_ip

    if server_ip is not None:
        return server_ip

    if config_utils.get_in_config('SERVER_IP') is None:
        print("No server IP specified in config, looking trough the entire network... (might take a few seconds)")
        result = find_server_on_network()
        if result is not None:
            print("Found server on : " + result)
            server_ip = result
            return result
        else:
            sys.exit("Server not found!")
    else:
        return config_utils.get_in_config('SERVER_IP')


def find_server_on_network():
    global server_ip

    # first try on the most common mask 192.168.1.0/24
    server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("192.168.1.0/24"),
                                                        config_utils.get_in_config('SERVER_PORT'))
    if server_ip is None:
        # then 172.16.0.0/12
        server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("172.16.0.0/12"),
                                                            config_utils.get_in_config('SERVER_PORT'))
        if server_ip is None:
            # and last but not least the 10.0.0.0/8 (damn that's gonna be long to scan)
            server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("10.0.0.0/8"),
                                                                config_utils.get_in_config('SERVER_PORT'))

    print("Found server on : " + str(server_ip))
    server_ip = server_ip.compressed
    return server_ip


def find_device_on_network_with_opened_port(hosts, port, timeout=0.02):
    found_ip = None

    for ip in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((socket.gethostbyname(ip.compressed), port))
            if result == 0:
                sock.close()
                found_ip = ip
                break

            sock.close()
        except Exception:
            pass

    return found_ip
