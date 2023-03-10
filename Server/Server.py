from unicodedata import name
from django.http import response
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
GET_UPLOAD_DATA_TYPE = os.getenv('GET_UPLOAD_DATA_TYPE')
GET_DOWNLOAD_DATA_TYPE = os.getenv('GET_DOWNLOAD_DATA_TYPE')
FILE_SAVED = os.getenv('FILE_SAVED')

sys.path.insert(0, PRINCIPAL_PATH)
from util import hashing, socketsRepo, broker
from util import header as hs

# From: https://zeromq.org/get-started/?language=python&library=pyzmq#
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

dicNames = {}
dicFilesUpload = {}

def getDataToUpload(socket, header, Nodes):

    try:
        print(f'Get Data to save the file {header["Name"]}.')

        if header["Hash"] in dicFilesUpload:
            dicNames[header["Name"]] = header["Hash"]
            response = hs.alreadyExistHeader()
            hsJSON = json.dumps(response).encode()
            socket.send(hsJSON)
            return
        
        response = hs.sendFileHeader(Nodes)
        hsJSON = json.dumps(response).encode()
        socket.send(hsJSON)

    except Exception as e: 
        print(e)
        print("Error Uploading the file")
        socket.send((f'{header["Name"]} Error uploading').encode())

def getDataToDownload(socket, header, Nodes):

    try:
        print(f'Get Data to download the file {header["Name"]}.')

        if header["Name"] in dicNames: 
            response = hs.downloadFileHeader(dicFilesUpload[dicNames[header["Name"]]])
            hsJSON = json.dumps(response).encode()
            socket.send(hsJSON)
            return

        response = hs.DoesntExistHeader()
        hsJSON = json.dumps(response).encode()
        socket.send(hsJSON)

    except Exception as e: 
        print(e)
        print("Error geting data to the file")
        socket.send((f'{header["Name"]} Error geting data').encode())

def upload(header):
    global dicFilesUpload
    global dicNames

    print(f'Saving file {header["Name"]} with hash {header["Hash"]} and size of {header["Size"]}.')
    dicNames[header["Name"]] = header["Hash"]
    dicFilesUpload[header["Hash"]] = header["Parts"]
    socket.send(b"All sended succesfully")

# def download(socket, header):
#     try: 
#         print(dicNames)
#         hash = dicNames[header["Name"]]
#         totalBytes = b''
#         for parts in dicFilesUpload[hash]:
#             fileName, ip, port = parts
#             bytes = broker.getFile(ip, port, fileName)
#             totalBytes += bytes
#         newhs = hs.getFile(header["Name"])
#         hsJSON = json.dumps(newhs).encode()
#         socket.send_multipart([hsJSON, totalBytes])
#     except Exception as e: 
#         print(e)
#         print("Error download the file")

def makeList(socket): 
    thelist = '''\n\n'''
    for i in dicNames: 
        thelist += f" - {i}\n "
    
    socket.send(thelist.encode())
    
def main():
    
    Nodes = []
        
    while True: 
        headerJSON = socket.recv()
        header = json.loads(headerJSON)

        if header["OperationType"] == GET_UPLOAD_DATA_TYPE:
            getDataToUpload(socket, header, Nodes)

        if header["OperationType"] == GET_DOWNLOAD_DATA_TYPE:
            getDataToDownload(socket, header, Nodes)

        if header["OperationType"] == FILE_SAVED:
            upload(header)
        
        if header["OperationType"] == LIST_TYPE:
            makeList(socket)
        
        if header["OperationType"] == SUBSCRIPTION_TYPE:
            Nodes.append([header["Ip"], header["Port"]])
            print(f'New node IP: {header["Ip"]} and port: {header["Port"]}')
            socket.send(b"Subscribed succesfully.")

main()