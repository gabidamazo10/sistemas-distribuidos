from concurrent import futures
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

class AdminPortal(projeto_pb2_grpc.AdminPortalServicer):
 
    def __init__(self) -> None:
        self.socketPar, self.socketImpar = setReplica()

    def CreateClient(self, request, context):
        
        socket = None
        
        CID = request.CID
        data = request.data
        
        if int(CID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        if CID not in client_list:
            
            msg = json.dumps({'function':'read', 'key':CID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            resposta = json.loads(resposta.decode())
                
            if resposta['data'] == '':
                
                client_list.update({CID:data})
                
                msg = json.dumps({'function':'insert', 'key':CID, 'value':data})
                socket.send(msg.encode())
                resposta = socket.recv(2048)
                return projeto_pb2.Reply(error = 0)
            else:
                
                product_list.update({CID:resposta['data']})
                return projeto_pb2.Reply(error = 1, description = '\nClient already in database: choose another ID.')
        
        else:
            
            return projeto_pb2.Reply(error = 1, description = '\nClient already in database: choose another ID.')
        
        
    def RetrieveClient(self, request, context):
        
        socket = None
        CID = request.ID
        
        if int(CID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar
        
        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
        
        if resposta['data'] == '':
            aux = "0"
            response = projeto_pb2.Client(data = 'NOT_FOUND', CID = CID)
            return response 
        else:
            product_list.update({CID:json.dumps(resposta['data'])})
            response = projeto_pb2.Client(data = json.dumps(resposta['data']), CID = CID)
            return response 
        
        
    def UpdateClient(self, request, context):
        
        socket = None
        
        CID = request.CID
        data = request.data
        
        if int(CID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
            
        if resposta['data'] != '':
            
            msg = json.dumps({'function':'delete', 'key':CID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            msg = json.dumps({'function':'insert', 'key':CID, 'value':data})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            client_list.update({CID:data})
            
            return projeto_pb2.Reply(error = 0)

        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient could not be updated.')
    
    
    def DeleteClient(self, request, context):
        
        socket = None
        
        CID = request.ID
    
        if int(CID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        msg = json.dumps({'function':'read', 'key':CID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
            
        if resposta['data'] != '': 
            
            if CID in client_list:
                del client_list[CID]
            
            msg = json.dumps({'function':'delete', 'key':CID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            return projeto_pb2.Reply(error = 0)
        
        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient not found.')
        

    ###############################################
    
    def CreateProduct(self, request, context):
        
        socket = None
        
        PID = request.PID
        data = request.data
        
        if int(PID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        if PID not in product_list:
            
            msg = json.dumps({'function':'read', 'key':PID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            resposta = json.loads(resposta.decode())
                
            if resposta['data'] == '':
                
                product_list.update({PID:data})
                
                msg = json.dumps({'function':'insert', 'key':PID, 'value':json.loads(data)})
                socket.send(msg.encode())
                resposta = socket.recv(2048)
                return projeto_pb2.Reply(error = 0)
            else:
                
                product_list.update({PID:resposta['data']})
                return projeto_pb2.Reply(error = 1, description = '\nProduct already in database: choose another ID.')
        
        else:
            
            return projeto_pb2.Reply(error = 1, description = '\nProduct already in database: choose another ID.')
            
    
    def RetrieveProduct(self, request, context):
        
        socket = None
        PID = request.ID
        
        if int(PID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar
        
        msg = json.dumps({'function':'read', 'key':PID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
        
        if resposta['data'] == '':
            aux = "0"
            response = projeto_pb2.Product(data = 'NOT_FOUND', PID = PID)
            return response 
        else:
            product_list.update({PID:json.dumps(resposta['data'])})
            response = projeto_pb2.Product(data = json.dumps(resposta['data']), PID = PID)
            return response 
        
    
    def UpdateProduct(self, request, context):
        
        socket = None
        
        PID = request.PID
        data = request.data
        
        if int(PID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        msg = json.dumps({'function':'read', 'key':PID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
            
        if resposta['data'] != '':
            
            msg = json.dumps({'function':'delete', 'key':PID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            msg = json.dumps({'function':'insert', 'key':PID, 'value':json.loads(data)})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            product_list.update({PID:data})
            
            return projeto_pb2.Reply(error = 0)

        else:
            return projeto_pb2.Reply(error = 1, description = '\nProduct could not be updated.')
    
    
    def DeleteProduct(self, request, context):
        
        socket = None
        
        PID = request.ID
    
        if int(PID) % 2 == 0:
            socket = self.socketPar
        else:
            socket = self.socketImpar

        msg = json.dumps({'function':'read', 'key':PID, 'value':None})
        socket.send(msg.encode())
        resposta = socket.recv(2048)
        resposta = json.loads(resposta.decode())
            
        if resposta['data'] != '': 
            
            if PID in product_list:
                del product_list[PID]
            
            msg = json.dumps({'function':'delete', 'key':PID, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            return projeto_pb2.Reply(error = 0)
        else:
            return projeto_pb2.Reply(error = 1, description = '\nProduct not found.')
        
 
def serve(port_):
           
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    projeto_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortal(), server)
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
