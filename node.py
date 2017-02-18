import socket, select, threading, time, string

class Node(object):
    busy_nodes = []
    def __init__(self,port,connected_nodes):
        self.node = socket.socket(family=AF_INET,type=SOCK_DGRAM)
        self.node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.port = port
        self.hostname = socket.gethostname()
        self.node.bind((self.hostname,self.port))

        self.connected_nodes = connected_nodes

        print "Node created at port: {0}".format(self.port)

        self.locked = False
        self.timer = 0

    def run(self):
        count = 0
        busy_neighbour = []
        for node in connected_nodes:
            if node not in busy_nodes:
                count += 1
            else:
                busy_neighbour.append(node)

        if count == 2:
            self.lock_resources()
        else:
            for node in busy_neighbour:
                threading.Thread(target=self.request_resources,args=(node,)).start()

    def request_resources(self,address):
        self.node.sendto("node:{0} requesting resources...".format(self.port),(self.hostname,address))

    def receive_requests(self):
        request, address = self.node.recvfrom(512)
        if string.find(request,"requesting",0,len(request)) > -1:
            status_response(address)
        elif string.find(request,"locked",0,len(request)) > -1:
            time.sleep(1)
            threading.Thread(target=self.request_resources,args=(node,)).start()
        elif string.find(s,"released",0,len(request))>-1:
            Node.busy_nodes.remove(address)
            self.run()

    def lock_resources(self):
        self.locked = True
        threading.Thread(target=self.receive_requests).start()
        threading.Thread(target=self.start_timer).start()

    def status_response(self,address):
        if not self.get_timer():
            self.node.sendto("resources locked by Node: {0}".format(self.port),(self.hostname,address))
        else:
            self.release_resources(address)

    def release_resources(self,address):
        self.locked = False
        Node.busy_nodes.remove(self.node)
        self.node.sendto("resources released by Node: {0}".format(self.port),(self.hostname,address))

    def start_timer(self):
        while(self.timer != 15):
            time.sleep(1)
            self.timer += 1
        self.reset()

    def get_timer(self):
        return self.timer == 15 ? True : False
