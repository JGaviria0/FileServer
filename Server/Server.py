import time
import zmq
import base64
import os
import hashlib
import sys
from dotenv import load_dotenv

load_dotenv()
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
BUF_SIZE = os.getenv('BUF_SIZE')
sys.path.insert(0, PRINCIPAL_PATH)
from util import hashing

# From: https://zeromq.org/get-started/?language=python&library=pyzmq#
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
dicHash = {}
dicnames = {}
actualname = {}

def upload(fileName):
    #from: https://docs.python.org/es/3/library/base64.html 
    try: 
        message = socket.recv()
        f = open(f"Files/{fileName}", 'wb')
         #decode the file
        f.write(message)
        f.close()
        with open(f'Files/{fileName}',"rb") as en:
            bytes = en.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest();
            if readable_hash in actualname:
                f = open(f"hashTable.txt", 'a')
                f.write(f'{fileName}//{readable_hash}\n')
                f.close()
                dicnames[fileName] = readable_hash
                os.remove(f'Files/{fileName}')
        time.sleep(1)
        # socket.send(f"File upload succesfully as {fileName}".encode())
        socket.send_multipart
        print(f"{fileName} upload succesfully")

    except: 
        err = "Error uploading file name, unexpected error"
        print(err)
        socket.send(err.encode())


def dowload(fileName):
    
    newfile = actualname[dicnames[fileName]]

    try: 
        f = open(f"Files/{newfile}" ,'rb')
        bytes = bytearray(f.read())
        strng = base64.b64encode(bytes)
        socket.send(strng)
        f.close()
    except:
        print("Error downloading file, maybe it doesn't exist or you are using a wrong extension")
        return
def hashfile(fname):
    sha1 = hashlib.sha1()

    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def createlist(newfilename):
    path = f"./{newfilename}"
    f = open('Files/list.txt', 'wb')
    obj = os.scandir(path)
    files = {}
    for entry in obj:
        # if entry.is_dir() or entry.is_file():
            f.write(f" - {entry.name}\n".encode())
            readable_hash = ""
            #https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
            with open(f'Files/{entry.name}',"rb") as en:
                bytes = en.read() # read entire file as bytes
                readable_hash = hashlib.sha256(bytes).hexdigest();
            files[readable_hash] = entry.name
            
    f.close()
    global actualname
    actualname = files
    return files

def newhashTable():
    global dicHash
    os.remove('./hashTable.txt')
    f = open('hashTable.txt', 'a')
    for hash in dicHash:
        for name in dicHash[hash]:
            f.write(f'{name}//{hash}\n')

    f.close()

def hashTableCheck():
    global dicHash
    global dicnames
    files = createlist('Files')
    
    f = open('hashTable.txt', 'r')
    newFiles = 0
    deleteFiles = 0
    for line in f: 
        filename, hash = line.split('//')
        hash = hash[:-1]
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

    newhashTable()
    hashing.newhashTablejson(dicnames)

def makealist():
    names = []
    for name in dicnames:
        names.append(name)
    names.sort()
    me = '''\n\n'''
    for name in names:
        me += f' - {name}\n'

    return me

def main():

    hashTableCheck()
    while True:    

        # try: 
        message1 = socket.recv()
        newfilename = message1.decode('ascii')
        filename = message1.decode().split('//')
        print(newfilename)
        newfilename = filename[1]

        # except: 
        #     err = "Error selecting a file name, file name invalid"
        #     print(err)
        #     socket.send(err.encode())
        


        if filename[0] == "upload":
            socket.send(b"Trying to upload the new file")
            upload(newfilename)
            continue
        
        if filename[0] == "download":
            dowload(newfilename)
            message = socket.recv().decode()
            print(message)
            socket.send(b'ok')
            continue

        if filename[0] == 'list':
            # createlist(newfilename)
            # dowload('list.txt')
            # os.remove("./Files/list.txt")
            me = makealist()
            socket.send(me.encode())

main()