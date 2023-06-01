import socket
import time

def gbn_send():
    # 文件名和接收方的IP地址和端口号
    file_name = "1.png"
    

    # 数据包大小和GBN窗口大小
    packet_size = 1024
    window_size = int(input("please input the window size:"))


    # 建立套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client_socket.settimeout(1)
    client_socket.bind(('0.0.0.0',8002))

    data, client_addr = client_socket.recvfrom(1024)
     
    # 打开文件并分割成数据包
    with open(file_name, "rb") as file:
        data = file.read()
        packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
        
    # 发送数据包
    base = 0
    next_seq_num = 0
    packets_lost = 0
    start_time = time.time()
    while base < len(packets):
        # 发送窗口内的数据包
        while next_seq_num < base + window_size and next_seq_num < len(packets):
            packet = packets[next_seq_num]
            
            client_socket.sendto(str(next_seq_num).zfill(10).encode() + packet, client_addr)
            next_seq_num += 1

        # 接收确认消息，如果没有接收到，重新发送窗口内的数据包
        try:
            client_socket.settimeout(1)
            ack, _ = client_socket.recvfrom(1024)
            ack = int(ack.decode())
            print("Received ACK with seq num: ", (ack % 1024),base,next_seq_num)
            if ack >= base :
                flag  = base // 1024
                base = ack + 1
            #else:
                #packets_lost += 1
                #next_seq_num = base
        except socket.timeout:
            print("Timeout, resending packets")
            packets_lost += 1
            next_seq_num = base

    end_time = time.time()
    client_socket.close()

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

    #if __name__ == '__main__':
    # select = input("please input(0->GBN,  1->SR):")
        #if select = 0:
            
