import os
from dotenv import load_dotenv

load_dotenv()
MAIN_DIRECTORY = os.getenv('MAIN_DIRECTORY')

def sendFile(socket, fileName, header, path=MAIN_DIRECTORY):
    print(f"{path}{fileName}")
    f = open(f"{path}{fileName}" ,'rb')
    bytes = f.read()
    socket.send_multipart([header, bytes])

def saveFile(socket, fileName, binaryFile, path=MAIN_DIRECTORY):
    # try:
        f = open(f"{path}{fileName}", 'wb')
        f.write(binaryFile)
        f.close()
        return "Saving succesfully."
    # except:
    #     print("Error saving file.")
    #     return ": Error saving the file."
