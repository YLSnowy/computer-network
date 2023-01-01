import tkinter
from tkinter import *
import socket, threading
import time
import os

server_window = tkinter.Tk()
server_window.title('服务器')
server_window.geometry("400x300+200+20")
users = {}


def run(connect, addrss):
    message = connect.recv(1024).decode("utf-8")
    userName = message.split()[0]
    user_ip = message.split()[1]
    user_port = message.split()[2]
    print(userName)
    print(user_ip)
    print(user_port)

    user_info = []
    user_info.append(connect)
    user_info.append(user_ip)
    user_info.append(user_port)
    users[userName] = user_info

    text.insert(tkinter.INSERT, userName + "连接\n")
    dir = os.getcwd()
    file = dir + "/log.txt"
    with open(file, mode='a', encoding='utf-8') as file_obj:
        file_obj.write(userName + "连接\n")

    printStr ="登录成功!\n"+"当前在线的好友有："+str(list(users.keys()))+"\n"
    for key in users:
        printStr += key + ":ip: " + users[key][1] + " port: " + users[key][2] + "\n"
    connect.send(printStr.encode())

    printStr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
    printStr += userName + "已上线\n"+"当前在线的好友有：\n"
    for key in users:
        printStr += key + ":ip: " + users[key][1] + " port: " + users[key][2] + "\n"
    print(printStr)
    for key in users:
        if key != userName:
            users[key][0].send(printStr.encode())

    while True:
        rData = connect.recv(1024)
        print(rData)
        dataStr = rData.decode("utf-8")

        infolist = dataStr.split(":")

        if len(infolist[0]) == 0:
            for key in users:
                if key != userName:
                    users[key][0].send((userName + "说（群发）:" + infolist[1]).encode("utf"))

        elif infolist[0] == "exit":
            del users[userName]
            printStr = "" + userName + "下线\n"
            dir = os.getcwd()
            file = dir + "/log.txt"
            with open(file, mode='a', encoding='utf-8') as file_obj:
                file_obj.write(userName + "下线\n")
            text.insert(tkinter.INSERT, printStr)
            for key in users:
                printStr = userName + "已下线\n"+"当前在线的好友有："+str(list(users.keys()))+"\n"
                users[key][0].send(printStr.encode())
                                
        else:
            print(infolist[0])
            print("=================")
            print(infolist[0]=='a')              
            if infolist[0] in users:
                users[infolist[0]][0].send((userName + "说(私聊):" + infolist[1]).encode("utf"))
            else:
                printStr =infolist[0]+"不在线，上条消息未发出"+"\n"
                connect.send(printStr.encode())
                                        

def startSever():
    s = threading.Thread(target=start)    
    s.start()

    
def start():
    ipStr = textServer.get("0.0",END).split(":")[0]
    ipStr = ipStr.rstrip("\n")
    portStr = textServer.get("0.0", END).split(":")[1]
    portStr = portStr.rstrip("\n")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipStr, int(portStr)))
    server.listen(10)

    text.insert(tkinter.INSERT, "服务器启动成功！\n")

    while True:
        connect, addrss = server.accept()
        t = threading.Thread(target=run, args=(connect, addrss))
        t.start()


labelServer = tkinter.Label(server_window, text="ip:Port").grid(row=1, column=0)
eserver = tkinter.Variable()
textServer = tkinter.Text(server_window, height=1, width=35)
textServer.grid(row=1, column=1)


button = tkinter.Button(server_window, text="启动", command=startSever).grid(row=1, column=2,padx=5)
text = tkinter.Text(server_window, height=15, width=35)
labeltext = tkinter.Label(server_window, text='连接消息').grid(row=3, column=0)
text.grid(row=3, column=1)

server_window .mainloop()

