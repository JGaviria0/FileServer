import json
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()
BUF_SIZE = int(os.getenv('BUF_SIZE'))
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def newhashTablejson(dichash):
    with open("hashTable.json", "w") as outfile:
        json.dump(dichash, outfile)

# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def hashfile(fname, path = MAIN_DIRECTORY):
    sha1 = hashlib.sha1()

    with open(f'{path}{fname}', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def hashTableCheck():
    dicnames = {}
    dicHash = {}
    f = open('hashTable.json')
    data = json.load(f)
    files = createlist('Files')
    newFiles = 0
    deleteFiles = 0

    for line in data: 
        filename, hash = line, data[line]
        if hash in files: 
            dicnames[filename] = hash
            if not hash in dicHash:
                dicHash[hash] = [filename]
            else:
                dicHash[hash].append(filename)
        else:
            deleteFiles += 1
    
    if newFiles or deleteFiles:
        print(f'New files: {newFiles} and Deleted files: {deleteFiles}, without using the server.')

    # newhashTable()
    newhashTablejson(dicnames)

    return dicnames, dicHash

def createlist(newfilename):
    path = f"./{newfilename}"
    f = open('Files/list.txt', 'wb')
    obj = os.scandir(path)
    files = {}
    for entry in obj:
        f.write(f" - {entry.name}\n".encode())
        readable_hash = hashfile(entry.name)
        files[readable_hash] = entry.name
            
    f.close()
    global actualname
    actualname = files
    return files