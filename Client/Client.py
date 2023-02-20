import zmq
import base64
import sys
import time
import os

def createlist():
    path = ""
    obj = os.scandir()
    files = []
    for entry in obj:
        if entry.is_dir() or entry.is_file():
            files.append(entry.name)
    return files

def chooseFileName(filename):

    files = createlist()
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

def upload(socket, fileName): 

    try: 
        file = f"upload//{fileName}".encode('ascii')
        socket.send(file)

    except: 
        print('Error in file name, try again.')
        return

    message = socket.recv().decode()
    print(message)

    if message[:5] == "Error":
        return 

    try: 
        f = open(fileName ,'rb')
        bytes = f.read()
        #strng = base64.b64encode(bytes)
        socket.send(bytes)
        f.close()
    except:
        print("Error uploading file, maybe it doesn't exist or you're using a wrong extention")
        return

    message = socket.recv()
    print(message.decode())

def dowload(socket, fileName):

    try: 
        file = f"download//{fileName}".encode('ascii')
        socket.send(file)
        newfilename = fileName

    except: 
        print('Error in file name, try again.')
        return

    newfilename = chooseFileName(fileName)

    if newfilename != fileName :
        print("New name: ", newfilename)

    try: 
        message = socket.recv()
        f = open(newfilename, 'wb')
        ba = bytearray(base64.b64decode(message))
        f.write(ba)
        f.close()
        time.sleep(1)
        message = f'{newfilename} Succesfull download'
        socket.send(message.encode())
        print(f"{newfilename} Succesfull download")

    except: 
        err = "Error downloading file name, unexpected error"
        print(err)
        socket.send(err.encode())

def thelist(socket, fileName):

    try: 
        fileName = f"Files/{fileName}" 
        file = f"list//{fileName}".encode('ascii')
        socket.send(file)

    except: 
        print('Error in file name, try again.')
        return

    try: 
        message = socket.recv()
        print(message.decode())
        # ba = base64.b64decode(message)
        # print("\n")
        # print( ba.decode())

    except: 
        err = "Error downloading file name, unexpected error"
        print(err)
        socket.send(err.encode())

    

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

    if type == 'upload':
        upload(socket, fileName)
        return 
    
    if type == 'download':
        dowload(socket, fileName)
        return

    if type == 'list':
        thelist(socket, fileName)
        return

    print("You didn't use the correct sintax")
main()