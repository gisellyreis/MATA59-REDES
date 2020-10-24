import time, socket, sys, threading
from datetime import datetime

global soc, Exit_thread
Exit_thread = False

def ReceberMsg():
   while True:
      message = soc.recv(1024)
      message = message.decode()
      print(message)
      if Exit_thread:
         break



name, server_host, port = input().split()

soc = socket.socket()
soc.connect((server_host, int(port)))
print("Conectado\n")

# now = datetime.now()
# connectionMessage =  ('{} \t {} \t Conectado'.format(now.strftime("%H:%M"), name))

# Envia mensagem para o servidor dizendo que está conectado.
connectionMessage = 'CONN {}'.format(name)
soc.send(connectionMessage.encode())


# Inicia a Thread responsável por receber as mensagens do servidor.
t = threading.Thread(target=ReceberMsg)
t.start()

while True:
   message = input()
   soc.send(message.encode())

