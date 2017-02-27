from node import Node
import time, json
from pprint import pprint
import threading
import sys
from multiprocessing import Process

if __name__ == "__main__":
    philosophers = []
    with open("philosophers.json") as phils:
        philosophers = json.load(phils)
        phils.close()
    for philosopher in range(len(philosophers)):
        Process(Node(int(philosophers[philosopher].keys()[0]),philosophers[philosopher].values()[0]).run()).start()
