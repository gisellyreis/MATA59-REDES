import time, socket, sys, threading, select
from datetime import datetime

soc = socket.socket()
do_read = False

def listen():
   try:
      r, _, _ = select.select([soc], [], [])
      do_read = bool(r)
   except socket.error:
      pass
   if do_read:
      data = soc.recv(1024)
      print(data.decode())

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
   sys.exit(0)


