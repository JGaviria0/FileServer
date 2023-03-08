import zmq
import os
import json
import hashlib
from dotenv import load_dotenv
from util import header

load_dotenv()
NODES_PORT = os.getenv('NODES_PORT')
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')
BUF_SIZE = int(os.getenv('BUF_SIZE'))


def sendChunk(bytes, ip, port, header, size, npart):
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
    print(ip, port, header["Name"])
    return hashPart

def sendFile(header, Nodes):
    
    fullFileName = header["Name"]
    size = header["Size"]
    
    cs = (size // BUF_SIZE)+1
    nNodes = len(Nodes)
    hashes = []

    with open(f'{fullFileName}', 'rb') as inputFile:
        for parts in range(cs):
            bytes = inputFile.read(BUF_SIZE)

            if parts == cs-1:
                cs = size%(BUF_SIZE)
                if cs == 0:
                    break
            whichNode = parts%nNodes
            newhash = sendChunk(bytes, Nodes[whichNode][0], Nodes[whichNode][1], header.copy(), cs, parts)
            hashes.append([newhash,  Nodes[whichNode][0], Nodes[whichNode][1]])

    return hashes

def getFile(ip, port, fileName):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://{ip}:{port}')

    hs = header.getFile(fileName)
    headerJSON = json.dumps(hs).encode()

    socket.send_multipart([headerJSON, headerJSON])

    headerJSON, bytes = socket.recv_multipart()

    return bytes
    