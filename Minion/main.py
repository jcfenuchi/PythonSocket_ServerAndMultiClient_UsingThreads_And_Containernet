import socket
from time import sleep
from sys import argv

class MIS_Socket:
    def __init__(self, CoreIp, CorePort):
        self.__coreIP, self.__corePort = CoreIp,CorePort
        self.__sock = None
        self.Minion_routine()

    def create_socket(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__coreIP,self.__corePort))

    def Minion_routine(self):
        self.create_socket()
        self.msg_sayHI()
        self.__sock.close()

    def msg_sayHI(self):
        try:
            while True:
                self.send_data(f'Minion says: Hello world!')
                received_msg = self.receiver_data()
                print(f'Received from Core: {received_msg}')
                sleep(10)
        except Exception:
            print('Socket connection failed. Retrying...')
            self.Minion_routine()

    # ----------------------- Functions for communication
    def receiver_data(self):
        message = ''
        while True:
            data = self.__sock.recv(1024).decode('utf-8')
            message += data    
            if '[CoreEND]' in message: return message.replace('[CoreSTART]','').replace('[CoreEND]','')
    
    def send_data(self,message):
        self.__sock.sendall(f'{message}[MinionEND]'.encode('utf-8'))

if __name__ == "__main__":
    MIS_Socket(argv[1],int(argv[2])) # ip alterado por segurança