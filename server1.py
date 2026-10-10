from http.server import BaseHTTPRequestHandler,HTTPServer

Page = '''\
<html>
<body>
<table>
<tr> <td>Header</td>				<td>Value</td>			</tr>
<tr> <td>Date and time</td>		<td>{date_time}</td>		</tr>
<tr> <td>Client host</td>		<td>{client_host}</td>	</tr>
<tr> <td>Client port</td>		<td>{client_port}</td>	</tr>
<tr> <td>Command</td>			<td>{command}</td>		</tr>
<tr> <td><Path</td>				<td>{path}</td>			</tr>
</table>
</body>
</html>
'''
class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		# 得到页面
		page = self.create_page()
		# 发送页面
		self.send_page(page)

	def create_page(self):
		values = {
			# self.date_time_string()是BaseHTTPRequestHandler提供的方法
			'date_time'		: self.date_time_string(),
			# client_address元组来自BaseHTTPRequestHandler
			# (host,port)
			'client_host'		: self.client_address[0],
			'client_port'		: self.client_address[1],
			# 客户端的请求方法，请求路径
			'command'			: self.command,
			'path'				: self.path
		}
		page=Page.format(**values)
		return page
	def send_page(self,page):
		# 发送状态码
		self.send_response(200)
		# 发送响应头
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",str(len(page.encode('utf-8'))))
		self.end_headers()
		# 发送内容
		self.wfile.write(page.encode('utf-8'))		
if __name__ == '__main__':
	serveraddress=('127.0.0.1',8080)
	server = HTTPServer(serveraddress,RequestHandler)
	server.serve_forever()