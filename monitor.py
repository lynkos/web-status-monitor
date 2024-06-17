from re import sub
from socket import socket, create_connection
from sys import argv, exit
from urllib.parse import urljoin, urlparse

BUFFER = 4096
'''Socket buffer size'''    

def receive(sock: socket) -> bytes:
    '''
    Receive data from socket

    Args:
        sock (socket): Connected socket

    Returns:
        bytes: Received data
    '''        
    data = b''
    
    while True:
        packet = sock.recv(BUFFER)
        if not packet: break
        data += packet

    return data

def encode_request(path: str, host: str | None, https: bool) -> bytes:
    '''
    Encode request

    Args:
        path (str): Requested [URL] path
        host (str | None): Hostname, if applicable
        https (bool): HTTPS or HTTP

    Returns:
        bytes: Encoded request
    '''    
    version = '1.1' if https else '1.0'
    request = f'GET {path} HTTP/{version}\r\n'
    request += f'Host: {host}\r\n'
    request += '\r\n'
    
    return request.encode()

def validate_url(orig_url: str, relative_url: str) -> str:
    '''
    Get absolute URL from relative URL

    Args:
        orig_url (str): Original URL
        relative_url (str): Relative URL

    Returns:
        str: Absolute URL
    '''
    return urljoin(orig_url, relative_url)

def get_reference(html: str, abs_url: str) -> list[str]:
    '''
    Get URL from image (i.e. referenced object) in HTML

    Args:
        html (str): Chunk of HTML
        abs_url (str): Absolute URL

    Returns:
        list[str]: List of referenced image URLs
    '''
    references = [ ]
    
    for line in html.split('\n'):
        line = line.strip()

        # check for image tag
        if line.lower().startswith('<img'):
            for word in line.split(' '):
                # check for src attribute
                if word.lower().startswith('src='):
                    # extract and validate URL
                    url = word.split('=')[1].strip()
                    url = sub('[\"\']', '', url)
                    absolute_url = validate_url(abs_url, url)
                    references.append(absolute_url)

    return references

def handler(url: str, url_title: str) -> None:
    '''    
    Handle URL

    Args:
        url (str): URL to be handled
        url_title (str): Title of URL
    '''
    # parse url
    parsed_url = urlparse(url)
    
    # init sock and responses
    sock = responses = None

    # create client socket, connect to server
    try:
        if parsed_url.scheme == 'http': sock = create_connection((parsed_url.hostname, 80), 5)

        # use SSL socket for HTTPS
        elif parsed_url.scheme == 'https':
            from ssl import create_default_context
            context = create_default_context()
            sock = create_connection((parsed_url.hostname, 443), 5)
            sock = context.wrap_socket(sock, server_hostname = parsed_url.hostname)
            
    except: print(f'{url_title}: {url}\nStatus: Network Error')

    if sock:
        https = True if parsed_url.scheme == 'https' else False
        
        # send encoded request
        sock.sendall(encode_request(parsed_url.path, parsed_url.hostname, https))

        # receive, decode, and split response
        response = receive(sock)
        response = response.decode(errors = 'replace') # alt: errors = 'ignore'
        response = response.split('\r\n')
        response = [ r for r in response if r != '\r\n' and r != '' ]

        # last element is HTML chunk
        responses = { 'HTML' : response[-1] }

        # parse info from response
        for word in response[1:-1]:
            if word != (' ' or '\n'):
                word = word.strip()
                if ':' in word:
                    key, val = word.split(':', 1)
                    key, val = key.strip(), val.strip()
                    responses[key] = val

        # separate status from 'HTTP/1.*'
        status = response[0].split(' ')
        responses['Status'] = ' '.join(status[1:])

        # print URL and status
        print(f'{url_title}: {url}\nStatus: {responses['Status']}')

        # check for redirection
        if status[1] == '301' or status[1] == '302':
            redirected_url = validate_url(url, responses['Location'])
            handler(redirected_url, 'Redirected URL')

        # check for referenced URLs
        for reference in get_reference(responses['HTML'], url):
            handler(reference, 'Referenced URL')
            
        # close socket
        sock.close()

if __name__ == '__main__':
    # get filename from command line
    if len(argv) != 2:
        print('Usage: monitor urls-file')
        exit()

    # text file to get list of urls
    urls = argv[1]

    # Parse URLs from file
    with open(urls, 'r') as f:
        for url in f.readlines():
            url = url.strip()

            if url:
                handler(url, 'URL')
                print()