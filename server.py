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

    try:
        while True:
            (message, address) = udp_server.recvfrom(1024)
            message = message.decode()
            response = message + " OK!"
            udp_server.sendto(response.encode(), address)
    except Exception as e:
        print(e)
        print('Server shut down!')
    finally:
        udp_server.close()


  
