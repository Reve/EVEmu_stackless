import stackless
import logging
import socket, struct

import PacketType


class Connection:
    def __init__(self, clientsocket, address, control):
        # Create manager channel which can inform us
        # about the results of any external manager's
        # actions (logging in, registering, etc)
        manager = stackless.channel()

        # Handle Messages in one tasklet
        stackless.tasklet(self.network)(clientsocket, address)

        self.control = control
        self.manager = manager

        stackless.schedule()

    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        data = ''
        while clientsocket.connect:
            data += clientsocket.recv(4096)
            if data == '':
                break

            # Check for a marshalled header
            if PacketType.MARSHALLED_HEADER in data:
                print("Received marshalled data: " + data)

            # Else check for gziped data

            data = ''
            stackless.schedule()

        # Loop over, connection is broken
        self.close(clientsocket)

    def close(self, clientsocket):
        clientsocket.close()







