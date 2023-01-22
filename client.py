import socket
import comm

if __name__ == '__main__':
    # ip = input('Enter IP address:')
    # port = int(input('Enter port: '))
    # ip = comm.get_ip()
    # port = 12000
    message = 'Marwans-MacBook-Pro.local'
    server_addr = comm.send_discover_message(('192.168.7.255', 13000), message)
    print(f'BROADCAST RESPONSE: {server_addr}')

    message = 'goodbye'
    response = comm.send_udp_message(server_addr, message)
    print(f'RESPONSE: {response}')
