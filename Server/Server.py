import time
import zmq
import sys
import json
import os
from dotenv import load_dotenv

load_dotenv()
PRINCIPAL_PATH = os.getenv('PRINCIPAL_PATH')
UPLOAD_TYPE = os.getenv('UPLOAD_TYPE')
DOWNLOAD_TYPE = os.getenv('DOWNLOAD_TYPE')
LIST_TYPE = os.getenv('LIST_TYPE')
SUBSCRIPTION_TYPE = os.getenv('SUBSCRIPTION_TYPE')
# BUF_SIZE = os.getenv('BUF_SIZE')

sys.path.insert(0, PRINCIPAL_PATH)
from util import hashing, socketsRepo, broker
from util import header as hs

# From: https://zeromq.org/get-started/?language=python&library=pyzmq#
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

dicNames = {}
dicHash = {}
dicFilesUpload = {}

def upload(socket, header, binaryFile, Nodes):
    global dicFilesUpload
    global dicNames
    global dicHash
    # try:
    print(f'Saving file {header["Name"]} with hash {header["Hash"]} and size of {header["Size"]}.')
    
    dicNames[header["Name"]] = header["Hash"]
    if header["Hash"] in dicFilesUpload:
        socket.send((f'{header["Name"]} Uploading').encode())
        return
    dicHash[header["Hash"]] = header["Name"]
    message = socketsRepo.saveFile(socket, header["Name"], binaryFile)
    socket.send((f'{header["Name"]} {message}').encode())
    parts = broker.sendFile(header, Nodes)
    dicFilesUpload[header["Hash"]] = parts

    # except:
    #     print("Error Uploading the file")
    #     socket.send((f'{header["Name"]} Error uploading').encode())

def download(socket, header):
    # try: 
    print(dicNames)
    hash = dicNames[header["Name"]]
    totalBytes = b''
    for parts in dicFilesUpload[hash]:
        fileName, ip, port = parts
        bytes = broker.getFile(ip, port, fileName)
        totalBytes += bytes
    newhs = hs.getFile(header["Name"])
    hsJSON = json.dumps(newhs).encode()
    socket.send_multipart([hsJSON, totalBytes])

    
def main():
    
    Nodes = []
        
    while True: 

        headerJSON, binaryFile = socket.recv_multipart()
        header = json.loads(headerJSON)

        if header["OperationType"] == UPLOAD_TYPE:
            upload(socket, header, binaryFile, Nodes)
        
        if header["OperationType"] == DOWNLOAD_TYPE:
            download(socket, header)
        
        if header["OperationType"] == SUBSCRIPTION_TYPE:
            Nodes.append([header["Ip"], header["Port"]])
            print(f'New node IP: {header["Ip"]} and port: {header["Port"]}')
            socket.send(b"Subscribed succesfully.")

main()