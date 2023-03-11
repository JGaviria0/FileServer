import zmq
import sys
import os
from dotenv import load_dotenv
import json

load_dotenv()
# env variables
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
GET_UPLOAD_DATA_TYPE = os.getenv('GET_UPLOAD_DATA_TYPE')
GET_DOWNLOAD_DATA_TYPE = os.getenv('GET_DOWNLOAD_DATA_TYPE')
FILE_DOESNT_EXITS_CODE = os.getenv('FILE_DOESNT_EXITS_CODE')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')
FILE_ALREADY_EXITS_CODE = os.getenv('FILE_ALREADY_EXITS_CODE')

# Modules
sys.path.insert(0, PRINCIPAL_PATH)
from util import header, socketsRepo, broker
context = zmq.Context()

def getDataUpload(socket, fileName):
    try:
        hs = header.getDataHeader(fileName, GET_UPLOAD_DATA_TYPE, path="")
        hsJSON = json.dumps(hs).encode()
        socket.send(hsJSON)
        response = socket.recv().decode()
        print(response)
        resposeJSON = json.loads(response)
        return hs, resposeJSON
    except Exception as e: 
        print(e)
        print("Error geting nodes data")

def upload(socket, headerJSON, res):    
    if res["Response"] == FILE_ALREADY_EXITS_CODE:
        print("The file already exist.")
        return
    hashes = broker.sendFile(headerJSON, res["Nodes"])
    hs = header.fileSavedHeader(hashes, headerJSON)
    hsJSON = json.dumps(hs).encode()
    socket.send(hsJSON)

    response = socket.recv().decode()
    print(response)

def getDataDownload(socket, fileName): 
    try:
        hs = header.getDataHeader(fileName, GET_DOWNLOAD_DATA_TYPE, path="")
        print(hs)
        hsJSON = json.dumps(hs).encode()
        socket.send(hsJSON)
        response = socket.recv().decode()
        print(response)
        resposeJSON = json.loads(response)
        return hs, resposeJSON  
    except Exception as e: 
        print(e)
        print("Error geting download data")

def download(head, res):

    ips = {}

    for parts in res["Parts"]:
        key = f"{parts[1]}:{parts[2]}"
        if not key in ips: 
            socket = context.socket(zmq.REQ)
            socket.connect(f"tcp://{key}")
            ips[key] = socket

    print (ips)

    totalBytes = b"" 
    for parts in res["Parts"]:
        fileName, ip, port = parts
        print(parts)
        key = f"{ip}:{port}"
        bytes = broker.getFile(ips[key], fileName)
        totalBytes += bytes
    
    try: 
        fileName, ext = head["Name"].split('.')
    except:
        ext = ""
    res = socketsRepo.saveFile( f'{fileName}2.{ext}', totalBytes, path="") 
    print(res)   

def thelist(socket, fileName): 
    try: 
        hs = header.getList()
        hsJSON = json.dumps(hs).encode()
        socket.send( hsJSON)
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

    #  Socket to talk to server
    print("Connecting to the file server…")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{ip}:{port}")

    if type == UPLOAD_TYPE:
        head, res = getDataUpload(socket, fileName)
        upload(socket, head, res)
        return 
    
    if type == DOWNLOAD_TYPE:
        head, res = getDataDownload(socket, fileName)
        download(head, res)
        return

    if type == LIST_TYPE:
        thelist(socket, fileName)
        return

    print("You didn't use the correct sintax")
main()