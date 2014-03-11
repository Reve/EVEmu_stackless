import logging
import stackless

from Client import Client


class Connection:

    # TO-DO: implement packet queue

    def __init__(self, clientsocket, address, control):
        # Create manager channel which can inform us
        # about the results of any external manager's
        # actions (logging in, registering, etc)
        manager = stackless.channel()

        # Handle Messages in one tasklet
        stackless.tasklet(self.network)(clientsocket, address)

        self.control = control
        self.manager = manager

        self.services = []
        self.entity_list = []

    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        # Create new client
        client = Client((clientsocket, address), self.services)

        # Add client to entity list
        self.entity_list.append(client)

        data = ''
        while clientsocket.connect:
            data = clientsocket.recv(4096)
            if data == '':
                break
            
            logging.info(data)
            
            data = ''
            stackless.schedule()

        # Loop over, connection is broken
        self.close(clientsocket)
        self.entity_list.remove(client)

    def close(self, clientsocket):
        clientsocket.close()





