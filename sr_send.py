import socket
import time

def sr_send():
    # 定义接收方的 IP 地址和端口号
    recv_ip = '123.249.11.92'
    recv_port = 8001

    # 定义文件名和缓冲区大小
    filename = '1.png'
    buffer_size = 1024

    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 设置超时时间
    timeout = int(input("please input timeout:"))
    sock.settimeout(timeout)

    # 打开文件并读取数据
    with open(filename, 'rb') as f:
        data = f.read()
    packets = [data[i:i+buffer_size] for i in range(0, len(data), buffer_size)]
    # 定义窗口大小和起始位置
    WINDOW_SIZE = int(input("please input window size:"))
    base = 0
    next_seq_num = 0

    # 定义发送窗口中每个数据包的状态
    state = [0] * ((len(data) - 1) // buffer_size + 1)

    start_time = time.time()
    total_bytes_sent = 0
    retransmitted_packets = 0
    total_packets_sent = 0
    lost_packets = 0
    sock.sendto(str(WINDOW_SIZE).zfill(10).encode(),(recv_ip,recv_port))
    while True:
        # 发送窗口中未被确认的数据包
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < len(packets):
            if state[next_seq_num] == 0:
                packet = packets[next_seq_num]
                sock.sendto(str(next_seq_num).zfill(10).encode() + packet, (recv_ip, recv_port))
                #print('Send packet:' ,next_seq_num)
                state[next_seq_num] = 1
                total_bytes_sent += buffer_size
                total_packets_sent += 1
            next_seq_num += 1

        # 接收 ACK
        try:
            packet, addr = sock.recvfrom(1024)
            ack = int(packet[:10].decode())
            if ack > base:
                #base = ack + 1
                print('Received ACK:', ack)
                state[ack] = 2
            elif ack == base:
                state[ack] = 2
                temp = ack
                sum = 0
                print('Received ACK:', ack)
                while temp < len(state) and state[temp] == 2:
                    sum  += 1
                    temp += 1
                base += sum
        except socket.timeout:
            # 超时重传未被确认的数据包
            print('Timeout')
            for i in range(base, next_seq_num):
                if state[i] == 1:
                    packet = packets[i]
                    sock.sendto(str(i).zfill(10).encode() + packet, (recv_ip, recv_port))
                    #print('Resend packet:', i)
                    retransmitted_packets += 1
                    total_bytes_sent += buffer_size
                    total_packets_sent += 1
                    lost_packets += 1
            #time.sleep(0.1)
        
        # 判断是否传输完成
        if base * buffer_size >= len(data):
            break

    # 计算传输时间、平均速度、丢包率和重传率
    transmission_time = time.time() - start_time
    average_speed = total_bytes_sent / transmission_time / 1024
    packet_loss_rate = lost_packets / total_packets_sent
    retransmission_rate = retransmitted_packets / total_packets_sent

    # 打印结果
    print('Transmission Time: %.3f seconds' % transmission_time)
    print('Average Speed: %.2f KB/second' % average_speed)
    print("Num of Resent Packet:",lost_packets)
    print("Packet loss rate: ", packet_loss_rate)
    print("Packet retransmission rate: ",retransmission_rate)

