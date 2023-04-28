import projeto_pb2
import projeto_pb2_grpc
import grpc

import json
import ast

import sys

def run(port):  

    with grpc.insecure_channel('localhost:'+ port, options=(("grpc.enable_http_proxy", 0),)) as channel:
        
        
        stub = projeto_pb2_grpc.AdminPortalStub(channel)
        aux = 0 

        while aux != '9':
            
            print('\n ------------------------------------- ')
            print('|            ADMIN PORTAL             |')
            print(' ------------------------------------- ')
            print('|   Welcome to the Admin Portal!      |')
            print(' ------------------------------------- ')
            print('|  1. Create client                   |')
            print('|  2. Retrieve Client                 |')
            print('|  3. Update Client                   |')
            print('|  4. Delete Client                   |')
            print('|  5. Create Product                  |')
            print('|  6. Retrieve Product                |')
            print('|  7. Update Product                  |')
            print('|  8. Delete Product                  |')
            print('|  9. Sair                            |')
            print(' ------------------------------------- ')
            print(' Choose an option: ', end='')
            aux = input()   
            
            if aux == '1':
                    print(" -------------------------------------")
                    print('\n Enter the client\'s NAME: ', end='')
                    name_aux = input()
                    print(' Enter the client\'s CID: ', end='')
                    id_aux = input()
                    
                    response = stub.CreateClient(projeto_pb2.Client(data = name_aux, CID = id_aux))
                    
                    if response.error == 0:
                        print('\n Client created with success!')
                    else:
                        print(response.description)                
                
            if aux == '2': 
                print(" -------------------------------------")
                print('\n Enter the client\'s CID: ', end='')
                id_aux = input()

                response = stub.RetrieveClient(projeto_pb2.ID(ID = id_aux))
                if response.data != 'NOT_FOUND':
                    print('\n Client data: ' + response.data)
                    print(' Client CID: ' + response.CID)
                else: 
                    print('\n Client NOT FOUND in database!')
                    print(' Client CID: 0')
                    
            if aux == '3':
                print(" -------------------------------------")
                print('\n Enter the client\'s CID to modify: ', end='')
                id_aux = input()
                
                response = stub.RetrieveClient(projeto_pb2.ID(ID = id_aux))
                
                if response.data != 'NOT_FOUND':
                    print('\n Client NAME: ' + response.data)
                    print(' Client CID to modify: ' + response.CID)
                    
                    print("\n-------------------------------------")
                    print('\n Enter the client\'s NEW NAME: ', end='')
                    name_aux_new = input()
                
                    responseModify = stub.UpdateClient(projeto_pb2.Client(data = name_aux_new, CID = response.CID))
                
                    if responseModify.error == 0:
                        print('\n The client was updated!')
                    else:
                        print(responseModify.description)
                    
                else: 
                    print('\n Client NOT FOUND in database.\n')
                    
            if aux == '4':
                print(" -------------------------------------")
                print('\n Enter the client\'s CID to delete: ', end='')
                id_aux = input()
                
                response = stub.DeleteClient(projeto_pb2.ID(ID = id_aux))
                
                if response.error == 0:
                    print('\n The client was deleted from database!')
                else:
                    print(response.description)    
                    
            if aux == '5':
                print(" -------------------------------------")
                print('\n Enter the products\'s NAME: ', end='')
                name_aux = input()
                print(' Enter the products\'s ID: ', end='')
                id_aux = input()
                print(' Enter the products\'s CAPACITY: ', end='')
                capacity_aux = input()
                
                dados = {}
                
                dados['NAME'] = name_aux
                dados['CAPACITY'] = capacity_aux
                
                response = stub.CreateProduct(projeto_pb2.Product(PID = id_aux, data = json.dumps(dados)))

                if response.error == 0:
                        print('\n Product created with sucess!')
                else:
                        print(response.description)    
            
            if aux == '6':
                print(" -------------------------------------")
                print('\n Enter an product\'s PID: ', end='')
                id_aux = input()

                response = stub.RetrieveProduct(projeto_pb2.ID(ID = id_aux))
                if response.data != 'NOT_FOUND':
                    print('\n Product PID: ' + response.PID)
                    
                    dados = ast.literal_eval(response.data)
                    # print(dados)        
                    
                    print(' Product NAME: ' + dados['NAME'])
                    print(' Product CAPACITY: ' + dados['CAPACITY'])
                else: 
                    print('\n Product NOT FOUND in database.')
                    print(' Product PID: 0\n')
                    
            if aux == '7':
                print(" -------------------------------------")
                print('\n Enter the product\'s PID to modify: ', end='')
                id_aux = input()
                
                response = stub.RetrieveProduct(projeto_pb2.ID(ID = id_aux))
                
                if response.data != 'NOT_FOUND':
                    print(" -------------------------------------")
                    print('\n Enter the products\'s NEW NAME: ', end='')
                    name_aux = input()
                
                    print(' Enter the products\'s NEW CAPACITY: ', end='')
                    capacity_aux = input()
                
                    dados = {}
                
                    dados['NAME'] = name_aux
                    dados['CAPACITY'] = capacity_aux
                
                    responseModify = stub.UpdateProduct(projeto_pb2.Product(data = json.dumps(dados), PID = response.PID))
                
                    if responseModify.error == 0:
                        print('\n The product was updated!\n')
                    else:
                        print(responseModify.description)
                    
                else: 
                    print('\n Product NOT FOUND in database!\n')
            
            if aux == '8':
                print(" -------------------------------------")
                print('\n Enter the products\'s PID to delete: ', end='')
                id_aux = input()
                
                response = stub.DeleteProduct(projeto_pb2.ID(ID = id_aux))
                
                if response.error == 0:
                    print('\n The product was deleted from database!\n')
                else:
                    print(response.description)  
      
if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        port = '50051'
    else:
        port = sys.argv[1]
         
    run(port)