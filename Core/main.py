from threading import Thread, Event
import socket


class Core_Socket:
    def __init__(self, server_IpAddress,server_Port):
        self.clients_conected = {}
        self.__coreIP = server_IpAddress
        self.__corePort = server_Port
        self.create_socket()
        
    def create_socket(self):
        self.__socket = socket.socket()
        self.__socket.bind((self.__coreIP,self.__corePort))
        print("socket created")
        self.__socket.listen()
        event = Event()
        
        while True:
          try:
            conn, address = self.__socket.accept()
            self.clients_conected[address] = Thread(target=self.client_handle_connection, args=(event, conn, address))
            self.clients_conected[address].start()
          except KeyboardInterrupt:
            event.set()
            print('Processo de desconexão finalizado.')
            exit()
          except Exception as ex:
            print(f'Error: {str(ex)}')
             

    def client_handle_connection(self, event, client_sock, address):
        print(f"{client_sock}, {address} aceita")
        loop_condition = 0
        while loop_condition != 1:
            if event.is_set():
                break
            received_msg = self.receiver_data(client_sock)
            # Only echo message
            if received_msg == 'exit' or received_msg == 'MINION_CONNECTION_CLOSED':
                loop_condition = 1
            else:
                # Send reply message to client
                print(f"replyng to msg: {received_msg} to {address}")
                self.send_data(client_sock, received_msg)
        
        client_sock.close()
        self.clients_conected.pop(address)
        print(f'{address} desconectado')



    def send_data(self, connection, message: str):
      connection.sendall(f'[CoreSTART]{message}[CoreEND]'.encode('utf-8'))

    def receiver_data(self,connection):
      message = ''
      while True:
        data = connection.recv(1024).decode('utf-8')
        message += data
        if '[MinionEND]' in data: return message.split('[MinionEND]')[:-1]
        if not data: return ['MINION_CONNECTION_CLOSED']

if __name__ == '__main__':
  Core = Core_Socket('0.0.0.0',6618)