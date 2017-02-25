import socket, select, threading, time, string
from clint.textui import puts, colored, indent

class Node(object):
    busy_nodes = []
    infected_nodes=[]
    def __init__(self,port,connected_nodes):
        self.node = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        self.node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.port = port
        self.hostname = socket.gethostname()
        if len(Node.busy_nodes) <= 0:
            puts(colored.cyan("\n\n---Server running on {0}---".format(self.hostname)))
        self.node.bind((self.hostname,self.port))
        self.connected_nodes = connected_nodes

        with indent(4, quote='>>'):
            puts(colored.yellow("Node created at port: {0}".format(self.port)))

        self.locked = False
        self.timer = 0

    def run(self):
        count = 0
        busy_neighbour = []
        for node in self.connected_nodes:
            if node not in Node.busy_nodes:
                count += 1
            else:
                busy_neighbour.append(node)
        if count == len(self.connected_nodes):
            Node.busy_nodes.append(self.node)
            self.lock_resources()
        else:
            print "inside else"
            for node in busy_neighbour:
                time.sleep(1)
                with indent(4, quote='>>'):
                    puts(colored.yellow("Node: {0} requesting resources from {1}...".format(self.port,node)))
                threading.Thread(target=self.request_resources,args=(node,)).start()
                threading.Thread(target=self.receive_requests).start()

    def request_resources(self,address):
        time.sleep(1)
        with indent(4, quote='>>'):
            puts(colored.yellow("Node: {0} requesting resources from {1}...".format(self.port,address)))
        self.node.sendto("Node: {0} requesting resources...".format(self.port),(self.hostname,address))

    def receive_requests(self):
        while True:
            request, address = self.node.recvfrom(512)
            if string.find(request,"requesting",0,len(request)) > -1:
                self.status_response(address)
            elif string.find(request,"locked",0,len(request)) > -1:
                time.sleep(1)
                threading.Thread(target=self.request_resources,args=(address[1],)).start()
            elif string.find(request,"released",0,len(request))>-1:
                self.run()

    def lock_resources(self):
        self.locked = True
        threading.Thread(target=self.receive_requests).start()
        threading.Thread(target=self.start_timer).start()

    def status_response(self,address):
        time.sleep(1)
        if not self.get_timer():
            with indent(4, quote='>>'):
                puts(colored.red("resources locked by Node: {0}".format(self.port)))
            self.node.sendto("resources locked by Node: {0}".format(self.port),address)
        else:
            with indent(4, quote='>>'):
                puts(colored.green("Resource released by Node:{0}".format(self.port)))
            self.release_resources(address)

    def release_resources(self,address):
        self.locked = False
        Node.busy_nodes.remove(self.node)
        time.sleep(1)
        with indent(4, quote='>>'):
            puts(colored.green("Resource released by Node:{0}".format(self.port)))
        self.node.sendto("resources released by Node: {0}".format(self.port),address)

    def start_timer(self):
        while(self.timer != 5):
            time.sleep(1)
            self.timer += 1

    def get_timer(self):
        if self.timer >=5:
            return True
        else:
            return False
