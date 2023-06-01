import socket
import pickle

def send_packet(sock, ack_num, addr):
    #packet = {'ack_num': ack_num}
    sock.sendto(str(ack_num).zfill(10).encode(), addr)

def gbn_receive():
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.settimeout(1)

    # 数据包大小和GBN窗口大小
    packet_size = 1024

    # 设置目标IP地址和端口号
    server_address = ("123.249.11.92", 9000)
    # 发送请求
    #filename = 'new.png'
    filename = str(input("please input the filename:"))
    sock.sendto(filename.encode(), server_address)

    # 接收数据包并写入文件
    with open(filename, 'wb') as f:
        expected_seq_num = 0
        while True:
            packet, addr = sock.recvfrom(1024+10)
            seq_num = int(packet[:10].decode())
            data = packet[10:]
            print("Received packet with seq num: ", seq_num)
            if seq_num == expected_seq_num:
                f.write(data)
                send_packet(sock, expected_seq_num, addr)
                print("Sent ACK with seq num: ", seq_num)
                expected_seq_num += 1
            elif seq_num > expected_seq_num:
                send_packet(sock, expected_seq_num - 1, addr)
            if len(data) < packet_size:
                break

