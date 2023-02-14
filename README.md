
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
  pip3 install pyzmq
```

Start the server

```bash
  cd Server
  python3 Server.py
```

Run the client, open other terminal

- **List**
    ```bash
    python3 Client/Client.py [ip] [port] list 
    ```

- **Download**
    ```bash
    python3 Client/Client.py [ip] [port] download [file name] 
    ```

- **Upload**
    ```bash
    python3 Client/Client.py [ip] [port] upload [file name] 
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
