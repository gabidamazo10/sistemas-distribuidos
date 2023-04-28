from concurrent import futures
import logging
import random

import grpc
import projeto_pb2
import projeto_pb2_grpc

from paho.mqtt import client as mqtt_client
import time

import sys

############################################################

broker = 'broker.emqx.io'
port = 1883
topic = "projeto/sd/entrega01"
#topic2 = "admin_product"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

client_list = {}
product_list = {}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]

    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):    
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # logica pra tratar msgs do MQTT: atualizar client_list e product_list
        mensagem = msg.payload.decode().split("-")
        
        if mensagem[3] == "admin_client":          
            if mensagem[0] == "ADD_CLIENT" or mensagem[0] == "UPDATE_CLIENT":
                client_list.update({mensagem[1]:mensagem[2]})
            elif mensagem[0] == "DELETE_CLIENT":
                if mensagem[1] in client_list:
                    del client_list[mensagem[1]]
            
                    
        elif mensagem[3] == "admin_product":
            
            if mensagem[0] == "ADD_PRODUCT" or mensagem[0] == "UPDATE_PRODUCT":
                product_list.update({mensagem[1]:mensagem[2]})
            elif mensagem[0] == "DELETE_PRODUCT":
                if mensagem[1] in product_list:
                    del product_list[mensagem[1]]
        

    client.subscribe(topic)
    client.on_message = on_message



############################################################

class AdminPortal(projeto_pb2_grpc.AdminPortalServicer):
 
    def CreateClient(self, request, context):
        
        # Create an dictionary for clients
        
        if request.CID not in client_list:
            client_list.update({request.CID:request.data})
            
            publish(client, f"ADD_CLIENT-{request.CID}-{request.data}-admin_client") 
            
            return projeto_pb2.Reply(error = 0) 
        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient already in database: choose another ID.')
            
        # return super().CreateClient(request, context)
        
    def RetrieveClient(self, request, context):
        
        CID = request.ID
        
        if CID not in client_list:
            aux = "0"
            response = projeto_pb2.Client(data = 'NOT_FOUND', CID = aux)
            return response 
        else:
            response = projeto_pb2.Client(data = client_list[CID], CID = CID)
            return response 
        
        # return super().RetrieveClient(request, context)
        
    def UpdateClient(self, request, context):
        if  request.CID in client_list: 
            
            chave = {request.CID:request.data}
            client_list.update(chave)
            
            publish(client, f"UPDATE_CLIENT-{request.CID}-{request.data}-admin_client")
            
            return projeto_pb2.Reply(error = 0) 

        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient could not be updated.')
        
        # return super().UpdateClient(request, context)
    
    def DeleteClient(self, request, context):
        CID = request.ID
        
        if CID in client_list: 
            
            del client_list[CID]   
            
            publish(client, f"DELETE_CLIENT-{CID}-NULL-admin_client")
            
            return projeto_pb2.Reply(error = 0) 
    
        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient not found.')
        
        # return super().DeleteClient(request, context)

    def CreateProduct(self, request, context):
        
        if request.PID not in product_list:
            
            product_list.update({request.PID:request.data})
            
            publish(client, f"ADD_PRODUCT-{request.PID}-{request.data}-admin_product") 
            
            return projeto_pb2.Reply(error = 0) 
        
        else:
            return projeto_pb2.Reply(error = 1, description = '\nProduct already in database: choose another ID.')
        
        # return super().CreateProduct(request, context)
        
    def RetrieveProduct(self, request, context):
        PID = request.ID
        
        if PID not in product_list:
            response = projeto_pb2.Product(data = 'NOT_FOUND', PID = PID)
            return response 
            
        else:
            response = projeto_pb2.Product(data = product_list[PID], PID = PID)
            return response 
        
        # return super().RetrieveProduct(request, context)
        
    def UpdateProduct(self, request, context):
        
        if  request.PID in product_list: 
             
            chave = {request.PID:request.data}
            product_list.update(chave)
            
            publish(client, f"UPDATE_PRODUCT-{request.PID}-{request.data}-admin_product") 
            
            return projeto_pb2.Reply(error = 0) 

        else:
            return projeto_pb2.Reply(error = 1, description = '\nProduct could not be updated.')
        
        
        # return super().UpdateProduct(request, context)
        
    def DeleteProduct(self, request, context):
        PID = request.ID
        
        if PID in product_list: 
            
            del product_list[PID]   
            publish(client, f"DELETE_PRODUCT-{PID}-NULL-admin_product")

            return projeto_pb2.Reply(error = 0) 
    
        else:
            return projeto_pb2.Reply(error = 1, description = '\nProduct not found.')
        
        # return super().DeleteProduct(request, context)
 
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
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)

    server.wait_for_termination()
