
# 从http.server模块中导入BaseHTTPRequestHandler类和HTTPServer类
from http.server import BaseHTTPRequestHandler,HTTPServer

# 创建一个类RequestHandler继承类BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    '''通过返回一个固定的网页来处理http请求'''
    # 要返回的网页
    Page = '''\
<html>
    <body>
        <p>Hello,web!</p>
    </body>
</html>
'''

    # 处理一个GET请求
    def do_GET(self):
        # 先发送http状态码，200,表示请求成功
        self.send_response(200)
        # 再发送响应头，告诉浏览器，接下来返回的内容类型是html
        self.send_header("Content-Type","text/html")
        # 告诉浏览器接下来返回的内容长度
        body=self.Page.encode('utf-8')
        self.send_header("Content-Length",str(len(body)))
        # 告诉浏览器响应头发完了
        self.end_headers();
        # wfile，BaseHTTPRequestHandler提供的一个“写文件对象”
        # str.encode('utf-8')把字符串编码成utf-8格式的字节序列
        # python3中str本身是Unicode，write()只接受bytes
        self.wfile.write(self.Page.encode('utf-8'))
if __name__ == '__main__':
    # 提供服务的地址，空ip代表127.0.0.1，端口号是8080
    # 一个元组
    serverAddress = ('127.0.0.1',8080)
    # BaseHTTPServer模板中的HTTPServer类(地址，请求处理类)
    server = HTTPServer(serverAddress,RequestHandler)
    # 启动服务
    server.serve_forever()    
