from node import Node
import time

if __name__ == "__main__":
    time.sleep(5)
    node = Node(2525,[2230,2235])
    node.run()
    time.sleep(3)
    node = Node(2230,[2525])
    node.run()
    node.request_resources(2525)
