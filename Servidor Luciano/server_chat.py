""""
Servidor: lida com múltiplos clientes em paralelo com select. Usa select
para manualmente lidar com um conjunto de sockets: Sockets principais que 
aceitam novas conexões, e sockets de input conectadas para aceitar clientes.
"""""

import time
import select
import socket

def agora(): return time.ctime(time.time())

# Configurações do servidor
meuHost = ''
minhaPort = 50007

# Número de sockets usados
numPortSocks = 2

# Lista de sockets criados por função de cada socket
socks_principais, le_socks, escreve_socks = [], [], []

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

print('Loop de seleção de socket iniciado')

while True:
    # Vemos todos os sockets legíveis e escrevíveis e os selecionamos
    legiveis, escreviveis, excessoes = select.select(le_socks, escreve_socks, [])

    # Para cada socket legígel
    for sockobj in legiveis:
        # Se ele é um socket principal
        if sockobj in socks_principais:
            # Aceita o socket
            novo_sock, endereco = sockobj.accept()
            # Imprime as conexões
            print('Conecta: ', endereco, id(novo_sock))
            # E o coloca no socket de leitura
            le_socks.append(novo_sock)

        else:
            # Lemos o que está no socket
            data = sockobj.recv(1024)

            # Imprime a mensagem recebida
            print('\tRecebeu', data, 'em', id(sockobj))

            # Se não recebermos nada
            if not data:
                # Fechamos os socket
                sockobj.close()
                # E o removemos do socket de leitura
                le_socks.remove(sockobj)
            # Caso contrário
            else:
                # Preparamos uma resposta a ser enviada
                resposta = 'Eco=>%s as %s' % (data, agora())
                sockobj.send(resposta.encode())








