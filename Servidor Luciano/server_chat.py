""""
Servidor: lida com múltiplos clientes em paralelo com select. Usa select
para manualmente lidar com um conjunto de sockets: Sockets principais que 
aceitam novas conexões, e sockets de input conectadas para aceitar clientes.
"""""

import time
import select
import socket
from datetime import datetime

def agora(): return time.ctime(time.time())

# Configurações do servidor
meuHost = '127.0.0.1' #IP de Loopback


# Número de sockets usados
numPortSocks = 2

# Lista de sockets criados por função de cada socket
socks_principais, le_socks, escreve_socks = [], [], []

clientmap = {}


# --------------------------------------------Programa Principal--------------------------------------------

# Recebe a entrada referente ao número da porta
minhaPort = int(input())

# Cria um socket para cada função
for i in range(numPortSocks):
    # Configura um socket TCP/IP
    portsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configura o socket
    portsock.bind((meuHost, minhaPort))
    portsock.listen(5)

    # O adiciona a lista de principais e leitoras
    socks_principais.append(portsock)
    le_socks.append(portsock)

    # Aumenta o valor da port para mudar o próximo socket
    minhaPort += 1

while True:
    # Vemos todos os sockets legíveis e escrevíveis e os selecionamos
    legiveis, escreviveis, excessoes = select.select(le_socks, escreve_socks, [])

    # Para cada socket legígel
    for sockobj in legiveis:
        # Se ele é um socket principal
        if sockobj in socks_principais:
            # Aceita o socket
            novo_sock, endereco = sockobj.accept()
            # E o coloca no socket de leitura
            le_socks.append(novo_sock)

            escreve_socks.append(novo_sock)
        else:
            # Lemos o que está no socket
            data = sockobj.recv(1024)

            # Se não recebermos nada
            if not data:
                # Fechamos os socket
                sockobj.close()
                # E o removemos do socket de leitura
                le_socks.remove(sockobj)
            # Caso contrário
            else:
                command, message = str(data.decode()).split(" ", 1)

                # Primeira mensagem do cliente: Conexão.
                if command == "CONN":
                    # Registra o nome do cliente
                    name = message.strip()
                    clientmap[sockobj] = name
                    now = datetime.now()
                    print('{} \t {} \t Conectado'.format(now.strftime("%H:%M"), name))

                elif command == "SEND":
                    name = clientmap[sockobj]
                    for o in escreve_socks:
                        if o != sockobj:
                            o.send(('{}: {}'.format(name, message).encode()))

                else:
                    sockobj.send('Mensagem Recebida'.encode())



                # Imprime a mensagem recebida
                # print()
                # print('\tRecebeu', data, 'em', id(sockobj))

                # Preparamos uma resposta a ser enviada
                # resposta = 'Eco=>%s as %s' % (data, agora())
                # sockobj.send(resposta.encode())








