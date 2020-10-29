### G09 - Safira 
## Componentes

- Roberto Rangel - rsrba1954@gmail.com
- Luciano Almeida - luciano_dealmeida@yahoo.com.br
- Giselly Alves Reis - giselly_reis@outlook.com
- Airton Serra - airton_serra_sena@hotmail.com

- Lingauagem utilizda: Python

## A Topologia

Topologia de Rede é um termo usado para designar a forma externa ou física assumida pelas ligações dos computadores ou nós da rede, podendo ser feita de vparias maneiras e formatos.
A topologia adotada nesse trabalho foi em Estrela. É uma topologia ponto a ponto, onde todos os dispositivos da rede encontram-se conectados a um Switch. 
Todos os dados enviados de um cliente para outro é enviada primeiro ao servidor que fica no centro da estrela.

![](https://sites.google.com/site/topologiasderedexd/_/rsrc/1496345699046/topologia-estrela/redesss.jpg)

> Estrela

## Tipo de Rede

LAN - O chat funciona apenas em redes locais, ou seja, os computadores (clientes) precisam estar no mesmo espaço físico, conectados a mesma rede para poder se conectar ao servidor do chat.

## Arquitetura

Cliente/ Servidor

Características do Cliente:
- Inicia pedidos para o servidor;
- Espera por respostas;
- Recebe respostas;
- Os dados enviados para o servidor devem ser comandos que iniciam com ums string indicando qual ação a ser realizada;

Características do Servidor:
- Sempre espera por um pedido de um cliente;
- Atende os pedidos e, em seguida responde aos clientes com os dados solicitados;
- Executa o comando especificado pelo cliente;
- Se a mensagem retornada pelo servidor começa com "ERRO:" significa que houve um erro;

## Protocolo

TCP - Transmission Control Protocol
Protocolo de transporte fim-a-fim, orientado a conexão, que fornece um serviço de transferência confiável de dados entre aplicações parceiras. 
Garante que os dados são entregues livres de erro, em sequência e sem perdas ou duplicação.
Admite o término negociado ou abrupto de conexões.
O protocolo TCP estabelece uma conexão entre o socket cliente e o socket servidor antes do envio de qualquer mensagem de dados.
Um servidor TCP/IP precisa associar um socket à alguma porta. Quando o servidor recebe uma solicitação de conexão, ele primeiramente precisa aceitá-la, para depois receber dados.
Quando a comunicação com o cliente for encerrada, o socket do cliente é destruído.

Para que o servidor respondesse a mais de umm cliente por vez, usamos select, para selecionar no lado do servidor a qual cliente ouvir/responder, e thread no lado cliente para que cada um seja uma conexão diferente.
