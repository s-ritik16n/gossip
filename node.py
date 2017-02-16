import socket, select, threading

class Node(object):
    def __init__(self,port):
        self.node = socket.socket(family=AF_INET,type=SOCK_DGRAM)
        self.port = port
        self.hostname = socket.gethostname()
        self.node.bind((self.hostname,self.port))

        self.locked = False
        self.timer = 0

        print "Node created at port: {0}".format(self.port)


    def status_response(self,address):
        if not self.get_timer():
            self.node.sendto("resources locked by {0}".format(self.port),(self.hostname,address))
        else:
            self.locked = False
            self.node.sendto("resource free",(self.hostname,address))

    def signal(self):

    def start_timer(self):
        while(self.timer != 15):
            time.sleep(1)
            self.timer += 1

    def get_timer(self):
        return self.timer==15 ? True : False

    def request_resources(self):
        pass

    def receive_requests(self):
        request, address = self.node.recvfrom(512)
        status_response(address)

    def lock_resources(self):
        self.locked = True
        threading.Thread(target=receive_requests).start()
