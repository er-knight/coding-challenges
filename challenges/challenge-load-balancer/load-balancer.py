from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
from colorama import Fore, init
import socketserver
import os
import threading
from collections import deque
import time

TERM = os.environ.get('TERM')
INFO = f'{Fore.LIGHTBLUE_EX}[LB]{Fore.RESET}' if TERM else '[LB]'
HEALTH = f'{Fore.LIGHTBLUE_EX}[HEALTH]{Fore.RESET}' if TERM else '[HEALTH]'

SERVERS = deque(['server-1', 'server-2', 'server-3', 'server-4'])
AVAILABLE_SERVERS = SERVERS

lock = threading.Lock()

def check_health():
    while True:
        _AVAILABLE_SERVERS = deque([])
        for server in SERVERS:
            try:
                connection = HTTPConnection(server, 8000)
                connection.request('GET', f'http://{server}:8000/', None, {})
                response = connection.getresponse()
                print(HEALTH, server, response, response.status)        
                if response.status == 200:
                    _AVAILABLE_SERVERS.append(server)
            except Exception as e:
                pass
        
        global AVAILABLE_SERVERS
        with lock:
            AVAILABLE_SERVERS = _AVAILABLE_SERVERS

        time.sleep(5)

class LoadBalancer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print(INFO, 'Received request')
        # print(self.client_address) # for ip-hash based routing
        self.route_request(self)

    @classmethod
    def route_request(cls, request):

        def parse_headers():
            headers = {}
            for line in str(request.headers).strip().split('\n'):
                key, value = line.split(': ')
                headers[key.strip()] = value.strip()
            return headers

        global AVAILABLE_SERVERS
        with lock:
            HOST = AVAILABLE_SERVERS.popleft()
            AVAILABLE_SERVERS.append(HOST)

        print(INFO, 'Routing request to', HOST.replace('-', ' '))
        
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

thread = threading.Thread(target=check_health)
thread.start()

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
    thread.join()
    print(INFO, 'Load balancer stopped')