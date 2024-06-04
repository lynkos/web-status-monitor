from sys import argv, exit
from socket import create_connection
from urllib.parse import urlparse

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
            url = url.strip()
            parsed_url = urlparse(url)
            
            # server/host, port, and path should be parsed from url
            host = parsed_url.hostname
            port = parsed_url.port if parsed_url.port else 443 if parsed_url.scheme == 'https' else 80 # use port 80 for http and port 443 for https
            path = parsed_url.path if parsed_url.path else '/'

            # create client socket, connect to server
            try:
                sock = create_connection((host, port), timeout=5)
            except Exception as e:
                print(f'URL: {url}\nStatus: Network Error\n')
                continue

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
                response = response.decode()

                version, status, reason = response.split(None, 2)
                #version, status = response.split(None, 1)
                #reason = ''
                #version = ''

                status_msg = 'OK' if status.startswith('2') else 'Moved Permanently' if status.startswith('3') else 'Not Found' if status.startswith('4') else 'Unknown'

                # Print the status returned for each URL
                print(f'URL: {url}\nStatus: {status} {status_msg}\n')
                if version and not version.startswith('HTTP/'):
                    raise ValueError('Invalid response line')

                # Follow URL redirection

                # Fetch referenced object

                # Monitor HTTPS URLs

                sock.close()