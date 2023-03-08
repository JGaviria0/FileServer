import zmq
import sys
import os
from dotenv import load_dotenv
import json

load_dotenv()
# env variables
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
GET_DATA_TYPE = os.getenv('GET_DATA_TYPE')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')

# Modules
sys.path.insert(0, PRINCIPAL_PATH)
from util import header, socketsRepo, broker

def getData(socket, fileName):
    # try:
    hs = header.getDataHeader(fileName, GET_DATA_TYPE, path="")
    hsJSON = json.dumps(hs).encode()
    socket.send(hsJSON)
    response = socket.recv().decode()
    print(response)
    resposeJSON = json.loads(response)
    return hs, resposeJSON
    # except Exception as e: 
    #     print(e)
    #     print("Error geting nodes data")

def upload(socket, headerJSON, res):    
    hashes = broker.sendFile(headerJSON, res["Nodes"])
    hs = header.fileSavedHeader(hashes, headerJSON)
    hsJSON = json.dumps(hs).encode()
    socket.send(hsJSON)

    response = socket.recv().decode()
    print(response)

def download(socket, fileName):

    hs = header.getFile(fileName)
    hsJSON = json.dumps(hs).encode()
    socket.send_multipart([hsJSON, hsJSON])
    _, bytes = socket.recv_multipart()
    try: 
        fileName, ext = fileName.split('.')
    except:
        ext = ""
    res = socketsRepo.saveFile( f'{fileName}2.{ext}', bytes, path="") 
    print(res)   

def thelist(socket, fileName): 
    try: 
        hs = header.getList()
        hsJSON = json.dumps(hs).encode()
        socket.send_multipart([hsJSON, hsJSON])
        message = socket.recv()
        print(message.decode())
    except: 
        print("Error list the files.")

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
        head, res = getData(socket, fileName)
        upload(socket, head, res)
        return 
    
    if type == DOWNLOAD_TYPE:
        download(socket, fileName)
        return

    if type == LIST_TYPE:
        thelist(socket, fileName)
        return

    print("You didn't use the correct sintax")
main()