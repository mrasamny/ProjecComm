import socket
import comm

if __name__ == "__main__":

    hostname = socket.gethostname()
    port = 12000
    ip = comm.get_ip()

    if len(ip) == 0:
        print('No interface found that has an IP address')

    try:
        # start up udp server
        udp_server = comm.start_udp_server(ip, port)
    except Exception as e:
        print(e)
        exit(1)

    while True:
        try:
            # start broadcast server and wait for query
            comm.respond_to(hostname, (ip, port))
        except Exception as e:
            print(e)
            break

        try:
            is_done = False
            while not is_done:
                (message, address) = udp_server.recvfrom(1024)
                message = message.decode()
                if message == 'goodbye':
                    is_done = True
                response = message + " OK!"
                udp_server.sendto(response.encode(), address)
        except Exception as e:
            print(e)
            print('Server shut down!')
            break;
    udp_server.close()


  
