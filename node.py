import socket, select, threading, time, string

class Node(object):
    busy_nodes = []
    def __init__(self,port,connected_nodes):
        self.node = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
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
        for node in self.connected_nodes:
            print node
            if node not in Node.busy_nodes:
                count += 1
            else:
                busy_neighbour.append(node)
        print "something"
        if count == len(self.connected_nodes):
            print "inside count"
            Node.busy_nodes.append(self.node)
            self.lock_resources()
        else:
            print "inside else"
            for node in busy_neighbour:
                print "Node: {0} requesting resources from {1}...".format(self.port,node)
                threading.Thread(target=self.request_resources,args=(node,)).start()
                threading.Thread(target=self.receive_requests).start()

    def request_resources(self,address):
        print "Node:{0} requesting resources from {1}".format(self.port,address)
        self.node.sendto("Node: {0} requesting resources...".format(self.port),(self.hostname,address))

    def receive_requests(self):
        request, address = self.node.recvfrom(512)
        if string.find(request,"requesting",0,len(request)) > -1:
            self.status_response(address)
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
            print "resources locked by Node: {0}".format(self.port)
            self.node.sendto("resources locked by Node: {0}".format(self.port),address)
        else:
            self.release_resources(address)

    def release_resources(self,address):
        self.locked = False
        Node.busy_nodes.remove(self.node)
        print "resources released by Node: {0}".format(self.port)
        self.node.sendto("resources released by Node: {0}".format(self.port),address)

    def start_timer(self):
        while(self.timer != 5):
            time.sleep(1)
            self.timer += 1

    def get_timer(self):
        if self.timer >=15:
            return True
        else:
            return False
