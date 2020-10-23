import socket
import sys
from datetime import datetime
import threading

HOST = ''
ADDR = '10.0.0.102'
PORT = 3000
BUFSIZE = 1024

clients = []

if (len(sys.argv) > 1):
    PORT = int(sys.argv[1])
else:
    PORT = int(input("Qual porta deseja ouvir? "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((ADDR, PORT))
sock.listen()

#print(ADDR)
print('Aguardando conexões ...') 

def sendMsg(client_name, connection, addr):
    while True:
        try:
            data = connection.recv(BUFSIZE)
            for client in clients:
                client["connection"].send(bytes(f'{client_name} > ', 'utf-8'))      
                client["connection"].send(data)   
            if not data:
                print(f'{datetime.now().strftime("%H:%M")} {client_name} Desconetado.')
                client = { 'name': client_name, 'connection': connection, 'addr': addr}
                clients.remove(client)
                connection.close()
                break
        except Exception as e:
            print(e)
            client = { 'name': client_name, 'connection': connection, 'addr': addr}
            clients.remove(client)
            break


while True:
    connection, addr = sock.accept()
    client_name = connection.recv(BUFSIZE)
    client_name = client_name.decode()
    client = { 'name': client_name, 'connection': connection, 'addr': addr}
    clients.append(client)
    print(f'{datetime.now().strftime("%H:%M")} {client_name} Conectado' )
    #print(clients)
    clientThread = threading.Thread(target=sendMsg, args=(client_name, connection, addr))
    clientThread.daemon = True
    clientThread.start()
    