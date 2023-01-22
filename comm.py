import socket
import re
import os
import pickle


def get_ip(ifaces=['wlan1', 'eth0', 'wlan0', 'en0']):
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = f'ifconfig {iface}'
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?= netmask)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return ''


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError as bioe:
        #print(bioe)
        return False
    except ConnectionResetError as cre:
        #print(cre)
        return True
    except BrokenPipeError as bpe:
        #print(bpe)
        return True
    except Exception as e:
        print(e)
        return False
    return False


def start_tcp_server(ip,port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((ip, port))
    tcp_server_socket.listen(1)
    tcp_server_socket.setblocking(False);
    print(f"The TCP server is ready on ({ip}, {port}).")
    return tcp_server_socket


def start_udp_server(ip, port):
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((ip, port))
    #udp_server_socket.setblocking(False);
    print(f"The UDP server is ready on ({ip}, {port}).")
    return udp_server_socket


def accept_tcp_connection(tcp_server):
    tcp_connection_socket, addr = tcp_server.accept()
    tcp_connection_socket.setblocking(True)
    print(f"Accepted connection from {addr}!")
    return tcp_connection_socket, addr


def respond_to(host_id, with_address, port=13000):
    broadcast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_server.bind(('0.0.0.0', port))
    (message, address) = broadcast_server.recvfrom(1024)
    if message.decode() == host_id:
        response = pickle.dumps(with_address)
        broadcast_server.sendto(response, address)
    broadcast_server.close()


def send_discover_message(server, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.sendto(message.encode(), server)
    response, server_address = client_socket.recvfrom(1048)
    return pickle.loads(response)


def send_udp_message(server, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), server)
    response, server_address = client_socket.recvfrom(1048)
    return response.decode()