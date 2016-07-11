#coding:utf-8
import socket

class WSGIserver(object):

    def __init__(self):
        listen_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listen_socket.bind(("",8888))
        listen_socket.listen(1)
        self.socket_type=socket.AF_APPLETALK
        self.socket_s=socket.SOCK_STREAM
        
