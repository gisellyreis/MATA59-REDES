""""
Servidor: lida com múltiplos clientes em paralelo com select. Usa select
para manualmente lidar com um conjunto de sockets: Sockets principais que 
aceitam novas conexões, e sockets de input conectadas para aceitar clientes.
"""""
import os
import time
import select
import socket
from datetime import datetime

# Configurações do servidor
HOST = '127.0.0.1' #IP de Loopback

# Lista de sockets criados por função de cada socket
socks_principais, le_socks, escreve_socks = [], [], []

clientmap = {}


# --------------------------------------------Programa Principal--------------------------------------------

try:
    # Recebe a entrada referente ao número da porta
    port = int(input())

    # Cria um socket para cada função
    # Configura um socket TCP/IP
    portsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configura o socket
    portsock.bind((HOST, port))
    portsock.listen(5)

    # O adiciona a lista de principais e leitoras
    socks_principais.append(portsock)
    le_socks.append(portsock)

    while True:
        # Vemos todos os sockets legíveis e escrevíveis e os selecionamos
        legiveis, escreviveis, excessoes = select.select(le_socks, escreve_socks, [])

        # Para cada socket legígel
        for sockobj in legiveis:
            # Se ele é um socket principal
            if sockobj in socks_principais:
                # Aceita o socket
                novo_sock, endereco = sockobj.accept()
                name = str(novo_sock.recv(1024).decode()).strip()
                socketReady = True

                for reg in clientmap.items():
                    if str(reg[1]).upper() == name.upper():
                        novo_sock.send("ERRO: O nome de usuário já está em uso.".encode())
                        novo_sock.close()
                        socketReady = False
                        break
                
                if socketReady:
                    le_socks.append(novo_sock)
                    escreve_socks.append(novo_sock)

                    clientmap[novo_sock] = name
                    now = datetime.now()
                    print('{} \t {} \t Conectado'.format(now.strftime("%H:%M"), name))
                    novo_sock.send("Conectado com sucesso.".encode())
            else:
                try:
                    # Lemos o que está no socket
                    data = sockobj.recv(1024)
                except:
                    data = None
            

                # Se não recebermos nada
                if not data:
                    name = clientmap[sockobj]

                    # Fechamos os socket
                    sockobj.close()
                    # E o removemos do socket de leitura
                    le_socks.remove(sockobj)
                    escreve_socks.remove(sockobj)
                    del clientmap[sockobj]

                    now = datetime.now()
                    print('{} \t {} \t Desconectado'.format(now.strftime("%H:%M"), name))
                else:
                    command = ""
                    message = ""
                    msgExec = "Sim"

                    sArgs = str(data.decode()).split(" ", 1)
                    if (len(sArgs) > 0):
                        command = sArgs[0]
                        if(len(sArgs) == 2):
                            message = sArgs[1]


                    if command == "SEND":
                        try:
                            name = clientmap[sockobj]
                            for o in escreve_socks:
                                if o != sockobj:
                                    o.send(('{}: {}'.format(name, message).encode()))
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t SEND  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))

                    elif command == "SENDTO":
                        try:
                            cName, cMessage = message.split(" ", 1)  
                            for o in escreve_socks:
                                if o != sockobj and str(clientmap[o]).upper() == cName.upper():
                                    name = clientmap[sockobj]
                                    o.send(('{}: {}'.format(name, cMessage).encode()))
                                    break
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t SENDTO  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))

                    elif command == "WHO":
                        try:
                            msgBuilder = ".:LISTA DE CLIENTE CONECTADOS:.\n"
                            for reg in clientmap.items():
                                msgBuilder+= "{}\n".format(reg[1])
                            sockobj.send(msgBuilder.encode())
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t WHO  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))

                    elif command == "HELP":
                        try:
                            msgBuilder = ".:LISTA DE COMANDO:.\n"
                            msgBuilder += "SEND: Envia uma mensagem para todos os clientes conectados (menos para você mesmo) [SEND <MESSAGE>].\n"
                            msgBuilder += "SENDTO: Envia uma mensagem para um cliente especifico que está conectado (menos para você mesmo) [SENDTO <CLIENTS_NAME> <MESSAGE>].\n"
                            msgBuilder += "WHO: Retorna a lista dos clientes conectados ao servidor.\n"
                            msgBuilder += "HELP: Retorna a lista de comandos suportados e seu uso.\n"

                            sockobj.send(msgBuilder.encode())
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t HELP  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))

                    else:
                        msg = "ERRO: Comando {} inválido".format(command)
                        print(msg)
                        sockobj.send(msg.encode())
except KeyboardInterrupt:
    print("Programa finalizado.")
    os._exit(0)
except Exception as e:
   print("ERRO: ", e)
   os._exit(0) 








