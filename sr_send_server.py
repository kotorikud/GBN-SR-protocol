import socket
import time
import os

def sr_send():
    # 定义接收方的 IP 地址和端口号
    recv_ip = '0.0.0.0'
    recv_port = 8030

    # 创建 UDP 套接字并绑定端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((recv_ip, recv_port))

    # 接收客户端请求
    data, addr = sock.recvfrom(1024)
    filename = data.decode()
    print("filename",filename)
    # 数据包大小和sr窗口大小
    packet_size = 1024
    window_size = 50
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"File '{filename}' not found")
        exit(-1)
        #return

    with open(filename, "rb") as file:
        data = file.read()
    packets_data = [data[i:i + packet_size] for i in range(0, len(data), packet_size)]  ##最后一个不够1024怎么处理
    # 定义起始位置
    
    base = 0
    next_seq_num = 0

    # 定义发送窗口中每个数据包的状态
    buffer_size = window_size
    state = [0] * ((len(data) - 1) // buffer_size + 1)

    #packets = {}  # 窗口中每个数据包的发送时间和重传次数
    
    start_time = time.time()
    total_bytes_sent = 0
    retransmitted_packets = 0
    total_packets_sent = 0
    lost_packets = 0
    # 设置超时时间
    sock.settimeout(1)
    while base < len(packets_data):
        # 发送窗口内的数据包
        while next_seq_num < base + window_size and next_seq_num < len(packets_data):
            if state[next_seq_num] == 0:
                packet = packets_data[next_seq_num]
                sock.sendto(str(next_seq_num).zfill(10).encode() + packet, addr)
                #print('Send packet:' ,next_seq_num)
                state[next_seq_num] = 1
                total_bytes_sent += buffer_size
                total_packets_sent += 1

            #packets[next_seq_num] = {'data': packets_data[next_seq_num], 'time': time.time(), 'retries': 0}
            next_seq_num += 1

            # 接收ACK
            try:
                packet, addr = sock.recvfrom(1024)
                ack_num = int(packet[:10].decode())
                if ack_num > base:
                    print('Received ACK:', ack_num)
                    state[ack_num] = 2
                    # print(f"Ack received: {ack_num}")
                elif ack_num == base:
                    state[ack_num] = 2
                    temp = ack_num
                    sum = 0
                    print('Received ACK:', ack_num)
                    while temp < len(state) and state[temp] == 2:
                        sum += 1
                        temp += 1
                    base += sum
            except socket.timeout:
                # 检查是否有超时未收到ACK的数据包
                #next_seq_num = base
                # 超时重传未被确认的数据包
                print('Timeout')
                for i in range(base, next_seq_num):
                    if state[i] == 1:
                        packet = packets_data[i]
                        sock.sendto(str(i).zfill(10).encode() + packet, addr)
                        # print('Resend packet:', i)
                        retransmitted_packets += 1
                        total_bytes_sent += buffer_size
                        total_packets_sent += 1
                        lost_packets += 1
            
                pass
            # 判断是否传输完成
            if base * buffer_size >= len(data):
                break

    # 发送结束标记
    #send_packet(sock, b'', seq_num, addr)
    sock.sendto(str(next_seq_num).zfill(10).encode() + b'', addr)
    sock.close()
    # 计算传输时间、平均速度、丢包率和重传率
    transmission_time = time.time() - start_time
    average_speed = total_bytes_sent / transmission_time
    packet_loss_rate = lost_packets / total_packets_sent
    retransmission_rate = retransmitted_packets / total_packets_sent

    # 打印结果
    print('Transmission Time: %.3f seconds' % transmission_time)
    print('Average Speed: %.2f bytes/second' % average_speed)
    print("Packet loss rate: ", packet_loss_rate)
    print("Packet retransmission rate: ",retransmission_rate)
    print((len(data) - 1) // buffer_size + 1)