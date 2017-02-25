from pprint import pprint
import json

with open("philosophers.json") as phil:
    d = json.load(phil)
    phil.close()
    pprint(d)
    
