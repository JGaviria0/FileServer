import zmq
import sys
import os
from dotenv import load_dotenv
import json

load_dotenv()
# env variables
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')

# Modules
sys.path.insert(0, PRINCIPAL_PATH)
from util import header, socketsRepo

def upload(socket, fileName):
    try:
        hs = header.createHeader(fileName, UPLOAD_TYPE, path="")
        hsJSON = json.dumps(hs).encode()
        socketsRepo.sendFile(socket, fileName, hsJSON, path="")
        response = socket.recv().decode()
        print(response)
    except: 
        print("Error uploading the file, the file doesn't exist.")

def download(socket, fileName):

    hs = header.getFile(fileName)
    hsJSON = json.dumps(hs).encode()
    socket.send_multipart([hsJSON, hsJSON])
    fullfilename, bytes = socket.recv_multipart()
    try: 
        fileName, ext = fileName.split('.')
    except:
        ext = ""
    socketsRepo.saveFile(socket, f'{fileName}2.{ext}', bytes, path="")

def main():
    try: 
        _, ip, port, type, fileName= sys.argv
    except:
        _, ip, port, type = sys.argv
        fileName = ""

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to the file server…")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")

    if type == UPLOAD_TYPE:
        upload(socket, fileName)
        return 
    
    if type == DOWNLOAD_TYPE:
        download(socket, fileName)
        return

    if type == LIST_TYPE:
        # thelist(socket, fileName)
        return

    print("You didn't use the correct sintax")
main()