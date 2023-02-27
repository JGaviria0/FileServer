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
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def getList(): 
    header = {
        "OperationType": LIST_TYPE,
    }

    return header

def createHeader( fileName, operationType, hash="", path=MAIN_DIRECTORY ):
    fileSize = os.path.getsize(f"{path}{fileName}")
    if hash == "":
        hash = hashing.hashfile(fileName, path)

    #https://www.c-sharpcorner.com/blogs/how-to-find-ip-address-in-python
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    
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
    
    # https://www.c-sharpcorner.com/blogs/how-to-find-ip-address-in-python
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    print(IPAddr)

    header = {
        "OperationType" : SUBSCRIPTION_TYPE,
        "Ip": IPAddr,
        "Port": portra
    }

    return header

def getFile(fileName):

    header = {
        "OperationType" : DOWNLOAD_TYPE,
        "Name": fileName
    }

    return header