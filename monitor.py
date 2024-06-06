from re import sub
from socket import socket, create_connection
from sys import argv, exit
from urllib.parse import urlparse

BUFFER = 4096
'''Socket buffer size'''

def random_port() -> int:
    '''
    Generate random available port number

    Returns:
        int: Random available port number
    '''
    with socket() as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]

def send(sock: socket, data: bytes) -> None:
    '''
    Send data to socket

    Args:
        sock (socket): Connected socket
        data (bytes): Data packet to be sent
    '''
    sock.sendall(data)

def receive(sock: socket) -> bytes:
    '''
    Receive data from socket

    Args:
        sock (socket): Connected socket

    Returns:
        bytes: Received data
    '''
    data, msg_length = b'', 0
    
    while True:
        packet = sock.recv(BUFFER)

        if not packet:
            break
        data += packet

        if len(data) >= msg_length:
            break

    return data

def connect(host: str | None, port: int, url: str) -> socket | None:
    '''
    Connect to server

    Args:
        host (str | None): Hostname, if applicable
        port (int): Port number
        sock (socket): Connected socket

    Returns:
        socket | None: Connected socket, if applicable
    '''
    try: return create_connection((host, port), timeout=5)
    except: print(f'URL: {url}\nStatus: Network Error\n')

def req(path: str, host: str | None) -> bytes:
    '''
    Send request

    Args:
        path (str): _description_
        host (str | None): Hostname, if applicable

    Returns:
        bytes: Encoded request
    '''
    request = f'GET {path} HTTP/1.0\r\n'
    request += f'Host: {host}\r\n'
    request += '\r\n'
    return request.encode()

def fetch_reference(html: str) -> str | None:
    '''
    Get URL from image (i.e. referenced object) in HTML

    Args:
        html (str): Chunk of HTML

    Returns:
        str | None: Image URL, if applicable
    '''
    for line in html.split('\n'):
        line = line.strip()
        if line.startswith('<img'):
            for word in line.split(' '):
                if word.startswith('src='):
                    return word.split('=')[1]

def handler(sock: socket, path: str, host: str | None, url: str, url_title: str):
    '''
    _summary_

    Args:
        sock (socket): Connected socket
        path (str): _description_
        host (str | None): Hostname, if applicable
        url (str): _description_
        url_title (str): Title of URL (e.g. 'URL', 'Redirected URL', etc.)

    Raises:
        ValueError: Invalid response line

    Returns:
        _type_: _description_
    '''
    # send http request                
    send(sock, req(path, host))

    # receive http response
    response = receive(sock).decode().split('\r\n')
    
    # 'Status' : f'{version} {status_num} {msg}'
    responses = { 'Status' : response[0] }

    for word in response[1:]:
        if not word or word == '' or word == ' ' or word == '\n':
            continue

        elif word:
            word = word.strip()
            if word.startswith('<') and (word.endswith('>') or word.endswith('>\r\n') or word.endswith('>\n') or word.endswith('>\r')):
                responses['HTML'] = word

            elif ': ' in word:
                key, val = word.split(': ', 1)
                responses[key] = val

    if responses['Status'] != ('' or ' ' or '\n' or '\r\n' or '\r'):
        status = responses['Status'].split(' ')
        # print('hhh', status)
        # print('eee', responses['Status'])
        url = sub('[\"\']', '', url)
        
        if status == ['']:
            print(f'{url_title}: {url}')
            return responses

        responses['Version'] = status[0]
        responses['Status'] = status[1]
        responses['Message'] = ' '.join(status[2:])

        # Print the status returned for URL
        print(f'{url_title}: {url}\nStatus: {responses['Status']} {responses['Message']}')
        if responses['Version'] and not responses['Version'].startswith('HTTP/'):
            raise ValueError('Invalid response line')

    return responses

if __name__ == '__main__':
    # get urls_file name from command line
    if len(argv) != 2:
        print('Usage: monitor urls_file')
        exit()

    # text file to get list of urls
    urls_file = argv[1]

    # Parse URLs from file
    with open(urls_file, 'r') as f:
        for url in f.readlines():
            # parse url
            url = url.strip()
            parsed_url = urlparse(url)
            
            # server/host
            host = parsed_url.hostname

            # port 80 for http, port 443 for https, random + available port for others
            port = parsed_url.port if parsed_url.port else 443 if parsed_url.scheme == 'https' else 80 if parsed_url.scheme == 'http' else random_port()

            # path
            path = parsed_url.path if parsed_url.path else '/'

            # create client socket, connect to server
            sock = connect(host, port, url)
            
            if sock:
                redirect, fetch = False, False
                
                header_info = handler(sock, path, host, url, 'URL')

                # Follow URL redirection
                if header_info['Status'] == ('301' or '302'):
                    redirect = True
                    url = header_info['Location'] if 'Location' in header_info else url
                    handler(sock, path, host, url, 'Redirected URL')
                
                # Fetch referenced object
                reference = fetch_reference(header_info['HTML'])
                if reference:
                    fetch = True
                    handler(sock, reference, host, url, 'Referenced URL')

                # Monitor HTTPS URLs

                sock.close()

                print()