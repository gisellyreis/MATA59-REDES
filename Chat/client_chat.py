import os
import sys
import time
import socket
import select
import threading

soc = socket.socket()

def listen():
   while True:
      r, _, _ = select.select([soc], [], [])
      try:
         data = r[0].recv(1024)
      except:
         data = None
      if data:
         print(data.decode())
      else:
         print("A conexão com o servidor foi perdida.")
         os._exit(0) 


      

try:
   
   name, server_host, port = input().split()

   soc.connect((server_host, int(port)))
   connectionMessage = name
   soc.send(connectionMessage.encode())

   message = soc.recv(1024).decode()
   print(message)

   if str(message).split(" ", 1)[0] != "ERRO:":
      # Inicia a Thread responsável por receber as mensagens do servidor.
      t = threading.Thread(target = listen)
      t.start()

      while True:
         message = input()
         soc.send(message.encode())
except KeyboardInterrupt:
   soc.shutdown(socket.SHUT_WR)
   print("Programa finalizado.")
   os._exit(0) 
except Exception as e:
   print("ERRO: ", e)
   os._exit(0) 



