from node import Node
import time
from pprint import pprint
import json

if __name__ == "__main__":
    d = []
    with open("philosophers.json") as phils:
        d = json.load(phils)
        phil.close()
    node = Node(2525,[2230,2235])
    node.run()
    time.sleep(3)
    node = Node(2230,[2525])
    node.run()
    node.request_resources(2525)
