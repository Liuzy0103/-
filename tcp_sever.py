import socket

#  最大接收字节
byte = 1024
ip_port = ('127.0.0.1', 8000)
#  1.创建服务端套接字
tcp_sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  2.绑定端口号
tcp_sever_socket.bind(ip_port)
#  3.测试监听
tcp_sever_socket.listen(5)
#  4.等待连接
service_client_socket, ip_port = tcp_sever_socket.accept()
#  5.接收客户端数据
recv_data = service_client_socket.recv(byte).decode('GBK')
print('接收', recv_data)
#  6.向客户端发送数据
service_client_socket.send('我是服务器'.encode('gbk'))
#  7.关闭套接字
service_client_socket.close()
tcp_sever_socket.close()