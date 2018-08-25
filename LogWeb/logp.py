from socket import *
webLogServer ={
    "ip":"192.168.0.30",
    "port":9999
}
def logp(msg):
    msg = msg.encode()
    skt = socket(AF_INET,SOCK_DGRAM)
    skt.sendto(msg,(webLogServer["ip"],webLogServer["port"]))
    skt.close()