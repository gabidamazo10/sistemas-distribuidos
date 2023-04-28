# Projeto final da disciplina de Sistemas Distribuídos

## Instruções detalhadas de compilação e execução

<ul>
<li> O ambiente de desenvolvimento escolhido foi o VSCode pelo Ubuntu, utilizando a linguagem de programação Python na versão 3.10.6 </li> 
<li> Os comandos para instalação do GRPC e do MQTT utilizados foram os seguintes:
 
  <p><li> Para instalar o GRPC pra Python:</p>
  
 ```python 
  python3 -m pip install --upgrade pip
  sudo python3 -m pip install grpcio
  python3 -m pip install grpcio-tools
 ```
  
<li>Para instalar o cliente Paho MQTT
  
 ```python 
  pip3 install paho-mqtt
 ```
  
<li> Os comandos para execução do projeto são: 

  <ul>
    <li>Para executar o SERVER do Portal ADMIN:
    <li> A PORTA em que o server será executado pode ser passada como argumento ou não. Caso não seja, terá valor default: 50051
  </ul>
  
 ```python
  python3 admin_server.py PORTA
 ``` 
  
  <ul>
    <li>Para executar o CLIENT do Portal ADMIN:
    <li> A PORTA em que o client será executado pode ser passada como argumento ou não. Caso não seja, terá valor default: 50051
  </ul>
  
 ```python
  python3 admin_client.py PORTA
 ``` 
  
  <ul>
    <li>Para executar o SERVER do Portal ORDER:
    <li> A PORTA em que o server será executado pode ser passada como argumento ou não. Caso não seja, terá valor default: 50051
  </ul>
  
 ```python
  python3 order_server.py PORTA
 ``` 
  
  <ul>
    <li>Para executar o CLIENT do Portal ORDER:
    <li> A PORTA em que o client será executado pode ser passada como argumento ou não. Caso não seja, terá valor default: 50051
  </ul>
  
 ```python
  python3 order_client.py PORTA
 ``` 

</ul>

## O que foi implementado?

<ul>
  <li> Todos os requisitos da primeira entrega foram implementados.  
</ul>

## Link para vídeo com compilação e execução

<ul>
 <li> https://youtu.be/ydkNSQzpW-U
</ul>

## Informações adicionais

<ul>

  <li> Foi utilizado um broker online para o MQTT: broker.emqx.io
  <li> Os servers devem ser inicalizados em portas diferentes. Assim como os clients, de forma que cada client acompanhe o server, pela porta.
  <li> TODOS os servers devem ser inicializados antes de acionar os clients.
  <li> Os testes estão localizados na pasta TESTES do repositório.
  
</ul>
 
## Referências utilizadas

<ul>
  
<li> https://grpc.io/docs/languages/python/quickstart/
<li> https://www.youtube.com/watch?v=WB37L7PjI5k
<li> https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
<li> http://www.steves-internet-guide.com/mqtt-python-callbacks/
  
  
</ul>
