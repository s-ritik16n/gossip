import socket, select, threading, time, string, sys, os, signal
from clint.textui import puts, colored, indent
from colorama import init, Fore, Style

init()

class Node(object):

    busy_nodes = []
    infected_nodes=[]
    count = 0
    def __init__(self,port,connected_nodes):
        sys.stdout.flush()
        self.node = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        self.node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.port = port
        self.hostname = socket.gethostname()
        if len(Node.busy_nodes) <= 0:
            sys.stdout.write(Fore.CYAN+"\n\n---Server running on {0}---\n".format(self.hostname))
        self.node.bind((self.hostname,self.port))
        self.connected_nodes = connected_nodes
        self.locked_resources = 0
        Node.count += 1

        indents(4,quote=">>")
        sys.stdout.write(Fore.LIGHTGREEN_EX+"Philosopher ID: {0}\n".format(self.port))
        self.locked = False
        self.dead = False
        self.timer = 0
        threading.Thread(target=self.receive_requests,name="receiver").start()

    def check_count(self):
        if len(Node.infected_nodes) == Node.count:
            threading.Thread(target=self.kill).start()

    def kill(self):
        sleep = 0
        while sleep != 5:
            time.sleep(1)
            sleep += 1
        os.kill(os.getpid(),signal.SIGTERM)

    def run(self,grab_from=None):
        count = 0
        busy_neighbour = []
        if grab_from is None:
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
        else:
            self.lock_resources(grab_from)

    def request_resources(self,address):
        time.sleep(1)
        indents(8,quote=">>")
        sys.stdout.write(Fore.LIGHTYELLOW_EX+"Philiosopher {0} requesting fork from Philosopher {1}...\n".format(self.port,address))
        self.node.sendto("requesting",(self.hostname,address))

    def receive_requests(self):
        while self.dead != True:
            request, address = self.node.recvfrom(512)
            time.sleep(0.5)
            if string.find(request,"requesting",0,len(request)) > -1:
                self.status_response(address)
            elif string.find(request,"locked",0,len(request)) > -1:
                time.sleep(1)
                self.run()
            elif string.find(request,"released",0,len(request))>-1:
                if address[1] in self.connected_nodes:
                    self.connected_nodes.remove(address[1])
                self.run(grab_from=address[1])

    def lock_resources(self,grab_from):
        self.locked = True
        indents(4,quote=">>")
        if(grab_from is not None):
            self.locked_resources += 1
            sys.stdout.write(Fore.LIGHTBLUE_EX+"Philisopher: {0} picked fork released by Philospher: {1}\n".format(self.port,grab_from))
            if self.locked_resources != 2:
                self.run()
            else:
                threading.Thread(target=self.start_timer).start()
        else:
            self.locked_resources = 2
            sys.stdout.write(Fore.LIGHTBLUE_EX+"Philosopher: {0} picked forks to eat\n".format(self.port))
            threading.Thread(target=self.start_timer).start()

    def status_response(self,address):
        if not self.get_timer():
            indents(8,quote=">>")
            sys.stdout.write(Fore.RED+"@Philosopher {0}: Philospher {1} is still eating...\n".format(address[1],self.port))
            self.node.sendto("locked",address)
        else:
            self.release_resources()
            indents(4,quote=">>")
            sys.stdout.write(Fore.LIGHTGREEN_EX+"Fork released by Philosopher: {0}\n".format(self.port))
            self.node.sendto("released",address)

    def release_resources(self):
        self.locked = False
        self.dead = True
        self.locked_resources = 0
        sys.stdout.write(Fore.LIGHTGREEN_EX+"Fork released by Philosopher: {0}\n".format(self.port))
        if self.port in Node.busy_nodes:
            Node.busy_nodes.remove(self.port)
        if self.port not in Node.infected_nodes:
            Node.infected_nodes.append(self.port)
        self.check_count()
        indents(4,quote=">>")
        sys.stdout.write(Fore.LIGHTBLUE_EX+"Philosophers finished eating: "+str(Node.infected_nodes)+"\n")
        indents(4,quote=">>")

    def start_timer(self):
        while(self.timer != 5):
            time.sleep(1)
            self.timer += 1
        self.release_resources()

    def get_timer(self):
        if self.timer >=5:
            return True
        else:
            return False

def indents(num,quote):
    return
