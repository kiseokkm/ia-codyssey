import http.server
import socketserver
from datetime import datetime

PORT = 8080

class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'접속 시간: {datetime.now()}')
        print(f'접속 IP: {self.client_address[0]}')

        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_message = '<h1>404 Not Found</h1><p>index.html 파일을 찾을 수 없습니다.</p>'
            self.wfile.write(error_message.encode('utf-8'))

def run_server():
    handler_object = MyHttpRequestHandler
    with socketserver.TCPServer(('', PORT), handler_object) as httpd:
        print(f'서버가 {PORT} 포트에서 실행 중입니다...')
        print('웹 브라우저에서 http://127.0.0.1:8080/ 으로 접속하세요.')
        print('서버를 중지하려면 Ctrl+C를 누르세요.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n서버를 종료합니다.')
            httpd.shutdown()

if __name__ == '__main__':
    run_server()