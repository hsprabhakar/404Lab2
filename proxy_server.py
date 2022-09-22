#!/usr/bin/env python3
import socket
import time
import sys

#define address & buffer size
HOST = ""
PORT = 8001
GOOGLE_HOST = 'www.google.com'
GOOGLE_PORT = 80
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            conn.sendall(full_data)

            # Proxy clinet time!
            try:
                pxyc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except (socket.error, msg):
                print(f'Failed to create proxy client socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
                sys.exit()
            
            print('Client Proxy Socket created successfully\n')

            remote_ip = get_remote_ip_as_proxy_client(GOOGLE_HOST)
            pxyc.connect((remote_ip , GOOGLE_PORT))
            p = Process(target=handle_echo, args=(proxy_end, addr, conn))
            p.daemon = True
            p.start()
            print("Started Process", p)

            print (f'Socket Connected to {GOOGLE_HOST} on ip {remote_ip}')

            #payload = f'GET / HTTP/1.0\r\nHost: {GOOGLE_HOST}\r\n\r\n'

            send_data(pxyc, full_data)
            pxyc.shutdown(socket.SHUT_WR)
            google_data = b""
            while True:
                data = pxyc.recv(1024)
                if not data:
                    break
                google_data += data

            print(google_data)
            conn.sendall(google_data)
            conn.close()
            break
        s.close()

            #proxy server time!
            

def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")


def get_remote_ip_as_proxy_client(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
if __name__ == "__main__":
    main()
