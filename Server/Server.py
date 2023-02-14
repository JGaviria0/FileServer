import time
import zmq
import base64
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def chooseFileName(filename):

    files = createlist('./Files/')
    newFileName = filename
    index = 1
    try:
        filename, ext = filename.split('.')
    except:
        ext = ""

    while newFileName in files:
        newFileName = f"{filename}({index}).{ext}"
        index += 1

    return newFileName


def upload(fileName):

    newfilename = chooseFileName(fileName)
    os.remove("./Files/list.txt")

    if newfilename != fileName :
        print("New name: ", newfilename)
    try: 
        message = socket.recv()
        f = open(f"Files/{newfilename}", 'wb')
        ba = bytearray(base64.b64decode(message))
        f.write(ba)
        f.close()
        time.sleep(1)
        socket.send(f"File upload succesfully as {newfilename}".encode())
        print(f"{newfilename} upload succesfully")

    except: 
        err = "Error upload file name, An expected error"
        print(err)
        socket.send(err.encode())


def dowload(fileName):
    
    try: 
        f = open(f"Files/{fileName}" ,'rb')
        bytes = bytearray(f.read())
        strng = base64.b64encode(bytes)
        socket.send(strng)
        f.close()
    except:
        print("Error with file, maybe doesn't exist or bad extention")
        return

def createlist(newfilename):
    path = f"./{newfilename}"
    f = open('Files/list.txt', 'wb')
    obj = os.scandir(path)
    files = []
    for entry in obj:
        if entry.is_dir() or entry.is_file():
            f.write(f" - {entry.name}\n".encode())
            files.append(entry.name)
    f.close()
    return files


while True:
    try: 
        message1 = socket.recv()
        newfilename = message1.decode('ascii')
        filename = message1.decode().split('//')
        newfilename = filename[1]
        print(newfilename)

    except: 
        err = "Error selecting a file name, file name invalid"
        print(err)
        socket.send(err.encode())

    if filename[0] == "upload":
        socket.send(b"Try to upload the new file")
        upload(newfilename)
        continue
    
    if filename[0] == "download":
        dowload(newfilename)
        message = socket.recv().decode()
        print(message)
        socket.send(b'ok')
        continue

    if filename[0] == 'list':
        createlist(newfilename)
        dowload('list.txt')
        os.remove("./Files/list.txt")