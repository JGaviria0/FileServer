

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
BUF_SIZE=65536 #64KB on memory
PRINCIPAL_PATH='./../'
UPLOAD_TYPE='upload'
DOWNLOAD_TYPE='download'
SUBSCRIPTION_TYPE='subscrition'
LIST_TYPE='list'
MAIN_DIRECTORY='./Files/'
