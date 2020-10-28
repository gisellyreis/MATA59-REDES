import os
import sys
import time
import socket
import select
import threading

# Socket principal
main_socket = socket.socket()

# Função responsável por escutar o servidor e printar suas mensagens
def listen():
   while True:
      # Receve a lista contendo o socket carregando uma mensagem do servidor
      r, _, _ = select.select([main_socket], [], [])
      try:
         # Recebe a mensagem do servidor
         data = r[0].recv(1024)
      except:
         data = None
      # Caso exista mensagem, printa imediatamente na tela
      if data:
         print(data.decode())
      # Caso a mensagem seja nula
      else:
         # Isso representa a perda de conexão com o servidor e por isso é finalizado o programa
         #print("A conexão com o servidor foi perdida, finalizando programa...")
         time.sleep(1)
         os._exit(0) 

try:
   # Recebe os parêmetros de conexão informados pelo cliente
   #name, server_host, port = input().split()
   name = sys.argv[1]
   server_host = sys.argv[2]
   port = sys.argv[3]
   print(name, server_host, port)
   # Estabelece conexão com o servidor
   main_socket.connect((server_host, int(port)))
   # Envia o nome do cliente para registro no servidor
   main_socket.send(name.encode())
   # Recebe retorno do servidor para saber se a conexão foi aceita ou não
   message = main_socket.recv(1024).decode()
   # Printa o retorno do servidor
   print(message)
   # Caso o retorno do servidor não comece com "ERRO:" - A conexão foi aceita
   if str(message).split(" ", 1)[0] != "ERRO:":
      # Inicia a Thread responsável por receber as mensagens do servidor.
      t = threading.Thread(target = listen)
      t.start()
      # Laço responsavel por receber todos os  inputs do cliente
      while True:
         # Recebe input
         message = input()
         # Envia input para o servidor
         main_socket.send(message.encode())

# CTRL + C ativado: Finaliza imediatamente do programa
except KeyboardInterrupt:
   # Desliga o socket principal
   main_socket.shutdown(socket.SHUT_WR)
   #print("Aviso: \"CTRL + C\" ativado, finalizando programa...")
   # time.sleep(1)
   os._exit(0) 
# Caso ocorra algum erro no programa: informa o erro e finializa
except Exception as e:
   #print("ERRO: ", e,"\nFinalizando programa...")
   # time.sleep(1)
   os._exit(0) 