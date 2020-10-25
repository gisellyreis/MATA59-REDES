import time, socket, sys, threading, signal
from datetime import datetime

soc = socket.socket()
exit_prog = False

def signal_handler(signal, frame):
  sys.exit(0)

def ReceberMsg():
   global exit_prog

   while True:
      data = soc.recv(1024)
      if not data or exit_prog:
         soc.close()
         break
      else:
         print(data.decode())


name, server_host, port = input().split()

soc.connect((server_host, int(port)))
connectionMessage = name
soc.send(connectionMessage.encode())

message = soc.recv(1024).decode()
print(message)

if str(message).split(" ", 1)[0] != "ERRO:":
   # Inicia a Thread responsável por receber as mensagens do servidor.
   t = threading.Thread(target=ReceberMsg)
   t.start()

   while True:
      message = input()

      # if keyboard.is_pressed('Ctrl + c'):
      #    print('Você foi desconectado.')
      #    soc.close()
      #    exit_prog = True
      #    time.sleep(1)
      #    sys.exit(0)

      soc.send(message.encode())

print("Programa finalizado.")

