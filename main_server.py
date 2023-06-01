import socket
import time
from new_send import gbn_send
from gbn_receive import gbn_receive
from sr_send_server import sr_send
from sr_receive import sr_receive
recv_ip = '0.0.0.0'
recv_port = 8000

if __name__ == '__main__':
    while True:
       
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((recv_ip, recv_port))
        data, client_addr= sock.recvfrom(5)
        a = int(data.decode())
        if a == 1:
            gbn_receive()
        elif a == 2:
            sr_receive()
        elif a == 3:
            gbn_send()
        elif a == 4:
            sr_send()
        else:
            print("error")
