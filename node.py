import socket, select, threading

class Node(object):
    busy_nodes = []
    def __init__(self,port,connected_nodes):
        self.node = socket.socket(family=AF_INET,type=SOCK_DGRAM)
        self.port = port
        self.hostname = socket.gethostname()
        self.node.bind((self.hostname,self.port))

        self.locked = False
        self.timer = 0
        self.connected_nodes = connected_nodes

        print "Node created at port: {0}".format(self.port)


    def status_response(self,address):
        if not self.get_timer():
            self.node.sendto("resources locked by {0}".format(self.port),(self.hostname,address))
        else:
            self.release_resources()

    def release_resources(self):
        self.locked = False
        Node.busy_nodes.remove(self.node)

    def start_timer(self):
        while(self.timer != 15):
            time.sleep(1)
            self.timer += 1
        self.locked = True

    def get_timer(self):
        return self.timer==15 ? True : False

    def request_resources(self):
        pass

    def receive_requests(self):
        request, address = self.node.recvfrom(512)
        status_response(address)

    def lock_resources(self):
        for node in self.connected_nodes:
            if node not in Node.busy_nodes:
                self.locked = True
                threading.Thread(target=receive_requests).start()
            else:
                #busy_wait
