import socket
import struct
import multiprocessing
import os
import time
import errno

try:
   import cPickle as pickle
except:
   import pickle

def __recvall(sock, n):
    data = b''
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK or e.args[0] == errno.EAGAIN:
                continue
            return None
    return data

def sendObject(sock, obj):
    packet = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
    sock.sendall(struct.pack('>I', len(packet))+packet)

def recevieObject(sock):
    raw_msglen = __recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    msg = __recvall(sock, msglen)
    if not msg:
        return None
    return pickle.loads(msg)

class RegisterThread:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.cores = multiprocessing.cpu_count()
        self.load = os.getloadavg()
