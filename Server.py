import time
from socket import *
import sys
import os
import logging


class Server:
    def __init__(self,port):
        self.port = port
        self.csocket = None
        self.dsocket = None
        self.buffer = 4096
        self.accounts = accounts = {"cs472" : "hw2ftp",
            "cme66" : "hi"}

    def connect(self):
        servSock = socket(AF_INET, SOCK_STREAM)
        servSock.bind(('',self.port))
        servSock.listen(1)
        #self.csocket, addr = servSock.accept()
        #self.send("220 Service ready for new user.\r\n")
        self.run(servSock)

    def send(self, message):
        self.csocket.send(message.encode())

    def receive(self):
        message_bytes = b''
        self.csocket.settimeout(5)
        while True:
            try:
                received = self.csocket.recv(self.buffer)
            except timeout:
                break
            message_bytes += received
            if b'\r\n' in message_bytes:
                break
            if len(received) == 0:
                break
        #self.log.info("The server sent the following response. \'{}\'".format(message_bytes.decode()))
        #print(message_bytes.decode())
        # print(msg_received)
        return message_bytes

    def getCommand(self,message):
        command = message.decode().split(" ")
        #print(command)
        return command[0]

    def getContent(self,message):
        response = message.decode().split(" ")
        if len(response) > 1:
            sent = response[1].replace("\r\n","")
            return sent
        else:
            return None

    def user(self):
        self.send("331 User name received, need password\r\n")
        answer = self.receive()
        return answer

    #Need to see how I can check what users are valid and what users are not
    #Come back to this later

    def pas(self,username,password):
        #username = username.replace("\r\n","")
        #password = password.replace("\r\n","")
        if(username in self.accounts and self.accounts[username] == password):
            self.send("230 User logged in, proceed.\r\n")
            answer = self.receive()
            return answer
        else:
            self.send("550 Not logged in.\r\n")
            self.csocket.close()
            return "QUIT"

    def quit(self):
        self.send("Now closing...\r\n")

    def cwd(self,message):
        if os.path.exists(message):
            os.chdir(message)
            self.send("250 The path has been successfully changed.\r\n")
        else:
            self.send("500 Path not found.\r\n")

    def pwd(self):
        directory = os.getcwd()
        self.send("257 The current working directory is {}\r\n".format(directory))

    #Need to check for users that are valid and their corresponding passwords

    def run(self,servSock):
        while True:
            self.csocket, addr = servSock.accept()
            self.send("220 Service ready for new user.\r\n")
            sentence = self.receive()
            #print(sentence)
            command = self.getCommand(sentence)
            #print(command)
            username = self.getContent(sentence)
            if command == "USER":
                response = self.user()
                #print(response)
                command = self.getCommand(response)
                password = self.getContent(response)
                #print(password)
                if command == "PASS":
                    answer = self.pas(username,password)
                    if answer == "QUIT":
                        break
                        exit(0)
                    else:
                        while True:
                            message = self.receive()
                            command = self.getCommand(message)
                            content = self.getContent(message)
                            if command == "CWD":
                                self.cwd(content)
                            if command == "PWD":
                                self.pwd()



            self.csocket.close()
            exit(0)

def main():
    serv = Server(2022)
    serv.connect()

if __name__ =="__main__":
    main()