import zmq
import os
import json
import hashlib
from dotenv import load_dotenv
from util import header

load_dotenv()
NODES_PORT = os.getenv('NODES_PORT')
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')


def sendChunk(bytes, ip, port, header, size, npart):
    ip = "localhost"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://{ip}:{port}')
    hash = hashlib.sha256()
    hash.update(bytes)
    hashPart = hash.hexdigest()
    fullFileName = header["Name"].split('.')
    header["Name"] = f"{fullFileName[0]}{npart}"
    header["Hash"] = hashPart
    header["Size"] = size
    headerJSON = json.dumps(header).encode()
    socket.send_multipart([headerJSON, bytes])
    return hashPart

def sendFile(header, Nodes):
    fullFileName = header["Name"]
    size = header["Size"]

    servers = len(Nodes)
    cs = size // (servers-1)

    hashes = []
    nParts = 0
    with open(f'{MAIN_DIRECTORY}{fullFileName}', 'rb') as inputFile:
        for ip in Nodes:
            nParts += 1
            bytes = inputFile.read(cs)
            if nParts == servers:
                cs = size%(servers-1)
                if cs == 0:
                    break
            newhash = sendChunk(bytes, ip[0], ip[1], header.copy(), cs, nParts)
            hashes.append([newhash, ip[0], ip[1]])

    return hashes

def getFile(ip, port, fileName):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://{ip}:{port}')

    hs = header.getFile(fileName)
    headerJSON = json.dumps(hs).encode()

    socket.send_multipart([headerJSON, headerJSON])

    headerJSON, message = socket.recv_multipart()

    return message
    