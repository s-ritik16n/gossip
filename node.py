import socket, select, threading, time, string, sys, os, signal
from clint.textui import puts, colored, indent

class Node(object):

    busy_nodes = []
    infected_nodes=[]
    count = 0
    def __init__(self,port,connected_nodes):
        self.node = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        self.node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.port = port
        self.hostname = socket.gethostname()
        if len(Node.busy_nodes) <= 0:
            puts(colored.cyan("\n\n---Server running on {0}---\n".format(self.hostname)))
        self.node.bind((self.hostname,self.port))
        self.connected_nodes = connected_nodes
        self.locked_resources = 0
        Node.count += 1

        with indent(4,quote=">>"):
            puts(colored.yellow("Node created at port: {0}".format(self.port)))

        self.locked = False
        self.timer = 0
        threading.Thread(target=self.receive_requests,name="receiver").start()

    def check_count(self):
        if (len(Node.busy_nodes) <= 0) and len(Node.infected_nodes) >= Node.count:
            os.kill(os.getpid(), signal.SIGHUP)

    def run(self,grab_from=None):
        count = 0
        busy_neighbour = []
        for node in self.connected_nodes:
            if (node not in Node.busy_nodes):
                count += 1
            else:
                busy_neighbour.append(node)
        if count == len(self.connected_nodes):
            Node.busy_nodes.append(self.port)
            self.lock_resources(grab_from)
        else:
            for node in busy_neighbour:
                if node not in Node.infected_nodes:
                    self.request_resources(node)

    def request_resources(self,address):
        time.sleep(1)
        with indent(8,quote=">>"):
            puts(colored.yellow("Node: {0} requesting resources from {1}...".format(self.port,address)))
        self.node.sendto("requesting",(self.hostname,address))

    def receive_requests(self):
        while True:
            request, address = self.node.recvfrom(512)
            time.sleep(0.5)
            if string.find(request,"requesting",0,len(request)) > -1:
                self.status_response(address)
            elif string.find(request,"locked",0,len(request)) > -1:
                time.sleep(1)
                self.run()
            elif string.find(request,"released",0,len(request))>-1:
                self.run(grab_from=address[1])

    def lock_resources(self,grab_from):
        self.locked = True
        with indent(4,quote=">>"):
            if(grab_from is not None):
                self.locked_resources += 1
                puts(colored.blue("Node: {0} locking resource released by Node: {1}".format(self.port,grab_from)))
                if self.locked_resources != 2:
                    self.request_resources(grab_from)
            else:
                self.locked_resources = 2
                puts(colored.blue("Node: {0} locking resources".format(self.port)))
                threading.Thread(target=self.start_timer).start()

    def status_response(self,address):
        time.sleep(1)
        if not self.get_timer():
            with indent(8,quote=">>"):
                puts(colored.red("@Node{0}: Resources locked by Node: {1}".format(address[1],self.port)))
            self.node.sendto("locked",address)
        else:
            self.release_resources(address)

    def release_resources(self,address):
        self.locked = False
        self.locked_resources = 0
        if self.port in Node.busy_nodes:
            Node.busy_nodes.remove(self.port)
        if self.port not in Node.infected_nodes:
            Node.infected_nodes.append(self.port)
        print "infected nodes: "+str(Node.infected_nodes)
        print "busy nodes: "+str(Node.busy_nodes)
        self.check_count()
        time.sleep(1)
        with indent(4,quote=">>"):
            puts(colored.green("Resource released by Node: {0}".format(self.port)))
        self.node.sendto("released",address)

    def start_timer(self):
        while(self.timer != 5):
            time.sleep(1)
            self.timer += 1

    def get_timer(self):
        if self.timer >=5:
            return True
        else:
            return False
