import logging
import stackless

from EVESession import EVESession


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
        
        self.session = EVESession(self)
        
        stackless.schedule()

    def network(self, clientsocket, address):
        logging.info("Client %s:%s connected!" % (address[0], address[1]))

        # Handshake with the client see EVESession.py for details
        # handshake(clientsocket)

        # If all is good:
        # We add the client to clients list
        # We start to listen for packets from the client

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

    def close(self, clientsocket):
        clientsocket.close()





