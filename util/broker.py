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
context = zmq.Context()



def sendChunk(bytes, socket, ip, port, hs, size, npart):

    hash = hashlib.sha256()
    hash.update(bytes)
    hashPart = hash.hexdigest()

    fullFileName = hs["Name"].split('.')
    fielName = f"{fullFileName[0]}{npart}"
    hsJSON = header.sendChunkHeader(fielName, hashPart, size)
    headerJSON = json.dumps(hsJSON).encode()

    socket.send_multipart([headerJSON, bytes])
    message = socket.recv()

    print(message.decode(), end="")
    print(ip, port, fielName)
    return hashPart

def sendFile(header, Nodes):
    
    fullFileName = header["Name"]
    size = header["Size"]

    socketsNodes = []
    for pack in Nodes:
        socket = context.socket(zmq.REQ)
        socket.connect(f'tcp://{pack[0]}:{pack[1]}')
        socketsNodes.append(socket)
    print(socketsNodes)
    cs = (size // BUF_SIZE)+1
    nNodes = len(Nodes)
    hashes = []

    with open(f'{fullFileName}', 'rb') as inputFile:
        for parts in range(cs):
            bytes = inputFile.read(BUF_SIZE)
            eachsize = BUF_SIZE
            if parts == cs-1:
                eachsize = size%(BUF_SIZE)
                if cs == 0:
                    break
            whichNode = parts%nNodes
            newhash = sendChunk(bytes, socketsNodes[whichNode], Nodes[whichNode][0], Nodes[whichNode][1], header.copy(), eachsize, parts)
            hashes.append([newhash, Nodes[whichNode][0], Nodes[whichNode][1]])

    return hashes

def getFile( socket, fileName):
    # socket = context.socket(zmq.REQ)
    # socket.connect(f'tcp://{ip}:{port}')

    hs = header.getFile(fileName)
    headerJSON = json.dumps(hs).encode()

    socket.send_multipart([headerJSON, headerJSON])

    headerJSON, bytes = socket.recv_multipart()

    return bytes
    