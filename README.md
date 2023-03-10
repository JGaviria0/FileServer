

# File server

Este proyecto esta desarrollado para la materia de Arquitectura cliente servidor de la Universidad Tecnológica de Pereira, el objetivo es subir y descargar cualquier tipo de archivo. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/JGaviria0/FileServer
```

Go to the project directory

```bash
  cd FileServer
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

### Start the Server

```bash
  cd Server
  python3 Server.py
```

### Start the Nodes

```bash
  cd Node
  python3 Node.py [Server IP] [Server port] 
```

Run the client, open other terminal

- **List**
    ```bash
    python3 Client/Client.py [Server IP] [Server port] list 
    ```

- **Download**
    ```bash
    python3 Client/Client.py [Server IP] [Server port] download [file name] 
    ```

- **Upload**
    ```bash
    python3 Client/Client.py [Server IP] [Server port] upload [file name] 
    ```



## Examples

- **List**
    ```bash
    python3 Client/Client.py 192.168.1.1 5555 list 
    ```

- **Download**
    ```bash
    python3 Client/Client.py 192.168.1.1 5555 download Test.txt
    ```

- **Upload**
    ```bash
    python3 Client/Client.py 192.168.1.1 5555 upload Test.txt
    ```
 ## .env
```bash
BUF_SIZE=1048576  
PRINCIPAL_PATH='./../'

UPLOAD_TYPE='upload'
GET_UPLOAD_DATA_TYPE='getUploadData'
GET_DOWNLOAD_DATA_TYPE='getDownloadData'
DOWNLOAD_TYPE='download'
SUBSCRIPTION_TYPE='subscrition'
FILE_SAVED='saved'
LIST_TYPE='list'
SEND_TYPE='sending'

MAIN_DIRECTORY='./Files/'
NODES_PORT=4000

#codes:
SEND_FILE_CODE=200
FILE_ALREADY_EXITS_CODE=201
FILE_DOESNT_EXITS_CODE=404
DOWNLOAD_FILE_CODE=202

```
