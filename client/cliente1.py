import socket
import sys
import time
from datetime import datetime

print('Setup do Cliente ...')
time.sleep(1)
#Get the hostname, IP Address from socket and set Port // Teste de acesso
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
#get information to connect with the server
print(shost, '({})'.format(ip))
server_host = input('Digite IP do servidor:')
name = input('Digite seu nome: ')
port = 3000
print('Estabelecendo conexao com o servidor: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Conectado ...\n")
soc.send(name.encode())
server_name = soc.recv(1024)
server_name = server_name.decode()
print('{} esta no chat ...'.format(server_name))
print('Digite [fim] para sair.')

while True:
   try:
      message = soc.recv(1024)
      message = message.decode()
      print(server_name, ">", message)
      message = input(str("Eu > "))
      if message == "[fim]":
         message = "Saindo do Chat"
         soc.send(message.encode())
         print("\n")
         break
   except KeyboardInterrupt:
      print(f'{datetime.now().strftime("%H:%M")} Você está Desconectado.')
      message = f'{datetime.now().strftime("%H:%M")} {name} Desconectado.'
      soc.send(message.encode())
      soc.close()
      # se envir essa msg vai para todos: soc.send()
      break
   soc.send(message.encode())

