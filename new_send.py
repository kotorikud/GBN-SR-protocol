import socket
import pickle
import os
import time

def send_packet(sock, seq_num, data, addr):
    sock.sendto(str(seq_num).zfill(10).encode() + data, addr)

def gbn_send():
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9000))

    # 接收客户端请求
    data, addr = sock.recvfrom(1024)
    filename = data.decode()
    print("filename",filename)

    # 数据包大小和GBN窗口大小
    packet_size = 1024
    window_size = int(input("please input window size:"))   #窗口不能太大，在进行重发时，太大会导致一段时间内传输数据包过多，缓冲区溢出，无法成功发送，也不能太小，太小会让发送速度主要受制与窗口大小，即接收方没办法大量的连续的接收数据包，大量时间浪费在cs通信中

    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"File '{filename}' not found")
        return

    # 分块读取文件并发送数据包
    seq_num = 0
    with open(filename, "rb") as file:
        data = file.read()
        packets_data = [data[i:i + packet_size] for i in range(0, len(data), packet_size)]  ##最后一个不够1024怎么处理
    

    base = 0
    next_seq_num = 0    # 发送窗口左右边界
    expected_ack = 0    # 发送方期望ACK
    packets = {}    # 窗口中每个数据包的发送时间和重传次数
    packets_lost = 0
    start_time = time.time()
    while base < len(packets_data):
        # 发送窗口内的数据包
        while next_seq_num < base + window_size and next_seq_num < len(packets_data):
            send_packet(sock, next_seq_num, packets_data[next_seq_num], addr)
            packets[next_seq_num] = {'data': packets_data[next_seq_num], 'time': time.time(), 'retries': 0}
            next_seq_num += 1



        # 接收ACK
        try:
            sock.settimeout(0.5)
            packet, addr = sock.recvfrom(10)
            ack_num = int(packet.decode())

            if ack_num >= base:
                base = ack_num + 1
                #print(f"Ack received: {ack_num}")
        except socket.timeout:
            # 检查是否有超时未收到ACK的数据包
            packets_lost += 1
            next_seq_num = base

            pass

    
   
    end_time = time.time()
    sock.close()

    # 计算传输时间，平均速度，丢包率和重传率
    time_elapsed = end_time - start_time
    file_size = len(data)
    average_speed = file_size / time_elapsed / 1024
    packets_sent = len(packets)
    packet_loss_rate = packets_lost / packets_sent
    packet_retransmission_rate = (packets_sent - packets_lost) / packets_sent

    # 打印传输信息
    print("\n\nFile transmission complete!")
    print("Time elapsed: ", time_elapsed)
    print("Average speed: ", average_speed, "KB/s")
    print("Packet loss num: ", packets_lost)
    print("Packet loss rate: ", packet_loss_rate)
    print("Packet retransmission rate: ", packet_retransmission_rate)
