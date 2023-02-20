import json

def newhashTablejson(dichash):
    with open("hashTable.json", "w") as outfile:
        json.dump(dichash, outfile)