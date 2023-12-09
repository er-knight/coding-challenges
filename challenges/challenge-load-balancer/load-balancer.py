from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
from colorama import Fore, init
import socketserver
import os

TERM = os.environ.get('TERM')
INFO = f'{Fore.LIGHTBLUE_EX}[LB]{Fore.RESET}' if TERM else '[LB]'

class LoadBalancer(BaseHTTPRequestHandler):
    
    SERVERS = ['server-1', 'server-2']
    CURRENT = 0

    def do_GET(self):
        print(INFO, 'Received request')
        self.route_request(self)

    @classmethod
    def route_request(cls, request):

        def parse_headers():
            headers = {}
            for line in str(request.headers).strip().split('\n'):
                key, value = line.split(': ')
                headers[key.strip()] = value.strip()
            return headers

        HOST = cls.SERVERS[cls.CURRENT]
        print(INFO, 'Routing request to', HOST.replace('-', ' '))

        cls.CURRENT = (cls.CURRENT + 1) % len(cls.SERVERS) 

        PORT = 8000

        METHOD = request.command
        PATH = request.path
        HEADERS = parse_headers(); 
        URL = f'http://{HOST}:{PORT}{PATH}'

        connection = HTTPConnection(HOST, PORT)
        connection.request(METHOD, URL, None, HEADERS)

        response = connection.getresponse()

        request.send_response(response.status)

        for key, value in response.getheaders():
            request.send_header(key, value)
        request.end_headers()

        request.wfile.write(response.read())

        connection.close()

PORT = 8000

load_balancer = socketserver.TCPServer(('', PORT), LoadBalancer)

if TERM:
    os.system('clear')

init()

print()
print(INFO, 'Load balancer started ...')
print(INFO, 'Listening on port', PORT)

try:
    load_balancer.serve_forever()
except KeyboardInterrupt as exc:
    print(INFO, 'Stopping load balancer ...')
finally:
    print(INFO, 'Load balancer stopped')