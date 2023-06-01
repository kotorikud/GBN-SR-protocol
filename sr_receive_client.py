import socket

def sr_receive():
    # 定义接收方的 IP 地址和端口号
    recv_ip = '123.249.11.92'
    recv_port = 8030

    # 定义缓存，用于存储已经接收到的数据包
    buffer = []

    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 设置超时时间
    # sock.settimeout(1)

    # 定义滑动窗口的大小和起始位置
    WINDOW_SIZE = 100
    packet_size = 1024
    # 发送请求
    filename = '1.png'
    sock.sendto(filename.encode(), (recv_ip, recv_port))

    # 接收数据包并写入文件
    with open(filename, 'wb') as file:
        expected_seq_num = 0
        while True:
            packet, addr = sock.recvfrom(packet_size + 10)
            seq_num = int(packet[:10].decode())
            data = packet[10:]
            print("Received packet with seq num: ", seq_num)
            if seq_num == expected_seq_num:
                buffer.insert(0, packet)
                flag = 0
                while buffer and int(buffer[0][:10].decode()) == expected_seq_num:
                    file.write(buffer[0][10:])
                    buffer.pop(0)
                    expected_seq_num += 1
            elif seq_num > expected_seq_num and seq_num < expected_seq_num + WINDOW_SIZE:
                buffer.insert(seq_num - expected_seq_num, packet)
                    #send_packet(sock, expected_seq_num - 1, addr)

            # 发送 ACK
            sock.sendto(str(seq_num).encode(), addr)
            if len(data) < packet_size:
                break

