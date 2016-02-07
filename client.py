import socket
import threading
import multiprocessing
import Action
import time

def run(hostname, port):
    s = None
    try:
        with socket.create_connection((hostname, port)) as sock:
            Action.sendObject(sock, Action.RegisterThread()) 
    except Exception as e:
        print(e)
        pass

cores = multiprocessing.cpu_count()
threads = []

run('localhost', 9999)

