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
SEND_TYPE = os.getenv('SEND_TYPE')

sys.path.insert(0, PRINCIPAL_PATH)
from util import socketsRepo, header

context = zmq.Context()


def subscribe(ip, port, portra):
    try: 
        socketsub = context.socket(zmq.REQ)
        socketsub.connect(f'tcp://{ip}:{port}')

        hs = header.subscription(ip, port, portra)

        headerJSON = json.dumps(hs).encode()
        socketsub.send(headerJSON)
        
        message = socketsub.recv().decode()
        print(message)
        socketsub.close()
    except Exception as e: 
        print(e)
        print("Not possible to connect to the server.")

def main():
    _, ip, port, portra = sys.argv
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{portra}")
    print(portra)
    subscribe(ip, port, portra)

    while True:
        # try: 
        headerJSON, binaryFile = socket.recv_multipart()
        heade = json.loads(headerJSON)
        print(heade)
        fileName = heade["Name"]
        # except Exception as e: 
        #     print(e)
        #     print("Error: Can't receive the file.")


        if heade["OperationType"] == SEND_TYPE:
            hash = heade["Hash"]
            print(f"upload file: {fileName} hash: {hash}")
            message = socketsRepo.saveFile(hash, binaryFile)
            socket.send(message.encode())
        
        if heade["OperationType"] == DOWNLOAD_TYPE:
            hs = header.createHeader(fileName, DOWNLOAD_TYPE)
            hsJSON = json.dumps(hs).encode()
            socketsRepo.sendFile(socket, fileName, hsJSON)
        

main()