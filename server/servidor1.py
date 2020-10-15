import time, socket, sys
print('Setup do servidor ...')
time.sleep(1)
#Get the hostname, IP Address from socket and set Port
soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = 1234
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))
name = input('Digite seu nome: ')
soc.listen() #Try to locate using socket
print('Aguardando conexoes ...')
connection, addr = soc.accept()
print("Tentando conexao com ", addr[0], "(", addr[1], ")\n")
print('Conexao estabelecida com: {}, ({})'.format(addr[0], addr[0]))
#get a connection from client side
client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name + ' esta conectado.')
print('Digite [fim] para sair do chat')
connection.send(name.encode())
while True:
   message = input('Eu > ')
   if message == '[fim]':
      message = 'Ate mais! Obrigado!...'
      connection.send(message.encode())
      print("\n")
      break
   connection.send(message.encode())
   message = connection.recv(1024)
   message = message.decode()
   print(client_name, '>', message)