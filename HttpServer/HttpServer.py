#coding=utf-8
'''
name : zjs
time : 2019-9-7
httpserver v3.0
'''

from socket import *
import sys
import re
from threading import Thread
from settings import *
import time

class HTTPServer(object):
    def __init__(self,addr=('0.0.0.0',80)):
        self.sockfd=socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr=addr

        self.bind(addr)
    def bind(self,addr):
        self.ip=addr[0]
        self.port=addr[1]
        self.sockfd.bind(addr)

    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d...'%self.port)
        while True:
            connfd,addr=self.sockfd.accept()
            print('Connect from',addr)

            handle_client=Thread\
            (target=self.handle_request,args=(connfd,))
            handle_client.start()

    def handle_request(self,connfd):
        request=connfd.recv(4096)
        # print(request)
        request_lines=request.splitlines()
        request_line=request_lines[0].decode()
        
        pattern=r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env=re.match(pattern,request_line).groupdict()
        except:
            response_headlers='HTTP/1.1 500 Server ERROR\r\n'
            response_headlers+='\r\n'
            response_body='Server Error'
            response=response_headlers+response_body
            connfd.send(response.encode())
            return
        
        status,response_body=\
        self.send_request(env['METHOD'],env['PATH'])

        response_headlers=self.get_headlers(status)

        response=response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()


    def send_request(self,method,path):
        s=socket()
        s.connect(frame_addr)
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status=s.recv(128).decode()
        response_body=s.recv(4096*10).decode()
        # print(status,response_body)

        return status,response_body

    def get_headlers(self,status):
        if status=='200':
            response_headlers='HTTP/1.1 200 ok\r\n'
            response_headlers+='\r\n'
        elif status=='404':
            response_headlers='HTTP/1.1 404 NOT Found\r\n'
            response_headlers+='\r\n'

        return response_headlers        






if __name__=='__main__':
    httpd=HTTPServer(ADDR)
    httpd.serve_forever()

