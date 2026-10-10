import os
# 从模板中导入类
from http.server import BaseHTTPRequestHandler,HTTPServer

# 定义一个名为ServerException的类，继承Exception
class ServerException(Exception):
	# pass 是一个空语句，什么都不做
	pass

Error_Page="""\
<html>
<body>
<h1>Error accessing {path}</h1>
<p>{msg}</p>
</body>
</html>
"""
class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			# os.getcwd获取程序当前工作目录，返回一个字符串
			# self.path,客户端发来的http请求行
			full_path = os.getcwd()+self.path

			if not os.path.exists(full_path):
				# raise主动抛出一个异常
				# ServerException,自定义异常类
				# 0表示把第0个参数放到这个
				raise ServerException("'{0}' not found".format(self.path))
			elif os.path.isfile(full_path):
				self.handle_file(full_path)
			else:
				raise ServerException("Unknown object '{0}'".format(self.path))
		except Exception as msg:
			self.handle_error(msg)
			
	def handle_file(self,full_path):
		try:
			# with 保证文件用完后自动关闭，即使读取过程中出错也会关闭
			# rb 表示以二进制只读模式打开文件，read binary
			# reader 是文件对象
			# open()返回一个对象，as把它绑定到reader上
			with open(full_path,'rb') as reader:
				content = reader.read()
			self.send_content(content)
		# OSError 表示操作系统级别的输入输出错误
		# 捕获OSRrror异常，msg是异常对象
		except OSError as msg:
			msg = "'{0}' cannot be read:{1}".format(self.path,msg)
			self.handle_error(msg)

	def handle_error(self,msg):
		content = self.Error_Page.format(path=self.path,msg=msg)
		self.send_content(content,404)


	def send_content(self,content,status=200):
		if isinstance(content,str):
			content=content.encode('utf-8')
		# 发送状态码
		self.send_response(status)
		# 发送响应头
		self.send_header("Content-type","text/html;charset=utf-8")
		self.send_header("Content-Length",str(len(content)))
		self.end_headers()
		# 发送内容
		self.wfile.write(content)		

if __name__ == '__main__':
	serveraddress=('127.0.0.1',8080)
	server = HTTPServer(serveraddress,RequestHandler)
	server.serve_forever()