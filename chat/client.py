import tkinter
from tkinter import *
import socket
import threading
import time
import pymysql

login_window = tkinter.Tk()
login_window.title('登录')
login_window.geometry("300x100")


textUsername = None
textServer = None
textClient = None
text = None
textSend = None
textFriend = None

users = {}


ck = None
client = None
friend = None

def Register():
    username = textUsername0.get("0.0",END).rstrip("\n")
    password = textPassword.get("0.0",END).rstrip("\n")

    if username == "":
        child_windows = tkinter.Tk()
        child_windows.title('错误消息')
        child_windows.geometry("300x150")
        text1 = tkinter.Text(child_windows, height=15, width=35)
        labeltext = tkinter.Label(child_windows).grid(row=3, column=0)
        text1.grid(row=3, column=1)
        text1.insert(tkinter.INSERT, "用户名为空, 请输入用户名\n")
        child_windows.focus_force()
        child_windows.mainloop()
        return -1

    conn=pymysql.connect(host = '127.0.0.1',user = 'root',passwd='123456',port= 3306,db='user',charset='utf8')

    cur = conn.cursor() # 生成游标对象
    sql="select username from `user` " # SQL语句
    cur.execute(sql) # 执行SQL语句
    data = cur.fetchall() # 通过fetchall方法获得数据
    for i in data: # 打印输出前2条数据
        print(i)
        if username == i[0]:
            child_windows = tkinter.Tk()
            child_windows.title('错误消息')
            child_windows.geometry("300x150")
            text1 = tkinter.Text(child_windows, height=15, width=35)
            labeltext = tkinter.Label(child_windows).grid(row=3, column=0)
            text1.grid(row=3, column=1)
            text1.insert(tkinter.INSERT, "用户名已存在, 请重新输入")
            child_windows.focus_force()
            child_windows.mainloop()

            return -1
    sql = "insert into user values(%s,%s,%s)"
    param = (username, password, "")
    print(sql)
    cur.execute(sql,param) # 执行SQL语句
    sql="select * from `user` " # SQL语句
    print(sql)
    cur.execute(sql) # 执行SQL语句
    conn.commit()
    data = cur.fetchall() # 通过fetchall方法获得数据
    for i in data[:2]: # 打印输出前2条数据
        print(i)
    cur.close() # 关闭游标
    conn.close() # 关闭连接
    return 0

def Authentication():
    username = textUsername0.get("0.0",END).rstrip("\n")
    password = textPassword.get("0.0",END).rstrip("\n")

    if username == "":
        child_windows = tkinter.Tk()
        child_windows.title('错误消息')
        child_windows.geometry("300x150")
        text1 = tkinter.Text(child_windows, height=15, width=35)
        labeltext = tkinter.Label(child_windows).grid(row=3, column=0)
        text1.grid(row=3, column=1)
        text1.insert(tkinter.INSERT, "用户名为空, 请输入用户名\n")
        child_windows.focus_force()
        child_windows.mainloop()
        return -1

    conn=pymysql.connect(host = '127.0.0.1',user = 'root',passwd='123456',port= 3306,db='user',charset='utf8')

    cur = conn.cursor() # 生成游标对象
    sql="select * from `user` " # SQL语句
    cur.execute(sql) # 执行SQL语句
    data = cur.fetchall() # 通过fetchall方法获得数据
    # for i in data: # 打印输出前2条数据
    #     print(i)
    flag = 0
    for i in range(len(data)):
        if username == data[i][0] and password == data[i][1]:
            flag = 1
        elif username == data[i][0]:
            flag = 2
        
    if flag == 0:
        child_windows = tkinter.Tk()
        child_windows.title('错误消息')
        child_windows.geometry("300x150")
        text1 = tkinter.Text(child_windows, height=15, width=35)
        labeltext = tkinter.Label(child_windows).grid(row=3, column=0)
        text1.grid(row=3, column=1)
        text1.insert(tkinter.INSERT, "用户名不存在, 请注册\n")
        child_windows.focus_force()
        child_windows.mainloop()
        return -1
    elif flag == 2:
        child_windows = tkinter.Tk()
        child_windows.title('错误消息')
        child_windows.geometry("300x150")
        text1 = tkinter.Text(child_windows, height=15, width=35)
        labeltext = tkinter.Label(child_windows).grid(row=3, column=0)
        text1.grid(row=3, column=1)
        text1.insert(tkinter.INSERT, "密码不正确, 请重新输入\n")
        child_windows.focus_force()
        child_windows.mainloop()
        return -1

    cur.close() # 关闭游标
    conn.close() # 关闭连接
    return username


# 服务器在每个用户上线/下线的时候告诉所有用户现有的用户以及相应的ip
def groupChat():
    while True:
        data = ck.recv(1024).decode("utf-8")#用于接受服务其发送的信息
        print(data)
        data = data.split("\n")
        # print(data)
        for i in range(2,len(data)):
            name = ""
            ip = ""
            port = ""
            flag = 0
            if len(data) == 0:
                continue
            for j in range(len(data[i])):
                if data[i][j] != ":" and flag == 0:
                    name += data[i][j]
                elif flag == 0:
                    flag = 1

                if data[i][j] == 't':
                    flag = 2
                if (data[i][j] >= '0' and data[i][j] <= '9'  or data[i][j] == '.') and flag == 1:
                    ip += data[i][j]

                if data[i][j] >= '0' and data[i][j] <= '9' and flag == 2:
                    port += data[i][j]
            if name != "":
                users[name] = []
                users[name].append(ip)
                users[name].append(port)
        print(users)
        text.insert(tkinter.INSERT, data)
        text.insert(tkinter.INSERT, "\n")


