import os
import sys
import time
import select
import socket
from datetime import datetime

# Configurações do servidor
HOST = '127.0.0.1' #IP HOST de Loopback

# Lista de sockets criados por função de cada socket
rList, wList = [], []
# Dicionário que guarda os nomes dos clientes conectados
clientmap = {}

try:
    # Recebe a entrada referente ao número da porta
    #port = int(input())
    port = int(sys.argv[1])

    # Configura um socket TCP/IP
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.bind((HOST, port))
    main_socket.listen(5)

    # Adiciona o socket principal a lista de leitores
    rList.append(main_socket)

    while True:
        # Recebe as listas de sockets de Leitura e escrita do select
        r, _, _ = select.select(rList, wList, [])

        # Para cada socket legígel
        for sockobj in r:
            # Se ele for o socket principal (Requisição de conexão de um cliente)
            if sockobj == main_socket:
                # Aceita o socket
                novo_sock, endereco = sockobj.accept()
                # Recebe o nome do cliente enviado pelo socket
                name = str(novo_sock.recv(1024).decode()).strip()
                socketReady = True
                
                # Verifica se já exite algum cliente com o mesmo nome
                for reg in clientmap.items():
                    if str(reg[1]).upper() == name.upper():
                        #novo_sock.send("ERRO: O nome de usuário já está em uso.".encode())
                        novo_sock.close()
                        socketReady = False
                        break

                # Caso o nome esteja disponível...
                if socketReady:
                    # Adiciona o novo socket na lista de leitores e escritores do servidor
                    rList.append(novo_sock)
                    wList.append(novo_sock)
                    # Registra o nome do socket junto com sua referência
                    clientmap[novo_sock] = name
                    # Printa e envia para o socket que ele foi conectado com sucesso.
                    now = datetime.now()
                    print('{} \t {} \t Conectado'.format(now.strftime("%H:%M"), name))
                    novo_sock.send("Conectado com sucesso.".encode())

            # Caso não seja um socket principal (Um socket de cliente já conectado)
            else:
                try:
                    # Lemos o que está no socket
                    data = sockobj.recv(1024)
                except:
                    data = None
            

                # Se não recebermos nada, desconectamos o socket do cliente
                if not data:
                    # Recupera o nome do cliente
                    name = clientmap[sockobj]

                    # Fechamos o socket do cliente
                    sockobj.close()
                    # Remove o socket da lista de leitores e escritores do servidor
                    rList.remove(sockobj)
                    wList.remove(sockobj)
                    # Remove o cliente do dicionário onde são guardados os nomes de cliente
                    del clientmap[sockobj]
                    # Informa a desconexão do cliente
                    now = datetime.now()
                    print('{} \t {} \t Desconectado'.format(now.strftime("%H:%M"), name))

                # Caso receba dados do socket do cliente
                else:
                    command = ""
                    message = ""
                    msgExec = "Sim"
                    # Recebe a mensagem do cliente e a interpreta
                    sArgs = str(data.decode()).split(" ", 1)
                    if (len(sArgs) > 0):
                        # Captura o comando da mensagem
                        command = sArgs[0]
                        if(len(sArgs) == 2):
                            # Captura a mensagem principal enviada pelo cliente
                            message = sArgs[1]
                    
                    # Comando SEND: Envia a mensagem principal para todos os clientes conectados
                    if command == "SEND":
                        try:
                            name = clientmap[sockobj]
                            for o in wList:
                                if o != sockobj:
                                    o.send(('{}: {}'.format(name, message).encode()))
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t SEND  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))
                    
                    # Comando SENDTO: Envia a mensagem para um cliente especifico
                    elif command == "SENDTO":
                        try:
                            cName, cMessage = message.split(" ", 1)  
                            for o in wList:
                                if o != sockobj and str(clientmap[o]).upper() == cName.upper():
                                    name = clientmap[sockobj]
                                    o.send(('{}: {}'.format(name, cMessage).encode()))
                                    break
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t SENDTO  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))
                    
                    # Retorna a lista de cliente conectados
                    elif command == "WHO":
                        try:
                            name = clientmap[sockobj]
                            msgBuilder = ".:LISTA DE CLIENTE CONECTADOS:.\n"
                            for reg in clientmap.items():
                                msgBuilder+= "{}\n".format(reg[1])
                            sockobj.send(msgBuilder.encode())
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t WHO  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))
                    
                    # Retorna a lista comandos suportados e seu uso
                    elif command == "HELP":
                        try:
                            name = clientmap[sockobj]
                            msgBuilder = ".:LISTA DE COMANDOS:.\n"
                            msgBuilder += "SEND: Envia uma mensagem para todos os clientes conectados (menos para você mesmo) [SEND <MESSAGE>].\n"
                            msgBuilder += "SENDTO: Envia uma mensagem para um cliente especifico que está conectado (menos para você mesmo) [SENDTO <CLIENTS_NAME> <MESSAGE>].\n"
                            msgBuilder += "WHO: Retorna a lista dos clientes conectados ao servidor.\n"
                            msgBuilder += "HELP: Retorna a lista de comandos suportados e seu uso.\n"

                            sockobj.send(msgBuilder.encode())
                        except:
                            msgExec = "Não"
                        finally:
                            print('{} \t {} \t HELP  Executado: {} '.format(now.strftime("%H:%M"), name, msgExec))
                    
                    # Caso o comando não seja reconhecido, printa e envia uma mensagem de erro para o cliente
                    else:
                        msg = "ERRO: Comando \"{}\" inválido".format(command)
                        print(msg)
                        sockobj.send(msg.encode())

# CTRL+C ativado: Finaliza imediatamente do programa
except KeyboardInterrupt:
    #print("Aviso: \"CTRL + C\" ativado, finalizando programa...")
    # time.sleep(1)
    os._exit(0)
# Caso ocorra algum erro no programa: informa o erro e finializa o programa
except Exception as e:
    #print("ERRO: ", e,"\nFinalizando programa...")
    # time.sleep(1)
    os._exit(0) 