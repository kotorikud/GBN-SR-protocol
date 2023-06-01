import socket
import time

def gbn_receive():
    # 文件名和本地IP地址和端口号
    file_name = "new.png"
    local_ip = "0.0.0.0"
    local_port = 8002

    # 数据包大小和GBN窗口大小
    packet_size = 1024
    #window_size = 1024

    # 建立套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((local_ip, local_port))

    # 打开文件以保存接收到的数据
    with open(file_name, "wb") as file:
        expected_seq_num = 0
        while True:
            # 接收数据包并提取序列号
            packet, client_address = server_socket.recvfrom(packet_size + 10)
            seq_num = int(packet[:10].decode())
            data = packet[10:]

            print("Received packet with seq num: ", seq_num)

            # 如果序列号与预期的序列号匹配，将数据写入文件并发送确认消息
            if seq_num == expected_seq_num:
                file.write(data)
                server_socket.sendto(str(seq_num).encode(), client_address)
                print("Sent ACK with seq num: ", seq_num % 1024)
                expected_seq_num = expected_seq_num + 1

            # 否则，重复发送上一次的确认消息
            else:
                server_socket.sendto(str(expected_seq_num - 1).encode(), client_address)
                print("Sent ACK with seq num: ", (expected_seq_num - 1) % 1024)
            
            # 如果已经接收到了所有的数据包，则退出循环
            if len(data) < packet_size:
                break


        
