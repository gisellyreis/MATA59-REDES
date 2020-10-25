import socket
import sys
from datetime import datetime
import threading
import keyboard
import time

HOST = ''
ADDR = '127.0.0.1'
PORT = 3000
BUFSIZE = 1024

clients = []

if (len(sys.argv) > 1):
    PORT = int(sys.argv[1])
else:
    PORT = int(input("Qual porta deseja ouvir? "))

def close():
    global clients

    for client in clients:
        client["connection"].send(bytes(f'Servidou parou', 'utf-8'))
        client["connection"].close()
    del clients
    print('Servidor Desconectado.')
    sock.close()
    sys.exit(0)


def HELP(connection):
    connection.send(bytes(f'\nSEND: <MESSAGE> - Envia <MESSAGE> para todos os usuários conectados ao servidor', 'utf-8'))
    connection.send(bytes(f'\nSENDTO: <CLIENT_NAME> <MESSAGE> - Envia <MESSAGE> apenas para o usuário <CLIENT_NAME> caso ele esteja conetado ao servidor', 'utf-8'))
    connection.send(bytes(f'\nWHO: - Retorna a lista dos usuários conectados ao servidor', 'utf-8'))
    connection.send(bytes(f'\nHELP: - Retorna a lista de comandos suportados e seu uso', 'utf-8'))

def WHO(connection):
    global clients
    for client in clients:
        connection.send(bytes(f'{client["name"]}', 'utf-8'))
        print()

def SEND(client_name, connection, msg):
    global clients
    for client in clients:
        if client["name"] == client_name:
            continue
        else:
            client["connection"].send(bytes(f'{client_name}: {msg}', 'utf-8'))      
            #client["connection"].send(data)   

def SENDTO(client_name, to, msg):
    global clients
    for client in clients:
        if client["name"] == to:
            client["connection"].send(bytes(f'{client_name}: {msg}', 'utf-8'))
            break

def DESCONNECT(client_name, msg):
    global clients
    for client in clients:
        if client["name"] == client_name:
            continue
        else:
            client["connection"].send(bytes(f'{msg}', 'utf-8'))  

def comand(client_name, connection, addr):
    global clients
    try:
        while True:
            try:
                data = connection.recv(BUFSIZE)
                if not data:
                    print(f'{datetime.now().strftime("%H:%M")} {client_name} Desconetado.')
                    client = { 'name': client_name, 'connection': connection, 'addr': addr}
                    clients.remove(client)
                    connection.close()
                    break

                comand = data.decode().split()
                cmd = comand[0]
                del comand[0]
                msg = ' '.join(comand)

                #print(cmd)
                #print(msg)
                if cmd == 'SEND':
                    print(f'{datetime.now().strftime("%H:%M")} {client_name} SEND Executado: Sim')
                    SEND(client_name, connection, msg)
                elif cmd == 'SENDTO':
                    print(f'{datetime.now().strftime("%H:%M")} {client_name} SENDTO Executado: Sim')
                    comand = msg.split()
                    to = comand[0]
                    del comand[0]
                    msg = ' '.join(comand)
                    SENDTO(client_name, to, msg)
                elif cmd == 'WHO':
                    print(f'{datetime.now().strftime("%H:%M")} {client_name} WHO Executado: Sim')
                    WHO(connection)
                elif cmd == 'HELP':
                    print(f'{datetime.now().strftime("%H:%M")} {client_name} HELP Executado: Sim')
                    HELP(connection)
                elif cmd == 'DESCONNECT':
                    print(msg)
                    msg = f'{client_name} saiu da sala.'
                    DESCONNECT(client_name, msg)
                else:
                    print('Comando não diponível. Use HELP para ver todos os comandos.')
            except Exception as e:
                # Fecha conexão do client que saiu
                print(e)
                client = { 'name': client_name, 'connection': connection, 'addr': addr}
                clients.remove(client)
                connection.close()
                break
    except Exception as e:
        print(e)
        sys.exit(0)


def start():
    global clients
    if keyboard.is_pressed('Ctrl + c'):
        print('erro ctrl') 
        sys.exit(0)
    try:
        while True:
            connection, addr = sock.accept()
                
            client_name = connection.recv(BUFSIZE)
            client_name = client_name.decode()
            client = { 'name': client_name, 'connection': connection, 'addr': addr}
            clients.append(client)
            print(f'{datetime.now().strftime("%H:%M")} {client_name} Conectado' )
            #print(clients)      
            time.sleep(1)     
            try:
                clientThread = threading.Thread(target=comand, args=(client_name, connection, addr))
                clientThread.daemon = True
                clientThread.start()
            except Exception as e:
                print(e) 
                sys.exit(0)
                break
    except:
        close()    


time.sleep(2)
while True:
    try:
        time.sleep(2)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((ADDR, PORT))
        sock.listen()

        #print(ADDR)
        print('Aguardando conexões ...')
        time.sleep(1)
        try:
            time.sleep(1)
            start()
        except Exception as e:
            print(e)
            sys.exit(0)
            break
    except Exception as e:
        print(e)
        sys.exit(0)
        break