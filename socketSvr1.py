import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 7682)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
i=0
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a new connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1300)
            print >>sys.stderr, 'received a packet with "%d" bytes' % len(data)
            if data:
                ack = 'ok:' + str(len(data))
                connection.sendall(ack)
                i=i+1
                rawFile="logs/" + str(i) + ".raw"
                outfil=open(rawFile,"wb")
                outfil.write(data)
                outfil.close()
                print >>sys.stderr, 'save the packet to file:"%s"' % rawFile

            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()

