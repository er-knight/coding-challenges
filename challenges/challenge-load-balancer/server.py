from http.server import BaseHTTPRequestHandler
from colorama import Fore, init
import socketserver
import os

SERVER_ID = os.environ.get('SERVER_ID')
TERM = os.environ.get('TERM')
INFO = f'{Fore.LIGHTBLUE_EX}[SERVER-{SERVER_ID}]{Fore.RESET}' if TERM else f'[SERVER-{SERVER_ID}]'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        print(INFO, 'Received request')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        self.wfile.write(f'Hello there! I am Server {SERVER_ID}'.encode())

PORT = 8000

httpd = socketserver.TCPServer(('', PORT), RequestHandler)

if TERM:
    os.system('clear')

init()

print()
print(INFO, 'Server started ...')
print(INFO, 'Listening on port', PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt as exc:
    print(INFO, 'Stopping server ...')
finally:
    print(INFO, 'Server stopped')