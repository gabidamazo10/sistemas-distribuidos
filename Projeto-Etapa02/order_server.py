import ast
from concurrent import futures
import json
import logging
import random

import grpc
import projeto_pb2
import projeto_pb2_grpc

import time

import sys

import json
import socket

global socketPar
global socketImpar

def setReplica():
    num = random.randint(1,3)

    try:
        hostName = socket.gethostname()

        socketPar = socket.socket()
        socketPar.settimeout(1)

        socketImpar = socket.socket()
        socketImpar.settimeout(1) 

        if num == 1:
            socketPar.connect((hostName, 10000))
            socketImpar.connect((hostName, 10001))
            print('Particao 1: 10000, Particao 2: 10001')
        elif num == 2:
            socketPar.connect((hostName, 10002))
            socketImpar.connect((hostName, 10003))
            print('Particao 1: 10002, Particao 2: 10003')
        elif num == 3:
            socketPar.connect((hostName, 10004))
            socketImpar.connect((hostName, 10005))
            print('Particao 1: 10004, Particao 2: 10005')
    except:
        print('Erro na criacao das particoes')
        sys.exit()
        
    return socketPar, socketImpar

############################################################

client_list = {}
product_list = {}
order_list = {}
dados_order = {} 

class OrderPortal(projeto_pb2_grpc.OrderPortalServicer):
    
    def __init__(self) -> None:
        self.socketPar, self.socketImpar = setReplica()
    
    def CreateOrder(self, request, context):
        socket = None

        # OID:CID-{PID:qnd, PID,qnt}
        # 1:1-{1:11, 2:5}
        # data 1-{1:11, 2:5}
        OID = request.OID
        CID = request.CID
        data = request.data

        value = f'{CID}-{data}' 
        # value = 1-{1:11, 2:5}


        if int(OID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar
        


        ###VERIFICACOES

        #verifica se ja existe OID --> se existir, erro
        msg = json.dumps({'function':'read', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaOID = json.loads(resposta.decode())

        if respostaOID['data'] != '': #existe OID
            return projeto_pb2.Reply(error = 1, description = '\Order already exists.')

        
        #verifica se existe CID --> se não existir, erro
        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaCID = json.loads(resposta.decode())
        print("CID EXISTE ", respostaCID)

        if respostaCID['data'] == '': #nao existe CID
            return projeto_pb2.Reply(error = 1, description = '\nClient not in database.')
        

        #verifica se existe PID e se existe o suficiente 
        products = ast.literal_eval(request.data) # {'11': '1'}
        keyList = list(products.keys()) # ['11']

        for i in keyList:
            msg = json.dumps({'function':'read', 'key':i, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            respostaPID = json.loads(resposta.decode())
            if respostaPID['data'] == '': #se não existir, erro
                return projeto_pb2.Reply(error = 2, description = '\nSome products doesnt exist.')
            
            #print('PRODUCT i', products[i]) # 1
            #print('DATA RESPPID', respostaPID['data']) #{'NAME': 'aaa', 'CAPACITY': '111'}
            #print('DATA RESPPID2', respostaPID['data']['CAPACITY']) #{'NAME': 'aaa', 'CAPACITY': '111'}

            #product_copy = ast.literal_eval(product_list[i])
            if int(products[i]) > int(respostaPID['data']['CAPACITY']):
                return projeto_pb2.Reply(error = 3, description = '\nNot enough products.')
            


        ##### CRIACAO PEDIDO

        #Cria order
        msg = json.dumps({'function':'insert', 'key':OID, 'value':value})
        socket.send(msg.encode())
        resposta = socket.recv(2048)

    
        # Atualiza Quantidades de Produtos
        for i in keyList:
            msg = json.dumps({'function':'delete', 'key':i, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            newQnt = int(respostaPID['data']['CAPACITY']) - int(products[i])
            data = {"NAME":respostaPID['data']['NAME'],"CAPACITY":str(newQnt)}

            msg = json.dumps({'function':'insert', 'key':i, 'value':data})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            

        return projeto_pb2.Reply(error = 0) 



    def RetrieveOrder(self, request, context):
        
        socket = None

        mensagem = (request.ID).split("-")

        OID = mensagem[0]
        CID = mensagem[1]


        if int(OID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        msg = json.dumps({'function':'read', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
        
        #print(resposta) #{'data': '1-{"11": "1"}'}
        #print('type:', type(resposta)) # <class 'dict'>
        #print('data',resposta['data']) #1-{"11": "1"}
        #print('type',type(resposta['data']))
        

        value = resposta['data'].split('-')

        if resposta['data'] == '':
            aux = "0"
            return projeto_pb2.Order(data = "NOT_FOUND", CID = "0", OID = "0")
            return response 
        else:
            return projeto_pb2.Order(data = value[1], CID = CID, OID = OID)
            return response 
           


        
    def UpdateOrder(self, request, context):
        socket = None

        # OID:CID-{PID:qnd, PID,qnt}
        # 1:1-{1:11, 2:5}
        # data 1-{1:11, 2:5}
        OID = request.OID
        CID = request.CID
        data = request.data

        
        # value = 1-{1:11, 2:5}


        if int(OID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar
        


        ###VERIFICACOES

        #verifica se ja existe OID --> se existir, erro
        msg = json.dumps({'function':'read', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaOID = json.loads(resposta.decode())

        if respostaOID['data'] == '': #existe OID
            return projeto_pb2.Reply(error = 1, description = '\Order doesnt exists.')

        
        #verifica se existe CID --> se não existir, erro
        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaCID = json.loads(resposta.decode())

        if respostaCID['data'] == '': #nao existe CID
            return projeto_pb2.Reply(error = 1, description = '\nClient not in database.')
        



        #pega o valor anterior do OID
        auxProduct = respostaOID['data'].split('-') 
        oldProducts = ast.literal_eval(auxProduct[1]) # {2: 10, 1: 5}
        keyList = list(oldProducts.keys()) # ['11']respostaOID['data'].split('-')

        #verifica se existe PID e se existe o suficiente  - no request.data tem o novo pedido
        newProducts = ast.literal_eval(request.data) # {'11': '1'}
        
        orders = oldProducts.copy()

        for i in keyList:
            msg = json.dumps({'function':'read', 'key':i, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            respostaPID = json.loads(resposta.decode())

            if respostaPID['data'] == '': #se não existir produto, erro
                return projeto_pb2.Reply(error = 2, description = '\nSome products doesnt exist.')

            
            oldValue = oldProducts[i]
            bankValue = int(respostaPID['data']['CAPACITY'])
            newValue = int(newProducts[i])
            
            chave = {i:str(bankValue)}
            orders.update(chave)

            key = list(newProducts.keys())

            if i == str(key[0]):
                #não tem produtos suficiente
                if newValue > bankValue:
                    return projeto_pb2.Reply(error = 3, description = '\nNot enough products.')
                
                if newValue > int(oldValue):
                    newQntBank = bankValue - (newValue - int(oldValue))

                if newValue < int(oldValue):
                    newQntBank = bankValue + (int(oldValue) - newValue)

                # mudar o product
                msg = json.dumps({'function':'delete', 'key':i, 'value':None})
                socket.send(msg.encode())
                resposta = socket.recv(2048)

                data = {"NAME":respostaPID['data']['NAME'],"CAPACITY":str(newQntBank)}
                msg = json.dumps({'function':'insert', 'key':i, 'value':data})
                socket.send(msg.encode())
                resposta = socket.recv(2048)

                chave = {i:str(newQntBank)}
                orders.update(chave)


                
        # Atualiza pedido
        msg = json.dumps({'function':'delete', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)

        value = f'{CID}-{orders}' 
        msg = json.dumps({'function':'insert', 'key':OID, 'value':value})
        socket.send(msg.encode())
        resposta = socket.recv(2048)

        return projeto_pb2.Reply(error = 0) 
    

    def DeleteOrder(self, request, context):
        socket = None

        mensagem = (request.ID).split("-")
        OID = mensagem[0]
        CID = mensagem[1]

        if int(OID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar
        


        ###VERIFICACOES

        # verifica se ja existe OID --> se existir, erro
        # E verifica se existe CID --> se não existir, erro
        msg = json.dumps({'function':'read', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaOID = json.loads(resposta.decode())
        
        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        respostaCID = json.loads(resposta.decode())
        
        
        if respostaOID['data'] == '' or respostaCID['data'] == '' : #existe OID
           return projeto_pb2.Reply(error = 1, description = '\nOrder or Client not in database.')
        
        
        auxProduct = respostaOID['data'].split('-')
        products = ast.literal_eval(auxProduct[1])
        keyList = list(products.keys()) # ['11']

        
        for i in keyList:
            msg = json.dumps({'function':'read', 'key':i, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            respostaPID = json.loads(resposta.decode())

            msg = json.dumps({'function':'delete', 'key':i, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            value = int(products[i])
            bankValue = int(respostaPID['data']['CAPACITY'])

            newQnt = bankValue + value
            data = {"NAME":respostaPID['data']['NAME'],"CAPACITY":str(newQnt)}

            msg = json.dumps({'function':'insert', 'key':i, 'value':data})
            socket.send(msg.encode())
            resposta = socket.recv(2048)



        msg = json.dumps({'function':'delete', 'key':OID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)

        return projeto_pb2.Reply(error = 0)

        

    def RetrieveClientOrders(self, request, context):
        CID = request.ID
        if CID not in client_list:
           yield projeto_pb2.Order(data = "NOT_FOUND", CID = "0", OID = "0")

        # {'1': '1-{"10": "1", "11": "1"}'}
        # order_data: {"1": "22", "2": "2", "3": "4"}
        keyList = list(order_list.keys())              
        
        for i in keyList:
            order_data = (order_list[i]).split('-')
            order_final = ast.literal_eval(order_data[1])
            if order_data[0] == CID:
                keyTeste = list(order_final.keys()) 
                #print(order_data[1])
                #print(keyTeste)
                for j in keyTeste:
                    yield projeto_pb2.Order(data = f'PID: {j} --- QUANTATY: {order_final[j]}', CID = request.ID, OID = i)
                
                #yield projeto_pb2.Order(data = order_data[1], CID = request.ID, OID = i)  

def serve(port_):
           
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    projeto_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortal(), server)
    server.add_insecure_port('[::]:' + port_)
    server.start()
    print('Server started, listening on '+ port_)
    return(server)
    
if __name__ == "__main__":
    logging.basicConfig()
    
    if len(sys.argv) <= 1:
        port_ = '50051'
    else:
        port_ = sys.argv[1]
    
    server = serve(port_)
    server.wait_for_termination()
