import comm

if __name__ == '__main__':
    # ip = input('Enter IP address:')
    # port = int(input('Enter port: '))
    ip = comm.get_ip()
    # port = 12000
    broadcast_addr = comm.get_broadcast_addr(ip)
    message = 'froggers'
    server_addr = comm.send_discover_message((broadcast_addr, 13000), message)
    print(f'BROADCAST RESPONSE: {server_addr}')

    message = 'goodbye'
    response = comm.send_udp_message(server_addr, message)
    print(f'RESPONSE: {response}')
