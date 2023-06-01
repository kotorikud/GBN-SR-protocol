import socket

def sr_receive():
    # 定义接收方的 IP 地址和端口号
    recv_ip = '0.0.0.0'
    recv_port = 8001
    file_name = "xx.jpg"

    # 创建 UDP 套接字并绑定端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((recv_ip, recv_port))

    # 定义缓存，用于存储已经接收到的数据包
    buffer = []

    # 定义滑动窗口的大小和起始位置
    size,_ = sock.recvfrom(1024)
    WINDOW_SIZE = int(size[:10].decode())
    print("windowsize=",WINDOW_SIZE)
    packet_size = 1024
    base = 0
    with open(file_name,'wb') as file:
        while True:
            # 接收数据包
            packet, addr = sock.recvfrom(packet_size + 10)
            seq_num = int(packet[:10].decode())
            

            # 如果收到的数据包的序号是窗口的起始位置，则将窗口向前移动，并将缓存中的数据包写入文件
            if seq_num == base:
                buffer.insert(0,packet)
                flag = 0
                while buffer and int(buffer[0][:10].decode()) == base:
                    
                        file.write(buffer[0][10:])
                        buffer.pop(0)
                        base += 1
                
            # 如果收到的数据包的序号在窗口中，则将数据包添加到缓存中
            elif seq_num > base and seq_num < base + WINDOW_SIZE:
                buffer.insert(seq_num - base, packet) 
                # 发送重复 ACK，告诉发送方需要重传数据包
                #ack_packet = (base - 1, b'ACK')
                #sock.sendto(pickle.dumps(ack_packet), addr)

            # 发送 ACK
            sock.sendto(str(seq_num).encode(), addr)
