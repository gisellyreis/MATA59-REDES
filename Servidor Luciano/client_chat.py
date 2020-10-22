import socket
import threading

class Cliente(threading.Thread):
    """
    Classe que irá gerar os clientes
    """
    def __init__(self, c, server, port, *mensagem):
        # Número identificador de cliente
        self.c = c

        # Servidor a ser conectado
        self.server = server

        # Port para ser usada
        self.port = port

        # Mensagens a serem colocadas
        self.msgs = mensagem

        threading.Thread.__init__(self)

    def run(self):
        # Criamos o socket e o conectamos ao servidor
        sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockobj.connect((self.server, self.port))

        # Mandamos a mensagem linha por linha
        for linha in self.msgs:
            sockobj.send(linha)

            # Depois de enviar a linha espera-se a resposta do servidor
            data = sockobj.recv(1024)
            print('Cliente', self.c, ' recebeu: ', data)
            
        # Fechamos a conexão
        sockobj.close()

# Configurações de conexão do servidor
serverHost = ''
serverPort = 50007

# Mensagem a ser mandada codificada por bytes
mensagem = [b'Ola, pessoal']

# Seperando os clientes
for c in range(20):
    Cliente(c, serverHost, serverPort, *mensagem).start()

print('Gerando todos os clientes')