def privateChat():
    while True:
        data = client.recv(1024).decode("utf-8")#用于接受服务其发送的信息
        print(data)
        text.insert(tkinter.INSERT, data)
        text.insert(tkinter.INSERT, "\n")


def connectServer():
    client_name_str = textUsername.get('0.0', END)
    client_name_str = client_name_str.rstrip("\n")
    print(client_name_str)

    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    client_ip_str = textClient.get('0.0', END).split(":")[0]
    client_ip_str = client_ip_str.rstrip("\n")
    client_port_str = textClient.get('0.0',END).split(":")[1]
    client_port_str = client_port_str.rstrip("\n")
    print(client_port_str)
    print(type(client_port_str))
    client.bind((client_ip_str,int(client_port_str)))
    # text.insert(tkinter.INSERT, client_name_str+" "+client_ip_str+" "+client_port_str)

    global ck#全局
    server_ip_str = textServer.get("0.0", END).split(":")[0]
    server_ip_str = server_ip_str.rstrip("\n")
    server_port_Str = textServer.get("0.0", END).split(":")[1]
    server_port_Str = server_port_Str.rstrip("\n")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4相关协议
    try:
        server.connect((server_ip_str, int(server_port_Str)))#连接服务器
    except:
        text.insert(tkinter.INSERT,"登陆失败, 请检查服务器ip是否正确, 以及客户端的ip是否重复\n")
    
    server.send((client_name_str+" "+client_ip_str+" "+client_port_str).encode("utf-8"))#将自己的登录名发送给服务器，函数会附带自己的IP信息
    ck = server
    t = threading.Thread(target=groupChat)
    t.start()
    t1 = threading.Thread(target=privateChat)
    t1.start()


def sendMail():
    global friend
    friend_name = textFriend.get("0.0", END).rstrip("\n")
    try:
        friend_ip_str = users[friend_name][0]
        friend_port_str = users[friend_name][1]
    except:
        if friend_name != "":
            text.insert(tkinter.INSERT,"输入昵称不存在, 请重新输入\n")
    
    sendStr = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())
    username  = textUsername.get("0.0", END).rstrip("\n")
    sendStr += username
    sendStr += ":"
    sendStr += textSend.get("0.0", END)
    # sendStr += sendStr.rstrip("\n")
    
    if len(friend_name) != 0:
        text.insert(tkinter.INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'+'我对'+friend_ip_str+":"+friend_port_str+'说：' + sendStr+'\n')
        print(textFriend.get("0.0",END))
        
        friend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sendStr = sendStr + "\n"
        client.sendto(sendStr.encode(), (friend_ip_str,int(friend_port_str)))
    else:        
        for key in users:
            if key != username:
                client.sendto(sendStr.encode(), (users[key][0], int(users[key][1])))
    
def Exit():
    sendStr = "exit" + ":" + ""
    ck.send(sendStr.encode("utf-8"))
    text.insert(tkinter.INSERT, "您已下线，如需接收信息请重新登录。\n")


#下面是界面
def Login():
    ret = Authentication()
    if ret == -1:
        return
    client_window = tkinter.Tk()
    client_window.title("客户端")
    client_window.geometry("400x300+300+200")

    global textServer
    global textClient
    global textUsername
    global text
    global textSend
    global textFriend

    labelUsername = tkinter.Label(client_window, text="userName").grid(row=0, column=0)
    eusername = tkinter.Variable()
    textUsername = tkinter.Text(client_window, height=1, width=35)
    textUsername.grid(row=0, column=1,padx=10)
    textUsername.insert(tkinter.INSERT, ret)

    labelServer = tkinter.Label(client_window, text="服务器ip:Port").grid(row=1, column=0)
    eserver = tkinter.Variable()
    textServer = tkinter.Text(client_window, height=1, width=35)
    textServer.grid(row=1, column=1)


    Labelclient = tkinter.Label(client_window, text="客户端ip:Port").grid(row=2, column=0)
    eclient = tkinter.Variable()
    textClient = tkinter.Text(client_window, height=1, width=35)
    textClient.grid(row=2, column=1)


    button = tkinter.Button(client_window, text="连接", command=connectServer).grid(row=0, column=2,padx=5)

    text = tkinter.Text(client_window, height=10, width=35)
    labeltext= tkinter.Label(client_window, text="显示消息").grid(row=4, column=0)
    text.grid(row=4, column=1)


    labelesend = tkinter.Label(client_window, text="发送的消息").grid(row=5, column=0)
    esend = tkinter.Variable()
    textSend = tkinter.Text(client_window, height=1, width=35)
    textSend.grid(row=5, column=1)


    labelefriend= tkinter.Label(client_window, text="发给谁").grid(row=6, column=0)
    efriend = tkinter.Variable()
    textFriend = tkinter.Text(client_window, height=1, width=35)
    textFriend.grid(row=6, column=1)

    button2 = tkinter.Button(client_window, text="发送", command=sendMail).grid(row=6, column=2)
    button2 = tkinter.Button(client_window, text="下线", command=Exit).grid(row=2, column=2)
    login_window.destroy()
    client_window.focus_force()
    client_window.mainloop()


labelUsername0 = tkinter.Label(login_window, text="用户名").grid(row=0,column=0)
eusername0 = tkinter.Variable()
textUsername0 = tkinter.Text(login_window, height=1, width=35)
textUsername0.grid(row=0,column=1)

labelpassword = tkinter.Label(login_window,text="密码").grid(row=1,column=0)
epassword = tkinter.Variable()
textPassword = tkinter.Text(login_window, height=1,width=35)
textPassword.grid(row=1,column=1)

button_Login = tkinter.Button(login_window,text="登录",command=Login).grid(row=6, column=1,padx=5)


button_Register = tkinter.Button(login_window, text="注册", command=Register).grid(row=6, column=0,padx=5)


login_window.mainloop()