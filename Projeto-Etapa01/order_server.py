import ast
from concurrent import futures
import json
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

client_id = f'python-mqtt-{random.randint(0, 1000)}'

client_list = {}
product_list = {}
order_list = {}
dados_order = {} 

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

        if mensagem[3] == "client_order":
            
            if mensagem[0] == "ADD_ORDER" or mensagem[0] == "UPDATE_ORDER":
                order_list.update({mensagem[1]:f"{mensagem[2]}-{mensagem[4]}"})
            elif mensagem[0] == "DELETE_ORDER":
                if mensagem[1] in order_list:
                    del order_list[mensagem[1]]
        

    client.subscribe(topic)
    client.on_message = on_message

############################################################

class OrderPortal(projeto_pb2_grpc.OrderPortalServicer):
    def CreateOrder(self, request, context):
     
        dados = ast.literal_eval(request.data)
        keyList = list(dados.keys())
        
        if request.OID in order_list:
            return projeto_pb2.Reply(error = 4, description = '\nOrders ID already exists.')


        for i in keyList:
            if i not in product_list:
                return projeto_pb2.Reply(error = 2, description = '\nSome products doesnt exist.')
                
            product_copy = ast.literal_eval(product_list[i])
            if int(dados[i]) > int(product_copy["CAPACITY"]):
                return projeto_pb2.Reply(error = 3, description = '\nNot enough products.')


        if request.CID in client_list:
            for i in keyList:
                product_copy = ast.literal_eval(product_list[i])
                    
                new_qnt = int(product_copy["CAPACITY"]) - int(dados[i])
                
                new_data = {}

                new_data['NAME'] = product_copy["NAME"]
                new_data['CAPACITY'] = str(new_qnt)

                product_data = json.dumps(new_data)

                chave = {i:product_data}
                product_list.update(chave)
                publish(client, f"UPDATE_PRODUCT-{i}-{product_data}-admin_product") 

                        
            order_list.update({request.OID:f"{request.CID}{request.data}"})
            publish(client, f"ADD_ORDER-{request.OID}-{request.CID}-client_order-{request.data}") 
            return projeto_pb2.Reply(error = 0) 
        else:
            return projeto_pb2.Reply(error = 1, description = '\nClient not in database.')
        
        # return super().CreateProduct(request, context)
    
    def RetrieveOrder(self, request, context):
        mensagem = (request.ID).split("-")

        if mensagem[1] in client_list and mensagem[0] in order_list:
            keyList = list(order_list.keys())              
            
            for i in keyList:
                order_data = (order_list[i]).split('-')
                
                if i == mensagem[0] and order_data[0] == mensagem[1]:
                    return projeto_pb2.Order(data = order_data[1], CID = mensagem[1], OID = i)
        else:
            return projeto_pb2.Order(data = "NOT_FOUND", CID = "0", OID = "0")

    def UpdateOrder(self, request, context):
            
        if request.OID not in order_list:
            return projeto_pb2.Reply(error = 1, description = '\nOrders OID not in database.')
        
        if request.CID not in client_list:
            return projeto_pb2.Reply(error = 2, description = '\Client CID not in database.')

        dados = ast.literal_eval(request.data)
        keyList = list(product_list.keys())
        

        for key in dados.keys():
            first_value = key
            second_value = dados[key]

        # dados[0]: pid
        # dados[1]: capacity
        # {'10':'30'}

        if first_value not in product_list:
            return projeto_pb2.Reply(error = 3, description = '\nProduct PID not in database.')

    
        keyList = list(order_list.keys())     
                
        
        for i in keyList:
            order_data = (order_list[i]).split('-')
            # {'1': '1-{"10": "1", "11": "1"}'}
            # order_data[1] ={"10": "1", "11": "1"}

            # 50 - (30 -> 70)
            # 50 - (30 -> 20)
            
        
            if i == request.OID and order_data[0] == request.CID:
                order_copy = ast.literal_eval(order_data[1])
                dados_order = order_copy.copy()

                for key, value in order_copy.items():
                    if first_value not in order_copy:
                        return projeto_pb2.Reply(error = 4, description = '\nProduct PID not in your order.')
                    
                    else:
                        if key == first_value:
                            capacidade = ast.literal_eval(product_list[key])                                
                                       
                                                 
                            if int(second_value) > int(capacidade['CAPACITY']):
                                return projeto_pb2.Reply(error = 5, description = '\nNot enough products in database.')

                            if int(second_value) > int(value):
                                valor = int(second_value) - int(value)
                                if valor > int(capacidade['CAPACITY']):
                                    return projeto_pb2.Reply(error = 5, description = '\nNot enough products in database.')

                                valor_corrigido = int(capacidade["CAPACITY"]) - valor
                                

                            if int(second_value) < int(value):
                                valor = int(value) - int(second_value)
                                valor_corrigido = int(capacidade["CAPACITY"]) + valor
                            
                            if int(second_value) == 0:
                                dados_order.pop(first_value)
                            else:
                                dados_order.update({key:str(second_value)})

                            dados_product = {}
                            dados_product['NAME'] = capacidade['NAME']
                            dados_product['CAPACITY'] = str(valor_corrigido)
                            
                            product_data = json.dumps(dados_product)
                            
                            chave = {key:product_data}
                            product_list.update(chave)
                            publish(client, f"UPDATE_PRODUCT-{key}-{product_data}-admin_product") 

                        #dados_order.update({key:value})
                
                # {'1': '1-{"10": "1", "11": "1"}'}
                # i : order_data[0] - {dados_order}
                # dados_order = {"10":"1", "11":1}
                
                del order_list[request.OID]
                order_list.update({request.OID:f"{request.CID}{str(dados_order)}"})
                publish(client, f"ADD_ORDER-{request.OID}-{request.CID}-client_order-{str(dados_order)}") 
                return projeto_pb2.Reply(error = 0) 


    def DeleteOrder(self, request, context):
        mensagem = (request.ID).split("-")
        # mensagem[0] = oid
        # mensagem[1] = cid

        if mensagem[1] in client_list and mensagem[0] in order_list:
            keyList = list(order_list.keys())              
            
            for i in keyList:
                order_data = (order_list[i]).split('-')
                # {'1': '1-{"10": "1", "11": "1"}'}
                # order_data[1] ={"10": "1", "11": "1"}
            
                if i == mensagem[0] and order_data[0] == mensagem[1]:
                    order_copy = ast.literal_eval(order_data[1])
                    
                    for key, value in order_copy.items():
                        # ir pro product_list em key e product_list["Capacity"] + value
                        capacidade = ast.literal_eval(product_list[key])
                        
                        valor_corrigido = int(capacidade["CAPACITY"]) + int(value)

                        dados_product = {}
                        dados_product['NAME'] = capacidade['NAME']
                        dados_product['CAPACITY'] = str(valor_corrigido)

                        chave = {key:dados_product}
                        product_list.update(chave)
                        publish(client, f"UPDATE_PRODUCT-{key}-{dados_product}-admin_product") 

            del order_list[mensagem[0]]
            publish(client, f"DELETE_ORDER-{mensagem[0]}-NULL-client_order")
            
            return projeto_pb2.Reply(error = 0)


        else:
            return projeto_pb2.Reply(error = 1, description = '\nOrder or Client not in database.')



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
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)

    server.wait_for_termination()
