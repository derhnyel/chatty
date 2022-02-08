import socket 
import threading
import logging
#change all prints to log
#host_name  = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
#os.system("clear")
class SocketServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        _ip_port = ('127.0.0.1',12345)
        self.socket.bind(_ip_port)
        self.socket.listen(5)
        self.list_of_clients = []
        self.dict_of_clients_sockets={}
        self.user_list=[]


    def send_message(self,connection,msg):
        connection.sendall(msg.encode('utf-8'))

    def recieve_message(self): 
        try:
            connection = self.connect
            addr = self.addr
            user = connection.recv(1024).decode()  
            while user in self.user_list:
                connection.sendall('not'.encode('utf-8'))
                user = connection.recv(1024).decode()
            connection.sendall('ok'.encode('utf-8'))
         
            self.list_of_clients.append(connection)
            self.user_list.append(user)
            self.dict_of_clients_sockets[connection]=(user,addr)
            intro_broadcast= "\n New User "+user+ " has joined the chatroom"
            users_in_chatroom ="\n Number of users in Chatroom: " +str(len(self.list_of_clients))
            welcome_message = "\n Welcome to this chatroom " +user+". You can start typing on the terminal"
            #use maps here
            self.send_message(connection=connection, msg=welcome_message)    
            self.send_message(connection,msg=users_in_chatroom)
            self.broadcast(connection,intro_broadcast)
            self.broadcast(connection,users_in_chatroom)
            print(addr[0]+ " "+str(addr[1])+ " connected")
            print("\n New User "+user+ " has joined the chatroom @" + str(self.addr[0] +":"+ str(self.addr[1])))
            print(users_in_chatroom)
        except:
            return False
        while True:
            try:
                message = connection.recv(1024).decode()
                if message.startswith('@send'):
                    ftn,r_name,r_msg= message.split(":")
                    for i,j in self.dict_of_clients_sockets.items():
                        if r_name == j[0] and r_name!=user:
                            p_msg = "\n <private message from @" +user+ ">:" + r_msg
                            i.sendto(p_msg.encode('utf-8'),j[1])
                            print("\n <@"+addr[0]+":"+str(addr[1])+" to @"+j[1][0]+":"+str(j[1][1])+">:"+r_msg)
                            check = True
                            break
                        else:
                            check = False
                    if not check:
                        self.send_message(connection,'\n No User Exist with that name')        

                elif  message.startswith('@users'):
                    self.send_message(connection,"\n Users in Chatroom:")
                    for i in self.user_list:
                        if i==user:
                            self.send_message(connection,'\n'+i+' (you)')
                        else:    
                            self.send_message(connection,'\n'+i)
                elif message:
                    print("\n <@"+addr[0]+":"+str(addr[1])+">"+message)
                    message_to_broadcast = "\n <" +user+ ">:" + message
                    self.broadcast(connection,message_to_broadcast)    
                else:
                    if connection in self.list_of_clients:
                        self.list_of_clients.remove(connection)
                        print('\n Removed client') 
            except:
                continue
    
    def check_for_available_users(self):
        message =''
        while True:
            for sock in self.list_of_clients:
                try:
                    sock.sendall(message.encode('utf-8'))
                except Exception as e:
                        user,addr=self.dict_of_clients_sockets.get(sock)
                        self.list_of_clients.remove(sock)
                        self.user_list.remove(user)
                        self.dict_of_clients_sockets.pop(sock) 
                        if user!='':
                            b_msg="\n"+ user+" has left chatroom"
                            self.broadcast(sock,message=b_msg) 
                            print('\n Removed client: ' + user+' @'+str(addr)+' from clients list') 
                            print("\n Number of users in Chatroom: " +str(len(self.list_of_clients)))
                          


    def broadcast(self,connection,message):
        for clients in self.list_of_clients:
            if clients != connection:
                try:
                    clients.sendall(message.encode('utf-8'))
                except:
                    clients.close()
                      
    def main(self):
        try:
            self.connect,self.addr = self.socket.accept()   
        except:
            return False    



server = SocketServer()
print('CHAT SERVER STARTED')
recieve_thread = threading.Thread(target=server.check_for_available_users)
recieve_thread.daemon = True
recieve_thread.start()
while True:
    server.main()
    threading._start_new_thread(server.recieve_message, ())    
    #add waitkey fuct
    #server.connect.close()
    #server.socket.close()




