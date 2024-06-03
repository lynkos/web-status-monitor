from sys import argv, exit
from socket import create_connection

# get urls_file name from command line
if len(argv) != 2:
    print('Usage: monitor urls_file')
    exit()

# text file to get list of urls
urls_file = argv[1]

# server, port, and path should be parsed from url
host = 'inet.cs.fiu.edu'
port = 80 # use port 80 for http and port 443 for https
path = '/temp/fiu.jpg'

sock = None
# create client socket, connect to server
try:
    sock = create_connection((host, port), timeout=5)
except Exception as e:
    print(f'Network Error:\n {e}')

if sock:
    # send http request
    request = f'GET {path} HTTP/1.0\r\n'
    request += f'Host: {host}\r\n'
    request += '\r\n'
    sock.send(bytes(request, 'utf-8'))

    # receive http response
    response = b''
    while True:
        data = sock.recv(4096)
        if not data: break
        response += data
    print(response.decode('utf-8'))
    sock.close()