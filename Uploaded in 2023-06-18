# Projeto final da disciplina de Sistemas Distribuídos - Etapa 02

## Enunciado do Projeto

<ul>
  
<li> https://paulo-coelho.github.io/ds_notes/projeto/
  
</ul>

## Instruções detalhadas de compilação e execução

<ul>
<li> O ambiente de desenvolvimento escolhido foi o VSCode pelo Ubuntu, utilizando a linguagem de programação Python na versão 3.10.6 </li> 
<li> Os comandos para instalação das ferramentas utilizados foram os seguintes:
 
  <p><li> Para instalar o GRPC pra Python:</p>
  
 ```python 
  python3 -m pip install --upgrade pip
  sudo python3 -m pip install grpcio
  python3 -m pip install grpcio-tools
 ```
  
<li>Para instalar Plyvel interface to LevelDB
  
 ```python 
 pip install plyvel
 ```
 
 <li>Para instalar PySyncObj
  
 ```python 
 pip install pysyncobj
 ```
 
<li> Os comandos para execução do projeto são: 
 
   <ul>
    <li>Para ligar os bancos:
    <li> Todos os bancos devem ser ligados antes dos servidores/clientes. O argumento X deve ir de 1-6.
  </ul>
  
 ```python
  python3 ./database/database.py X
 ``` 
 
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

## O que NÃO foi implementado?

<ul>
  <li> RETRIEVE MULTIPLE ORDERS: Orders
</ul>

## Link para vídeo com compilação e execução

<ul>
 <li> https://youtu.be/ky8U_kuiDAo
</ul>

## Informações adicionais

<ul>
 
  <li> Devem ser testados CID, PID, OID com valores DIFERENTE. 
  <li> TODOS os bancos devem ser inicializados antes da criação dos servers/clients.
  <li> ATENÇÃO: No arquivo leveldb.py o endereço deve ser trocado para o caminho do seu computador de forma que o final f'COMPLETAR_ENDERECO/leveldb/{part}/{port}/'. Onde leveldb é a pasta de mesmo nome no programa.
  <li> Os servers devem ser inicalizados em portas diferentes. Assim como os clients, de forma que cada client acompanhe o server, pela porta.
  <li> TODOS os servers devem ser inicializados antes de acionar os clients.
 
  
</ul>

## Formato dos Dicionários usados em python e dos bancos
<ul>

  <li> Client_list
  
  ```
  {CID:NAME}
  ```
  
  <li> Product_list
  
  ```
  {PID:{NAME:CAPACITY}
  ```
  
  <li> Order_list
  
  ```
  {OID:CID-{PID:CAPACITY}
  ```
  
  CID: client id </br>
  PID: product id </br>
  OID: order id
</ul>

 
## Referências utilizadas

<ul>
  
<li> https://grpc.io/docs/languages/python/quickstart/
<li> https://www.youtube.com/watch?v=WB37L7PjI5k
<li> https://plyvel.readthedocs.io/en/latest/user.html#getting-started
<li> https://github.com/bakwc/PySyncObj/blob/master/examples/kvstorage.py
  
</ul>
