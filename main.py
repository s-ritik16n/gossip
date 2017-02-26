from node import Node
import time
from pprint import pprint
import json

if __name__ == "__main__":
    philosophers = []
    with open("philosophers.json") as phils:
        philosophers = json.load(phils)
        phils.close()
    for philosopher in range(len(philosophers)):
        Node(int(philosophers[philosopher].keys()[0]),philosophers[philosopher].values()[0]).run()
