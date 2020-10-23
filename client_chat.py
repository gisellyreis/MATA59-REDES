import socket
import sys
from datetime import datetime
import threading
import keyboard

HOST = ''
SERVER_PORT = 3000
BUFSIZE = 1024

name = input('Digite seu nome: ')
#SERVER_ADDR = input('Digite endereço do servidor: ')
SERVER_PORT = int(input('Digite a porta do servidor: '))
SERVER_ADDR = '10.0.0.102'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((SERVER_ADDR, SERVER_PORT))

sock.send(name.encode())
print("Conectado com sucesso")

def send():
    while True:
        #sock.send(bytes(input(""), 'utf-8'))
        if keyboard.is_pressed('Ctrl + c'):
            #print('Ctrl + c')
            print(f'{datetime.now().strftime("%H:%M")} Você está Desconectado.')
            message = f'{datetime.now().strftime("%H:%M")} {name} Desconectado.'
            sock.send(message.encode())
            sock.close()
            sys.exit(0)
        try:
            message = input((""))
            sock.send(message.encode())
        except EOFError:
            #print('Error')
            continue
        """  print(f'{datetime.now().strftime("%H:%M")} Você está Desconectado.')
            message = f'{datetime.now().strftime("%H:%M")} {name} Desconectado.'
            sock.send(message.encode())
            sock.close() 
            # se envir essa msg vai para todos: sock.send()
            message = str(e)
            break """
        

iThread = threading.Thread(target=send)
iThread.daemon = True
iThread.start()

while True:
    data = sock.recv(BUFSIZE)
    if not data:
        break
    print(str(data, 'utf-8'))
    