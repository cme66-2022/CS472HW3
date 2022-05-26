import time
from socket import *
import sys
import os
import logging



def main():
    port = 2022

    servSock = socket(AF_INET, SOCK_STREAM)
    servSock.bind(('', port))
    servSock.listen(1)
    while True:
        Newsocket, addr = servSock.accept()
        send = Newsocket.send("220 it worked\r\n".encode())
        sentence = Newsocket.recv(4096).decode()
        caps = sentence.upper()
        print(caps)
        Newsocket.send(caps.encode())
        Newsocket.close()
        quitter = input("What is your name?")
        quitter = "YES"
        if(quitter  == "YES"):
            break

if __name__ =="__main__":
    main()