import os
import zmq
from util import hashing
import socket
import json
from dotenv import load_dotenv

load_dotenv()
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')
SUBSCRIPTION_TYPE = os.getenv('SUBSCRIPTION_TYPE')
SUBSCRIPTION_TYPE = os.getenv('SUBSCRIPTION_TYPE')
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def createHeader( fileName, operationType, hash="", path=MAIN_DIRECTORY ):
    fileSize = os.path.getsize(f"{path}{fileName}")
    if hash == "":
        hash = hashing.hashfile(fileName, path)
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 
    try:
        _, ext = fileName.split('.') 
    except:
        ext = ""
    header = {
        "OperationType": operationType,
        "Name": fileName,
        "Size": fileSize,
        "Hash": hash,
        "Source": IPAddr,
        "Ext": ext
    }

    return header

def subscription(ip, port, portra):
    contextsub = zmq.Context()
    socketsub = contextsub.socket(zmq.REQ)
    socketsub.connect(f'tcp://{ip}:{port}')
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)

    header = {
        "OperationType" : SUBSCRIPTION_TYPE,
        "Ip": IPAddr,
        "Port": portra
    }

    headerJSON = json.dumps(header).encode()

    socketsub.send_multipart([headerJSON, headerJSON])

    message = socketsub.recv().decode()
    print(message)
    socketsub.close()

def getFile(fileName):

    header = {
        "OperationType" : DOWNLOAD_TYPE,
        "Name": fileName
    }

    return header

