import asyncore
import socket
import Action

class Handler(asyncore.dispatcher_with_send):
    
    def handle_read(self):
        action = Action.recevieObject(self)
        if not action:
            return
        print(action)
    
    def handle_close(self):
        self.close()

class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = Handler(sock)
    
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    server = Server(HOST, PORT)
    asyncore.loop()
