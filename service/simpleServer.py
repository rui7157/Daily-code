#coding:utf-8

import socket
listen_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
listen_socket.bind(("",8888))
listen_socket.listen(1)

while 1:

    connect,addrs = listen_socket.accept()
    request=connect.recv(1024)
    print ">>>",request
    print "*"*30
    httpresponse="""HTTP/1.1 200 OK
    
<html><head></head><body><h1>hello world!</h1>
    </body></html>
    """
    connect.sendall(httpresponse)
    connect.close()


