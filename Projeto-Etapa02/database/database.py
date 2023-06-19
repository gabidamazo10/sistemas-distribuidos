from __future__ import print_function
from leveldb import Database

import sys
import socket
import threading
import json
            
def funcoesBanco(replica, conn, addr):
    while True:
        data = conn.recv(2048)
        msg = data.decode()
        if msg:
            responseMsg = json.loads(msg)
            functionName = responseMsg['function']
            key = responseMsg['key']
            value = responseMsg['value']
            
        if functionName == 'insert':           
            replica.insertData(key, value)            
            resp = json.dumps({'msg': "Insert realizado com sucesso."})

        if functionName == 'read':
            response = replica.getData(key)
            
            if response != '':
                response = json.loads(response)    
            
            resp = json.dumps({'data': response})

        if functionName == 'delete':
            replica.deleteData(key)
            resp = json.dumps({'msg': "Delete realizado com sucesso."})


        conn.send(resp.encode())

def run():
    if len(sys.argv) < 2:
        sys.exit(-1)

    arg = int(sys.argv[1])

    if arg not in [1, 2, 3, 4, 5, 6]:
        print("Escolha: 1, 2, 3, 4, 5 ou 6")
        sys.exit(-1)
    
    # Partição 1
    if arg == 1:
        portaSocket = 10000
        replica = Database(portaSocket, 'particao00', 'localhost:20000',['localhost:20002', 'localhost:20004'])
    if arg == 2:
        portaSocket = 10002
        replica = Database(portaSocket, 'particao00', 'localhost:20002',['localhost:20000', 'localhost:20004'])
    if arg == 3:
        portaSocket = 10004
        replica = Database(portaSocket, 'particao00', 'localhost:20004',['localhost:20000', 'localhost:20002'])
    
    # Partição 2
    if arg == 4:
        portaSocket = 10001
        replica = Database(portaSocket, 'particao01', 'localhost:20001',['localhost:20003', 'localhost:20005'])
    if arg == 5:
        portaSocket = 10003
        replica = Database(portaSocket, 'particao01', 'localhost:20003',['localhost:20001', 'localhost:20005'])
    if arg == 6:
        portaSocket = 10005
        replica = Database(portaSocket, 'particao01','localhost:20005',['localhost:20001', 'localhost:20003'])

    sock = socket.socket()
    host = socket.gethostname()
    sock.bind((host, portaSocket))
    sock.listen(15)
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=funcoesBanco, args=(replica, conn, addr)).start()


if __name__ == '__main__':
    run()