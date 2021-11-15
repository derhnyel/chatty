import socket
import threading
import select

#Add Encrytion
#Remeber UsersInChatroom
#Make it a Django project


class SocketClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        _ip_port = ("127.0.0.1",12345)
        self.socket.connect(_ip_port)
        self.sockets_list=[]
        self.name = input("\nEnter a name: ")
        self.message = None
        if self.name!= '':
            self.send_message(self.name)
            self.message = self.socket.recv(1024).decode() 
        else:
            print('\nInvalid name:')
        #print(self.message)
        #if self.message=='error':
               # raise Exception         
        while self.message != 'ok':
            self.name = input("\nEnter another name: ")
            if self.name != '':
                self.send_message(self.name)           
                self.message = self.socket.recv(1024).decode()
                #if self.message=='error':
                #    raise Exception 
                if self.message!= 'ok':
                    print('\nA user already exists by that name')
            else:
                print('\nInvalid name')
                

           



    def send_message(self,message):
        self.socket.send(message.encode())

    def recieve_message(self):
            message = self.socket.recv(1024).decode()
            return message
    def recieve_response(self):
        self.message='' 
        while True:
            self.sockets_list = [self.socket]
            read_sockets, write_socket, error_socket = select.select(self.sockets_list, [], [],0)
            if len(read_sockets) < 1:
                    if self.message!='':
                        self.send_message(self.message)
                        print("\n<YOU>: " + self.message)
                        self.message=''
                    else:
                        continue          
            else:
                for socks in read_sockets:
                    if socks == self.socket:
                        message = self.recieve_message()
                        print("\n"+message)       
                continue
    def main(self):
        while True:
            self.message = input()
                   


client = SocketClient()
recieve_thread = threading.Thread(target=client.recieve_response)
recieve_thread.daemon=True
recieve_thread.start()
client.main()
client.socket.close()




