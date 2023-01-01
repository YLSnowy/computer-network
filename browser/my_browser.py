from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtGui
from PyQt5.QtWebEngineWidgets import *
import os
import sys
import socket
from socket import *


class ChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('新窗口')

        self.resize(700,400)
        self.textEdit = QTextEdit()
        self.textEdit.setFixedSize(700,400)

        self.label1 = QLabel() # 用于显示图片
        self.label1.setFixedSize(700,400)
        self.label1.setScaledContents(True)
        self.pixmap = QPixmap() # 用于显示图片
        self.pixmap.width=700
        self.pixmap.height=400

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0,0,0,0)     

    def get_url(self,url):
        if url == "no":
            self.textEdit.setPlainText("此链接不支持跳转，请重新选取")
            self.h_layout.addWidget(self.textEdit)
            self.setLayout(self.h_layout)
            return
        if url[0:5] == "https":
            url = url[8:]
            print(url)
        if url[-1] == '/':
            url = url[0:len(url)-1]
        HOST = url
        PORT = 80
        print(HOST)
        for res in getaddrinfo(HOST, PORT, AF_UNSPEC,SOCK_STREAM, 0, AI_PASSIVE):
            af, socktype, proto, canonname, sockaddr = res

            try:
                self.server = socket(af, socktype)
            except OSError as msg:
                self.server = None
                continue
            try:
                self.server.connect(sockaddr)
            except OSError as msg:
                self.server.close()
                self.server = None
                continue
            break
        self.request_line = "GET / HTTP/1.1\r\n"
        self.request_header = "Host:" + url +"\r\n"
        self.request_blank = "Connection: close\r\n\r\n"
        self.request_data = self.request_line + self.request_header + self.request_blank

        buf = []

        self.server.send(self.request_data.encode())
        
        while True:
            recv = self.server.recv(1024)
            # print(recv)
            if recv:
                buf.append(recv.decode('utf-8','ignore'))
            else:
                break

        data = ''.join(buf).encode()
        data = data.decode()
        self.recv_text = data
        self.textEdit.setPlainText(self.recv_text)

        self.h_layout.addWidget(self.textEdit)

        self.setLayout(self.h_layout)
        return


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        self.setWindowTitle('Lx_Browser')
        self.resize(1400, 800) 
        self.show()

        # # 添加URL地址栏
        self.urlbar = QLineEdit()
        self.urlbar2 = QLineEdit()
        # 让地址栏支持输入地址回车访问
        self.urlbar.returnPressed.connect(self.get_url)
        self.urlbar.setText("get")
        self.urlbar2.returnPressed.connect(self.head_url)
        self.urlbar2.setText("head")

        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        self.addToolBar(navigation_bar)
        navigation_bar.addWidget(self.urlbar)
        navigation_bar.addWidget(self.urlbar2)

        # 添加标签栏
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.add_new_tab(QUrl('https://www.baidu.com/'), 'Homepage')
        self.setCentralWidget(self.tabs)

        # 添加文本框，显示交互过程
        self.textEdit = QTextEdit()
        self.textEdit.setFixedSize(1400,400)

        # 用于显示html中的图片
        self.label1 = QLabel() # 用于显示图片
        self.label1.setFixedSize(700,400)
        self.label1.setScaledContents(True)
        self.pixmap = QPixmap() # 用于显示图片
        self.pixmap.width=700
        self.pixmap.height=400

        # 用于显示html中的问文本内容
        self.output = QTextBrowser()
        self.output.setFixedSize(700,200)

        # 用于显示html中的超链接，用表格的形式体现
        self.tableWidget = QTableWidget()
        self.tableWidget.setGeometry(QRect(0, 0, 700, 200))
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1) # 8行4列
        self.tableWidget.itemClicked.connect(self.click_href)

        # 设计整体页面的布局
        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0,0,0,0)
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0,0,0,0)
        self.v_layout0 = QVBoxLayout()
        self.v_layout0.setContentsMargins(0,0,0,0)


    def send_recv(self,opt):
        if opt == 1:
            url = self.urlbar.text()
            if url[0:5] == "https":
                url = url[8:]
            print(url)

            if url[0:3] == "www":
                HOST = url
            else:
                HOST = "www." + url
        else:
            url2 = self.urlbar2.text()
            if url2[0:5] == "https":
                url2 = url2[8:]

            if url2[0:3] == "www":
                HOST = url2
            else:
                HOST = "www." + url2
        
        PORT = 80
        for res in getaddrinfo(HOST, PORT, AF_UNSPEC,SOCK_STREAM, 0, AI_PASSIVE):
            af, socktype, proto, canonname, sockaddr = res

            try:
                self.server = socket(af, socktype)
            except OSError as msg:
                self.server = None
                continue
            try:
                self.server.connect(sockaddr)
            except OSError as msg:
                self.server.close()
                self.server = None
                continue
            break
        
        if opt == 1:
            self.request_line = "GET / HTTP/1.1\r\n"
            self.request_header = "Host:" + url +"\r\n"
        else:
            self.request_line = "HEAD / HTTP/1.1\r\n"
            self.request_header = "Host:" + url2 +"\r\n"
        self.request_blank = "Connection: close\r\n\r\n"
        self.request_data = self.request_line + self.request_header + self.request_blank

        buf = []

        self.server.send(self.request_data.encode())
        
        while True:
            recv = self.server.recv(1024)
            # print(recv)
            if recv:
                buf.append(recv.decode('utf-8','ignore'))
            else:
                break

        data = ''.join(buf).encode()
        data = data.decode()
        self.recv_text = data


    # 以get的方式发送请求
    def get_url(self):
        self.send_recv(1)
        # 将获得的结果解析出来，显示交互过程
        self.textEdit.setPlainText(self.request_data  + self.recv_text)

        # 找到html文件中的文字
        chinese = []
        place = -1
        for i in range(len(self.recv_text) - 1):
            i = place + 1
            if i < len(self.recv_text) and u'\u4e00' <= self.recv_text[i] <= u'\u9fff':
                ch = ''
                for j in range(i, len(self.recv_text)):
                    if u'\u4e00' <= self.recv_text[j] <= u'\u9fff':
                        ch += self.recv_text[j]
                        place = j
                    else:
                        chinese.append(ch)
                        place = j
                        break
            else:
                place += 1
        # print(chinese)

        for i in range(len(chinese)):
            self.output.append(chinese[i])
                    

        # 找到得到的html文件中的url，放在文本框中，并支持跳转
        urls = []
        for i in range(len(self.recv_text)-5):
            if self.recv_text[i:i+5] == 'href=': # 判断是链接
                # print(self.recv_text[i:i+5])
                url = 'https:'
                for j in range(i + 6, len(self.recv_text)-5):
                    if self.recv_text[j] == '\"':
                        urls.append(url)
                        # print(url)
                        break
                    url += self.recv_text[j]

        for i in range(len(urls)):
            item = QTableWidgetItem(urls[i])
            self.tableWidget.setItem(i,0,item)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
        

        # 解析html中的图片src标签
        img_src = 'https:'
        for i in range(len(self.recv_text)-4):
            if self.recv_text[i:i+4] == 'src=':
                # print(self.recv_text[i:i+4])
                img_src = 'https:'
                for j in range(i + 5, len(self.recv_text) - 5):
                    if self.recv_text[j] == '\"':
                        # print(img_src)
                        break
                    img_src += self.recv_text[j]

        if img_src != 'https:':
            from wget import download
            download(img_src)
            for i in range(len(img_src)-1,0,-1):
                if img_src[i] == '/':
                    self.local_dir = img_src[i+1:len(img_src)]
                    break
            self.local_dir = os.getcwd() + "/" + self.local_dir
            # print(self.local_dir)
            self.pixmap.load(self.local_dir)
            new_img = self.pixmap.scaled(700, 300)##调整图片尺寸
            self.label1.setPixmap(new_img)

        self.v_layout.addWidget(self.textEdit)
        self.h_layout.addLayout(self.v_layout0)
        self.v_layout0.addWidget(self.tableWidget)
        self.v_layout0.addWidget(self.output)
        
        if img_src != 'https':
            self.h_layout.addWidget(self.label1)

        
        self.v_layout.addLayout(self.h_layout)
        self.tabs.setLayout(self.v_layout)

    # 支持链接的点击事件，设置对应的跳转槽函数
    def click_href(self,Item=None):
        if Item is None:
            return
        else:
            text = Item.text()  # 获取内容
            print(text)
            self.child = ChildWindow()
            # self.child.url = text
            self.child.show()
            row = Item.row()
            deny = [0,1,6,9,10,11,14,15,17,18,19]
            if row in deny:
                self.child.get_url("no")
            else:
                self.child.get_url(text)
            # self.child.exec_()
            

    
    # 以head的方式发送请求
    def head_url(self):
        self.send_recv(2)
        self.textEdit.setPlainText(self.request_data  + self.recv_text)
        # print(self.recv_text)
        self.v_layout.addWidget(self.textEdit)
        self.tabs.setLayout(self.v_layout)
        

    def add_new_tab(self, qurl=QUrl(''), label='Blank'):
        # 设置浏览器
        self.browser = QWebEngineView(self)
        self.browser.load(qurl)
        # 为标签添加索引方便管理
        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)


# 创建应用
app = QApplication(sys.argv)
# 创建主窗口
window = MainWindow()

# 显示窗口
window.show()
# 运行应用，并监听事件
app.exec_()