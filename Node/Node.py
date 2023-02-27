import time
import zmq
import random
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')

sys.path.insert(0, PRINCIPAL_PATH)
from util import hashing, socketsRepo, broker, header


context = zmq.Context()
socket = context.socket(zmq.REP)
portra = random.randint(4000, 5554)
socket.bind(f"tcp://*:{portra}")
print(portra)

def subscribe(ip, port, portra):
    contextsub = zmq.Context()
    socketsub = contextsub.socket(zmq.REQ)
    socketsub.connect(f'tcp://{ip}:{port}')

    hs = header.subscription(ip, port, portra)

    headerJSON = json.dumps(hs).encode()

    socketsub.send_multipart([headerJSON, headerJSON])

    message = socketsub.recv().decode()
    print(message)
    socketsub.close()

def main():
    _, ip, port = sys.argv
    subscribe(ip, port, portra)


    while True:
        #  Wait for next request from client
        headerJSON, binaryFile = socket.recv_multipart()
        heade = json.loads(headerJSON)
        print(heade)
        fileName = heade["Name"]

        if heade["OperationType"] == UPLOAD_TYPE:
            hash = heade["Hash"]
            print(f"upload file: {fileName} hash: {hash}")
            socketsRepo.saveFile(socket, hash, binaryFile)
            socket.send(b"Nice")
        
        if heade["OperationType"] == DOWNLOAD_TYPE:
            hs = header.createHeader(fileName, DOWNLOAD_TYPE)
            hsJSON = json.dumps(hs).encode()
            socketsRepo.sendFile(socket, fileName, hsJSON)
        

main()