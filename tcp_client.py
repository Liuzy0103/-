import socket
#  1.设置IP和端口号
ip_port = ('127.0.0.1', 8000)
#  创建tcp客户端套接字
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  3.和服务端建立连接
tcp_client_socket.connect(ip_port)
#  4.发送数据
send_data = '我是客户端，请求连接'.encode('GBK')
tcp_client_socket.send(send_data)
#  5.接收数据
#  定义接收的字节数
byte = 1024
recv_data = tcp_client_socket.recv(byte)
print(recv_data)
recv_data_code = recv_data.decode('GBK')
print('接收服务器的数据为', recv_data_code)
#  6.关键套接字
tcp_client_socket.close()
