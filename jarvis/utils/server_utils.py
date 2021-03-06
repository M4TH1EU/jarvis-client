import ipaddress
import socket
import sys

import requests
from requests.structures import CaseInsensitiveDict

from jarvis.utils import config_utils

server_ip = None


def send_record_to_server(raw_audio_data):
    url_service = "http://" + str(get_server_ip()) + ":" + str(get_server_port()) + "/process_audio_request"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/xml; charset=utf8"
    headers['Client-Ip'] = socket.gethostbyname(socket.gethostname())
    headers['Client-Port'] = str(config_utils.get_in_config('PORT'))
    # headers["Authorization"] = config_utils.get_in_config("API_KEY")

    response = requests.post(url_service,
                             headers=headers,
                             data=raw_audio_data)

    print(bytes.decode(response.content))


def send_sentence_to_server(sentence):
    url_service = "http://" + str(get_server_ip()) + ":" + str(get_server_port()) + "/process_text_request"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json; charset=utf8"
    headers['Client-Ip'] = socket.gethostbyname(socket.gethostname())
    headers['Client-Port'] = str(config_utils.get_in_config('PORT'))
    # headers["Authorization"] = config_utils.get_in_config("API_KEY")

    try:
        response = requests.post(url_service,
                                 headers=headers,
                                 json={'sentence': sentence})

        print(bytes.decode(response.content))
    except ConnectionError:
        print("Error connecting to the server (server was probably shutdown during request)...")


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

    ip = socket.gethostbyname(socket.gethostname())

    # sometimes it might return the local ip (127.0.0.1) adding local should solves that
    # TODO: see if we only use the ".local" ip
    if ip.startswith("127.0"):
        ip = socket.gethostbyname(socket.gethostname() + ".local")

    if ip.startswith("192.168.1"):
        server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("192.168.1.0/24"),
                                                            config_utils.get_in_config('SERVER_PORT'))
    elif ip.startswith("172.16"):
        server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("172.16.0.0/12"),
                                                            config_utils.get_in_config('SERVER_PORT'))
    elif ip.startswith("10."):
        print("Warning: scanning for server on a huge network, please specify the server's ip in the config.json asap.")
        server_ip = find_device_on_network_with_opened_port(ipaddress.ip_network("10.0.0.0/8"),
                                                            config_utils.get_in_config('SERVER_PORT'))
    if server_ip is None:
        return None

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
