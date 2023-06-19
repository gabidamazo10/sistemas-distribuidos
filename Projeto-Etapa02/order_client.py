import projeto_pb2
import projeto_pb2_grpc
import grpc

import json
import ast

import sys

def run(port):  

    with grpc.insecure_channel('localhost:'+ port, options=(("grpc.enable_http_proxy", 0),)) as channel:
        
        
        stub = projeto_pb2_grpc.OrderPortalStub(channel)
        aux = 0

        while aux != '6':

            print('\n ------------------------------------ ')
            print('|            ORDER PORTAL             |')
            print(' ------------------------------------- ')
            print('|   Welcome to the Order Portal!      |')
            print(' ------------------------------------- ')
            print('|  1. Create Order                    |')
            print('|  2. Retrieve Order                  |')
            print('|  3. Update Order                    |')
            print('|  4. Delete Order                    |')
            print('|  5. Retrive Client Orders           |')
            print('|  6. Sair                            |')
            print(' ------------------------------------- ')
            print(' Choose an option: ', end='')
            aux = input()
            
            if aux == '1':
                print(" -------------------------------------")
                print('\n Enter the client\'s CID: ', end='')
                cid_aux = input()
                print(' Enter the order\'s OID: ', end='')
                oid_aux = input()
                print('')

                pid_aux = -1
                dados = {}
                
                while(pid_aux != 0):                    
                    print(' Enter the order\'s PRODUCT PID: ', end='')
                    pid_aux = int(input())

                    if pid_aux == 0:
                        break
                    
                    print(' Enter the order\'s PRODUCT QUANTITY: ', end='')
                    qtd_aux = input()
                    
                    chave = {pid_aux:qtd_aux}
                    dados.update(chave)
            
                    print('\n ENTER 0 TO STOP ORDER!!!\n\n', end='')

                # se não tiver produto/client error     
                
                response = stub.CreateOrder(projeto_pb2.Order(OID = oid_aux, CID = cid_aux, data = json.dumps(dados)))        

                if response.error == 0:
                    print("\n Order successfully created!\n")
                else:
                    print(response.description)
            
            if aux == '2':
                print(" -------------------------------------")
                print('\n Enter an client\'s CID: ', end='')
                cid_aux = input()
                print(' Enter an order\'s OID: ', end='')
                oid_aux = input()

                response = stub.RetrieveOrder(projeto_pb2.ID(ID = f'{oid_aux}-{cid_aux}'))
                
                if response.data != 'NOT_FOUND':
                    print("-------------------------")
                    print('\n Client\'s CID: ' + response.CID)
                    print(' Order\'s OID: ' + response.OID)
                    
                    dados = ast.literal_eval(response.data)
                    # print(dados)        
                    
                    for key, value in dados.items():
                        print('\n Product Order PID: ' + key)
                        print(' Product Order CAPACITY: ' + value)
                else: 
                    print('\n Order or Client NOT FOUND in database!')
                    print('\n Order OID: 0')
            
            if aux == '3':
                print(" -------------------------------------")
                print('\n Enter an client\'s CID: ', end='')
                cid_aux = input()
                print(' Enter an order\'s OID: ', end='')
                oid_aux = input()

                print('\n Enter the order\'s PRODUCT PID: ', end='')
                pid_aux = int(input())
                
                print(' Enter the order\'s new PRODUCT QUANTITY: ', end='')
                qtd_aux = input()

                aux = {}
                
                chave = {pid_aux:qtd_aux}
                aux.update(chave)

                response = stub.UpdateOrder(projeto_pb2.Order(OID = oid_aux, CID = cid_aux, data = json.dumps(aux)))
                
                if response.error == 0:
                    print(" Order successfully updated.\n")
                else:
                    print(response.description)

            if aux == '4':
                print(" -------------------------------------")
                print('\n Enter an client\'s CID: ', end='')
                cid_aux = input()
                print(' Enter an order\'s OID: ', end='')
                oid_aux = input()

                response = stub.DeleteOrder(projeto_pb2.ID(ID = f'{oid_aux}-{cid_aux}'))
                
                if response.error == 0:
                    print(" Order successfully deleted!\n")
                else:
                    print(response.description)

            if aux == '5':
                print(" -------------------------------------")
                print('\n Enter an client\'s CID: ', end='')
                cid_aux = input()

                response = stub.RetrieveClientOrders(projeto_pb2.ID(ID = cid_aux))
                
                print("-------------------------")
                
                for value in response:
                    print(value)    


if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        port = '50051'
    else:
        port = sys.argv[1]
         
    run(port)