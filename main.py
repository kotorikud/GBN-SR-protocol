import socket
import time
from gbn_send import gbn_send
from new_receive import gbn_receive
from sr_send import sr_send
from sr_receive_client import sr_receive
recv_ip = '123.249.11.92'
recv_port = 8000

if __name__ == '__main__':
    while True:
        a = int(input("please select GBN or SR, 1 -> GBN, 2 -> SR, 3 -> GBN_rec, 4 -> SR_rec"))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(a).zfill(5).encode(),(recv_ip,recv_port))   
        if a == 1:
            gbn_send()
        elif a == 2:
            sr_send()
        elif a == 3:
            gbn_receive()
        elif a == 4:
            sr_receive()
        else:
<<<<<<< HEAD
            print("master")
=======
            print("hot_fix")
>>>>>>> hot_fix
