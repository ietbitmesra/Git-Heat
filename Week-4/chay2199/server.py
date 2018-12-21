# server.py
import os
import socket                   # Import socket module

class Server():

    def sendFile(self):
        port = 60001  # Reserve a port for your service.
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        s.bind((host, port))  # Bind to the port
        s.listen(1)  # Now wait for client connection.
        print('Server is ready!!')
        while True:
            (conn, addr) = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            try:
                pathName = os.getcwd()
                dir = open('dir_info.txt', 'w')
                for x in os.listdir(pathName):
                    if os.path.isfile(x):
                        dir.write('f-' + ' ' + x)
                    elif os.path.isdir(x):
                        dir.write('d-' + ' ' + x)
                    elif os.path.islink(x):
                        dir.write('l-' + ' ' + x)
                    else:
                        dir.write(' ' + ' ' + x)
                    dir.write('\n')
                dir.close()

            except NotADirectoryError:
                print('Oops directory not found')
            print('Sending server directory information......')
            f = open('dir_info.txt', 'r')
            l = f.read(1024)
            while l:
                conn.send(l.encode())
                l = f.read(1024)
            f.close()
            conn.close()
            print('Server directory information sent!!')

            port = 60002  # Reserve a port for your service.
            s = socket.socket()  # Create a socket object
            host = socket.gethostname()  # Get local machine name
            s.bind((host, port))  # Bind to the port
            s.listen(1)  # Now wait for client connection.

            print('Sending file....')
            while True:
                (conn, addr) = s.accept()     # Establish connection with client.
                file = conn.recv(1024)
                filename = file.decode('utf-8')
                if os.path.isfile(filename):
                    conn.send(str.encode("EXISTS " + str(os.path.getsize(filename))))
                    f = open(filename, 'rb')
                    l = f.read(1024)
                    while l:
                        conn.send(l)
                        l = f.read(1024)
                    f.close()
                    print('Done sending!')
                    conn.close()
                    print('Connection Closed!')

                else:
                    print('File not found')
                    conn.close()
                    print('Connection Closed!')


serverOne = Server()
serverOne.sendFile()
