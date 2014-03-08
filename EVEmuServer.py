import logging
import stackless
import StacklessSocket
StacklessSocket.install()
import socket

import Connection

class Server(object):
    def __init__(self, conn):
        self.connectedClients = []

        # Create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to an address and a port
        self.serversocket.bind(conn)
        # Become a server socket
        self.serversocket.listen(5)

        control = stackless.channel()

        stackless.tasklet(self.acceptConnection)(control)

        logging.info("Accepting connections on %s:[%s]" % (conn[0], conn[1]))

    def acceptConnection(self, control):
        while self.serversocket.accept:
            # Accept connections from outside
            clientsocket, clientaddress = self.serversocket.accept()

            # Now do something with the clientsocket
            # In this case, each client is managed in a tasklet

            # Update clients list
            self.connectedClients.append((clientsocket, clientaddress))

            # Also activate the connection handler
            Connection.Connection(clientsocket, clientaddress, control)

            stackless.schedule()

    def getConnectedClients(self):
        return self.connectedClients


if __name__ == "__main__":
    # Configure logging system
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    # Configure server
    host = "127.0.0.1"
    port = 26000
    logging.info("Starting up server")
    
    
    s = Server((host, port))
    stackless.run()