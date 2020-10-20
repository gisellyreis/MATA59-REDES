import socket
import sys
import time
from datetime import datetime

#Recebe a porta que o server vai estar escutando como parametro
if (len(sys.argv) > 1):
   PORT = int(sys.argv[1])
   #print(PORT)
else:
   PORT = 3000

print('Setup do servidor ...')
time.sleep(1)

#Define o protocolo -> socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Garante destruição do socket após interrupção
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
BUFSIZE = 1024

clients = []

sock.bind((HOST, PORT))
#print(HOST, '({})'.format(IP))
sock.listen() #Try to locate using socket


server_name = input('Digite seu nome: ')

#print('Aguardando conexoes ...')
connection, addr = sock.accept()
#print("Tentando conexao com ", addr[0], "(", addr[1], ")\n")
#print('Conexao estabelecida com: {}, ({})'.format(addr[0], addr[0]))


#Get a connection from client side
client_name = connection.recv(BUFSIZE)
client_name = client_name.decode()
print(f'{datetime.now().strftime("%H:%M")} {client_name} Conectado' )
print('Digite [fim] para sair do chat')
connection.send(server_name.encode())

while True:
   try:
      message = input('Eu > ')
      if message == '[fim]':
         message = 'Ate mais! Obrigado!...'
         connection.send(message.encode())
         print("\n")
         break
   except KeyboardInterrupt:
      message = 'Servidor parou.'
      break
   connection.send(message.encode())
   message = connection.recv(BUFSIZE)
   message = message.decode()
   print(client_name, '>', message)